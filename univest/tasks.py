import time
from opentelemetry import trace
from univest.models import Idea, IdeaStatus
from utils.tracing_utils import request_with_trace
from opentelemetry.instrumentation.django import DjangoInstrumentor
from datetime import datetime
from dotenv import load_dotenv
import os

DjangoInstrumentor().instrument()
load_dotenv()


def call_google():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("call_google") as log:
        url = "www.google.com"
        log.add_event(f"initiating call for {url}")
        request_with_trace(tracer=tracer, endpoint=url, method="GET")


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
        url = "api.univest.in/resources/trade-cards"
        token = f"Bearer {os.environ.get('UNIVEST_BEARER_TOKEN')}"
        headers = {"authorization": token}

        log.add_event(f"initiating call for {url}")

        response = request_with_trace(
            tracer=tracer,
            endpoint=url,
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
                    "status": "NEW",
                },
            )
        log.add_event("addition completed, identifying expired ideas")

        expired_ideas = Idea.objects.exclude(status="OPEN")
        for idea_status in IdeaStatus.objects.filter(
            idea__in=expired_ideas, order__isnull=True, status="NEW"
        ):
            idea_status.status = "EXPIRED"
            idea_status.save()

        log.add_event("filtered expired ideas and marked")


def place_market_buy_order_for_new_ideas(term):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("place_market_buy_order_for_new_ideas") as log:
        log.add_event(f"begin buying ideas which are NEW for term = {term}")
        # Query IdeaStatus objects where status is 'NEW' and related Idea has the specified term
        new_ideas = IdeaStatus.objects.filter(status="NEW", idea__term=term)

        # Iterate over the filtered IdeaStatus objects and print them
        for idea_status in new_ideas:
            log.add_event(
                f"IdeaStatus ID: {idea_status.id}, Related Idea: {idea_status.idea.stockName}, Status: {idea_status.status}"
            )

        log.add_event("market buy orders placed successfully")
