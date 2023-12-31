import json
import os
from opentelemetry import trace
from angel_broking.utilities.apis.smart_api.smart_connect import SmartConnect
from angel_broking.utilities.common import YourValidationError, validate_order_params
from dotenv import load_dotenv

load_dotenv()


def place_order(orderparams: {}) -> dict:
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("place_order") as log:
        log.add_event(f"received orderparams : {orderparams}")
        log.add_event("validating order params")
        try:
            validate_order_params(orderparams)
        except YourValidationError as e:
            log.add_event(f"Validation Error: {e}")
            return {
                "status": False,
                "message": f"Validation Error: {e}",
            }

        obj = SmartConnect(
            access_token=os.environ.get("ANGEL_ONE_ACCESS_TOKEN"),
            bearer_token=os.environ.get("ANGEL_ONE_BEARER_TOKEN"),
            tracer=tracer,
        )

        log.add_event(
            "placing the order with params : ",
            attributes={"orderparams": json.dumps(orderparams)},
        )
        # return {
        #     "status": True,
        #     "message": {"data": {"orderid": "some_order_id"}},
        # }
        try:
            response = obj.placeOrderCustom(orderparams)
            return {
                "status": True,
                "message": response,
            }
        except Exception as e:
            log.set_attribute("error", True)
            log.add_event("Order placement failed: {}".format(e.message))
            return {
                "status": False,
                "message": "Order placement failed: {}".format(e.message),
            }


def get_order_book() -> dict:
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("get_order_book") as log:
        log.add_event("received get_order_book call")
        # obj = SmartConnect(
        #     access_token=os.environ.get("ANGEL_ONE_ACCESS_TOKEN"),
        #     bearer_token=os.environ.get("ANGEL_ONE_BEARER_TOKEN"),
        #     tracer=tracer,
        # )

        # return {
        #     "status": True,
        #     "message": {"data": {"orderid": "some_order_id"}},
        # }
        try:
            import requests

            url = "https://amx.angeltrade.com/report/order/v3/getOrderBook"

            payload = {}
            headers = {
                "Authorization": f"Bearer {os.environ.get('ANGEL_ONE_BEARER_TOKEN')}",
            }

            response = requests.request(
                "GET", url, headers=headers, data=payload
            ).json()

            log.add_event("response ", attributes={"response": json.dumps(response)})

            # print(response.text)

            # response = obj.orderBookCustom()
            return {
                "status": True,
                "message": response["data"],
            }
        except Exception as e:
            log.set_attribute("error", True)
            log.add_event("Order placement failed: {}".format(e.message))
            return {
                "status": False,
                "message": "Order placement failed: {}".format(e.message),
            }
