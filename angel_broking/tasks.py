from datetime import datetime
import json
from opentelemetry import trace
from angel_broking.models import SymbolTokenMappingSheet
from univest.constants import OrderStatusChoices
from univest.models import Order
from utils.tracing_utils import remove_http_https, request_with_trace
from django.db import transaction
import angel_broking.utilities.orders as broker


def call_open_api_to_populate_mapping_sheet():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("call_open_api_to_populate_mapping_sheet") as log:
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        log.add_event(f"initiating call for {remove_http_https(url)}")
        response = request_with_trace(tracer=tracer, url=url, method="GET")

        if response.status_code == 200:
            # Clear the table
            with transaction.atomic():
                SymbolTokenMappingSheet.objects.all().delete()

                # Prepare the data for bulk insert
                bulk_list = []
                for item in response.json():
                    expiry = (
                        datetime.strptime(item.get("expiry"), "%d%b%Y")
                        if item.get("expiry")
                        else None
                    )
                    obj = SymbolTokenMappingSheet(
                        token=item.get("token", ""),
                        symbol=item.get("symbol", ""),
                        name=item.get("name", ""),
                        expiry=expiry,
                        strike=str(item.get("strike", "")),
                        lotsize=int(item.get("lotsize", 1)),
                        instrumenttype=item.get("instrumenttype", ""),
                        exch_seg=item.get("exch_seg", ""),
                        tick_size=item.get("tick_size", ""),
                    )
                    bulk_list.append(obj)

                # Perform bulk insert
                SymbolTokenMappingSheet.objects.bulk_create(bulk_list)


def get_trade_book_and_update_order_status():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("get_trade_book_and_update_order_status") as log:
        order_book = broker.get_order_book()
        log.add_event(
            "order_book ",
            attributes={"order_book": json.dumps(order_book)},
        )
        for order in order_book["message"]:
            log.add_event("order from_api ", order)
            order_id_from_api = order["orderid"]
            log.add_event(f"order_id_from_api {order_id_from_api}")
            try:
                order_instance = Order.objects.get(
                    exchange_order_id=order_id_from_api,
                    status=OrderStatusChoices.PLACED.name,
                )  # Assuming the field name is 'order_id'
                log.add_event("found ")
            except Order.DoesNotExist:
                log.add_event("not found ")
                continue  # Skip if the order is not found

            if order["orderstatus"] == "rejected":
                order_instance.status = OrderStatusChoices.REJECTED.name
            elif order["orderstatus"] == "complete":
                order_instance.status = OrderStatusChoices.EXECUTED.name
            elif order["orderstatus"] == "cancelled":
                order_instance.status = OrderStatusChoices.CANCELLED.name
            else:
                log.add_event("unknown order status ", order["orderstatus"])
                continue  # Skip if the order is not found

            order_instance.save()
