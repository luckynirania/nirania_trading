import json
import math
import time
from opentelemetry import trace
from angel_broking.constants import (
    PER_ORDER_AMOUNT,
    Duration,
    Exchange,
    OrderType,
    ProductType,
    TransactionType,
    Variety,
)
from angel_broking.models import SymbolTokenMappingSheet
from angel_broking.utilities.common import is_market_open, pre_traing_hours
from univest.constants import IdeaStatusChoices, OrderStatusChoices, OrderTypeChoices
from univest.models import Idea, IdeaStatus, Order
from utils.tracing_utils import remove_http_https, request_with_trace
from django.forms.models import model_to_dict

from datetime import datetime
from dotenv import load_dotenv
import os
import angel_broking.utilities.orders as broker

load_dotenv()


def call_google():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("call_google") as log:
        url = "https://www.google.com"
        log.add_event(f"initiating call for {remove_http_https(url)}")
        request_with_trace(tracer=tracer, url=url, method="GET")


def loop_univest_fetch(times: int, delay: int):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("loop_univest_fetch") as log:
        log.add_event(f"begin the loop for {times - 1} times and delay = {delay} secs")
        for i in range(times - 1):
            log.add_event(
                f"iteration {i + 1} begin, calling fetch_and_store_ideas_from_univest_api"
            )
            start_time = datetime.now()
            fetch_and_store_ideas_from_univest_api()

            log.add_event("populate idea statuses and buy short term new ideas")
            populate_idea_statuses()
            place_market_buy_order_for_new_ideas(term="SHORT")

            end_time = datetime.now()
            time_elapsed = (end_time - start_time).total_seconds()
            sleep_time = max(0, delay - time_elapsed)

            log.add_event(f"iteration {i + 1} end, sleeping for {sleep_time} secs")
            time.sleep(sleep_time)

        log.add_event("end loop")
        log.add_event("calling fetch_and_store_ideas_from_univest_api last time")
        fetch_and_store_ideas_from_univest_api()

        log.add_event("populate idea statuses and buy short term new ideas")
        populate_idea_statuses()
        place_market_buy_order_for_new_ideas(term="SHORT")

        log.add_event("all calls completed, exiting ...")


def fetch_and_store_ideas_from_univest_api():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("fetch_and_store_ideas_from_univest_api") as log:
        url = "https://api.univest.in/resources/trade-cards"
        token = f"Bearer {os.environ.get('UNIVEST_BEARER_TOKEN')}"
        headers = {"authorization": token}

        log.add_event(f"initiating call for {remove_http_https(url)}")

        response = request_with_trace(
            tracer=tracer,
            url=url,
            method="GET",
            headers=headers,
        )
        if response.status_code == 200:
            api_data = response.json().get("data", {}).get("list", [])
            for item in api_data:
                Idea.objects.update_or_create(
                    univest_id=item["id"],
                    defaults={
                        "streamChannelId": item.get("streamChannelId"),
                        "streamMessageId": item.get("streamMessageId"),
                        "senderId": item.get("senderId"),
                        "stockName": item.get("stockName"),
                        "suggestedPrice": item.get("suggestedPrice"),
                        "expiresAt": item.get("expiresAt"),
                        "targetPrice": item.get("targetPrice"),
                        "stopLoss": item.get("stopLoss"),
                        "recommendationType": item.get("recommendationType"),
                        "confidenceLevel": item.get("confidenceLevel"),
                        "closureReason": item.get("closureReason"),
                        "bsePriceAtClosure": item.get("bsePriceAtClosure"),
                        "nsePriceAtClosure": item.get("nsePriceAtClosure"),
                        "createdAt": item.get("createdAt"),
                        "lastModified": item.get("lastModified"),
                        "channelName": item.get("channelName"),
                        "firstName": item.get("firstName"),
                        "lastName": item.get("lastName"),
                        "senderContactNumber": item.get("senderContactNumber"),
                        "profilePictureUrl": item.get("profilePictureUrl"),
                        "open": item.get("open"),
                        "hit": item.get("hit"),
                        "finCode": item.get("finCode"),
                        "expectedDurationEnum": item.get("expectedDurationEnum"),
                        "status": item.get("status"),
                        "type": item.get("type"),
                        "watchListIds": item.get("watchListIds"),
                        "analysis": item.get("analysis"),
                        "attachments": item.get("attachments"),
                        "term": item.get("term"),
                        "newTradeCard": item.get("newTradeCard"),
                        "locked": item.get("locked"),
                        "logoUrl": item.get("logoUrl"),
                        "compName": item.get("compName"),
                        "netGain": item.get("netGain"),
                    },
                )


