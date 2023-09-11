from datetime import datetime
from opentelemetry import trace
from angel_broking.models import SymbolTokenMappingSheet
from utils.tracing_utils import remove_http_https, request_with_trace
from django.db import transaction


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
