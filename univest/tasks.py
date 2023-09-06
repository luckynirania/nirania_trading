from django_q.tasks import async_task
from opentelemetry import trace
from univest.models import Idea
from utils.tracing_utils import request_with_trace
from opentelemetry.instrumentation.django import DjangoInstrumentor

DjangoInstrumentor().instrument()


def call_google():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("call_google") as log:
        url = "www.google.com"
        log.add_event(f"initiating call for {url}")
        request_with_trace(tracer=tracer, endpoint=url, method="GET")


def fetch_and_store_ideas_from_univest_api():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("fetch_and_store_ideas_from_univest_api") as log:
        url = "api.univest.in/resources/trade-cards"
        headers = {
            "authorization": "Bearer eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiIyODc5NTQiLCJpYXQiOjE2ODk0MTI1NDd9.F5Z6l_j7qw4CZwCBw8P5AuTjfZkyMn2CTxPkjJCLD3ZbR6Y1NTJ0FbmqWz6J_5A1"
        }
        log.add_event(f"initiating call for {url}")
        response = request_with_trace(
            tracer=tracer, endpoint=url, method="GET", headers=headers
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


# To enqueue the task, use the following:
async_task("univest.tasks.call_google")
async_task("univest.tasks.fetch_and_store_ideas_from_univest_api")