def populate_idea_statuses():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("populate_idea_statuses") as log:
        log.add_event("begin adding new idea into idea status table")
        # First, populate the IdeaStatus table with status "NEW" for all ideas
        for idea in Idea.objects.all():
            IdeaStatus.objects.get_or_create(
                idea=idea,
                defaults={
                    "status": IdeaStatusChoices.NEW.name,
                },
            )
        log.add_event("addition completed, identifying expired ideas")

        expired_ideas = Idea.objects.exclude(status="OPEN")
        for idea_status in IdeaStatus.objects.filter(
            idea__in=expired_ideas,
            order__isnull=True,
            status=IdeaStatusChoices.NEW.name,
        ):
            idea_status.status = IdeaStatusChoices.EXPIRED.name
            idea_status.save()

        log.add_event("filtered expired ideas and marked")


def place_market_buy_order_for_new_ideas(term):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("place_market_buy_order_for_new_ideas") as log:
        log.add_event(f"begin buying ideas which are NEW for term = {term}")
        # Query IdeaStatus objects where status is 'NEW' and related Idea has the specified term
        all_new_ideas = IdeaStatus.objects.filter(status="NEW")
        new_ideas = IdeaStatus.objects.filter(status="NEW", idea__term=term)

        log.add_event(
            "all_new_ideas ",
            attributes={
                "all_new_ideas ideas": json.dumps(
                    [
                        {**model_to_dict(instance), "term": instance.idea.term}
                        for instance in all_new_ideas
                    ]
                ),
            },
        )

        log.add_event(
            "new ideas ",
            attributes={
                "new ideas": json.dumps(
                    [
                        {**model_to_dict(instance), "term": instance.idea.term}
                        for instance in new_ideas
                    ]
                )
            },
        )

        # Iterate over the filtered IdeaStatus objects and print them
        for idea_status in new_ideas:
            if pre_traing_hours():
                log.add_event(
                    f"Pre-trading hours. Skipping idea: {idea_status.idea.stockName}"
                )
                continue

            orderparams = construct_order_params(idea_status=idea_status)
            # Place the order
            order = broker.place_order(
                orderparams=orderparams,
            )

            save_order_details(order, idea_status, orderparams)

            log.add_event(
                f"IdeaStatus ID: {idea_status.id}, Related Idea: {idea_status.idea.stockName}, Status: {idea_status.status}"
            )

        log.add_event("market buy orders placed successfully")


def construct_order_params(idea_status: IdeaStatus) -> dict:
    # Initialize default values
    trading_symbol = f"{idea_status.idea.stockName}-EQ"
    try:
        symbol_token = SymbolTokenMappingSheet.objects.get(symbol=trading_symbol).token
    except SymbolTokenMappingSheet.DoesNotExist:
        symbol_token = None  # Or whatever default value or exception you want

    variety = Variety.AMO.name
    order_type = OrderType.LIMIT.name
    quantity = str(math.ceil(PER_ORDER_AMOUNT / idea_status.idea.suggestedPrice))
    price = None  # Not setting the price initially

    # Check if market is open
    if is_market_open():
        variety = Variety.NORMAL.name
        order_type = OrderType.MARKET.name
    else:
        suggested_price = idea_status.idea.suggestedPrice
        increased_price = suggested_price * 1.005
        rounded_price = math.ceil(increased_price * 100) / 100.0
        price = "{:.2f}".format(round(math.ceil(rounded_price / 0.05) * 0.05, 2))

    orderparams = {
        "disclosedquantity": "0",
        "duration": Duration.DAY.name,
        "exchange": Exchange.NSE.name,
        "ordertype": order_type,
        "producttype": ProductType.DELIVERY.name,
        "quantity": quantity,
        "price": "0",
        "stoploss": "0",
        "squareoff": "0",
        "tradingsymbol": trading_symbol,
        "transactiontype": TransactionType.BUY.name,
        "triggerprice": "0.00",
        "trailingStopLoss": "0",
        "variety": variety,
        "orderValidityDate": datetime.now().strftime("%d/%m/%Y"),
    }

    # Add price if it's available
    if price:
        orderparams["price"] = price

    if symbol_token:
        orderparams["symboltoken"] = symbol_token

    return orderparams


def save_order_details(order: dict, idea_status: IdeaStatus, orderparams: dict) -> None:
    if order["status"] is True:
        order_id = order["message"]["data"]["orderid"]
        try:
            price = float(orderparams["price"])
        except:  # noqa E722
            price = 0
        Order.objects.create(
            idea_status=idea_status,
            order_type=OrderTypeChoices.BUY.name,
            order_sub_type=OrderType.MARKET.name,
            status=OrderStatusChoices.PLACED.name,
            price=price,
            quantity=float(orderparams["quantity"]),
            exchange_order_id=order_id,
        )
