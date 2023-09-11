from typing import Dict, Any
from datetime import datetime, time

from angel_broking.constants import (
    Duration,
    Exchange,
    OrderType,
    ProductType,
    TransactionType,
    Variety,
)


class YourValidationError(Exception):
    pass


def validate_order_params(orderparams: Dict[str, Any]) -> bool:
    # Check for mandatory fields
    mandatory_fields = [
        "variety",
        "tradingsymbol",
        "symboltoken",
        "transactiontype",
        "exchange",
        "ordertype",
        "producttype",
        "duration",
        "quantity",
    ]
    for field in mandatory_fields:
        if field not in orderparams:
            raise YourValidationError(f"{field} is missing")

    # Check if enums match
    if orderparams["variety"] not in Variety.__members__:
        raise YourValidationError("Invalid variety")
    if orderparams["transactiontype"] not in TransactionType.__members__:
        raise YourValidationError("Invalid transactiontype")
    if orderparams["ordertype"] not in OrderType.__members__:
        raise YourValidationError("Invalid ordertype")
    if orderparams["producttype"] not in ProductType.__members__:
        raise YourValidationError("Invalid producttype")
    if orderparams["duration"] not in Duration.__members__:
        raise YourValidationError("Invalid duration")
    if orderparams["exchange"] not in Exchange.__members__:
        raise YourValidationError("Invalid exchange")

    # Additional Conditions
    if orderparams["ordertype"] == OrderType.LIMIT and "price" not in orderparams:
        raise YourValidationError("Price is mandatory for LIMIT orders")

    if (
        orderparams["ordertype"]
        in [OrderType.STOPLOSS_LIMIT, OrderType.STOPLOSS_MARKET]
        and "triggerprice" not in orderparams
    ):
        raise YourValidationError(
            "Trigger price is mandatory for STOPLOSS_LIMIT or STOPLOSS_MARKET orders"
        )

    if orderparams["variety"] == "ROBO" and not all(
        k in orderparams for k in ["squareoff", "stoploss", "trailingStopLoss"]
    ):
        raise YourValidationError(
            "squareoff, stoploss, and trailingStopLoss are mandatory for ROBO orders"
        )

    return True


def pre_traing_hours() -> bool:
    current_time = datetime.now().time()
    start_time = time(9, 0)  # 9:00 AM
    end_time = time(9, 15)  # 9:15 AM

    return start_time <= current_time <= end_time


def is_market_open() -> bool:
    current_time = datetime.now().time()
    start_time = time(9, 15)  # 9:15 AM
    end_time = time(15, 30)  # 3:30 PM

    return start_time <= current_time <= end_time


def after_market_hours() -> bool:
    return not pre_traing_hours() and not is_market_open()
