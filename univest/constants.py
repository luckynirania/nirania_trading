# constants.py

from enum import Enum


class OrderTypeChoices(Enum):
    SELL = "Sell"
    BUY = "Buy"


class OrderSubTypeChoices(Enum):
    GTT = "GTT"
    MARKET = "Market"
    LIMIT = "Limit"
    STOP_LOSS = "Stop Loss"


class OrderStatusChoices(Enum):
    PLACED = "Placed"
    CANCELLED = "Cancelled"
    EXECUTED = "Executed"
    REJECTED = "Rejected"


class IdeaStatusChoices(Enum):
    NEW = "New"
    BUY_ORDER_PLACED = "Buy Order Placed"
    BUY_ORDER_CANCELLED = "Buy Order Cancelled"
    BOUGHT = "Bought"
    SELL_ORDER_PLACED = "Sell Order Placed"
    SELL_ORDER_CANCELLED = "Sell Order Cancelled"
    SOLD = "Sold and Closed"
    EXPIRED = "Idea was already Closed"


# Convert Enum to choices that can be used in Django models
ORDER_TYPE_CHOICES = [(e.name, e.value) for e in OrderTypeChoices]
ORDER_SUB_TYPE_CHOICES = [(e.name, e.value) for e in OrderSubTypeChoices]
ORDER_STATUS_CHOICES = [(e.name, e.value) for e in OrderStatusChoices]
IDEA_STATUS_CHOICES = [(e.name, e.value) for e in IdeaStatusChoices]
