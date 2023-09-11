from opentelemetry import trace
from angel_broking.utilities.apis.smart_api.smart_web_socketV2 import SmartWebSocketV2

AUTH_TOKEN = "authToken"
API_KEY = "api_key"
CLIENT_CODE = "client code"
FEED_TOKEN = "feedToken"
correlation_id = "abc123"
action = 1
mode = 1

token_list = [{"exchangeType": 1, "tokens": ["26009"]}]
token_list1 = [{"action": 0, "exchangeType": 1, "tokens": ["26009"]}]

sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("place_order") as log:

    def on_data(wsapp, message):
        log.add_event("Ticks: {}".format(message))
        # close_connection()

    def on_open(wsapp):
        log.add_event("on open")
        sws.subscribe(correlation_id, mode, token_list)
        # sws.unsubscribe(correlation_id, mode, token_list1)

    def on_error(wsapp, error):
        log.add_event(error)

    def on_close(wsapp):
        log.add_event("Close")

    def close_connection():
        sws.close_connection()


# Assign the callbacks.
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error
sws.on_close = on_close

sws.connect()
