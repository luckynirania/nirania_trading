import time
from opentelemetry import trace
from univest.models import Idea
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
        log.add_event(f"begin the loop for {times} times and delay = {delay} secs")
        for i in range(times):
            log.add_event(
                f"iteration {i + 1} begin, calling fetch_and_store_ideas_from_univest_api"
            )
            start_time = datetime.now()
            fetch_and_store_ideas_from_univest_api()

            end_time = datetime.now()
            time_elapsed = (end_time - start_time).total_seconds()
            sleep_time = max(0, delay - time_elapsed)

            log.add_event(f"iteration {i + 1} end, sleeping for {sleep_time} secs")
            time.sleep(sleep_time)

        log.add_event("end loop")
        log.add_event("calling fetch_and_store_ideas_from_univest_api last time")
        fetch_and_store_ideas_from_univest_api()
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
