# constants.py

from enum import Enum


class OrderTypeChoices(Enum):
    SELL = "Sell"
    BUY = "Buy"
    GTT_SELL = "GTT Sell"
    GTT_BUY = "GTT Buy"


class OrderStatusChoices(Enum):
    PLACED = "Placed"
    CANCELLED = "Cancelled"
    EXECUTED = "Executed"


class IdeaStatusChoices(Enum):
    NEW = "New"
    BUY_ORDER_PLACED = "Buy Order Placed"
    BUY_ORDER_CANCELLED = "Buy Order Cancelled"
    BUY_GTT_ORDER_PLACED = "Buy GTT Order Placed"
    BUY_GTT_ORDER_CANCELLED = "Buy GTT Order Cancelled"
    BOUGHT = "Bought"
    SELL_ORDER_PLACED = "Sell Order Placed"
    SELL_ORDER_CANCELLED = "Sell Order Cancelled"
    SELL_GTT_ORDER_PLACED = "Sell GTT Order Placed"
    SELL_GTT_ORDER_CANCELLED = "Sell GTT Order Cancelled"
    SOLD = "Sold and Closed"
    EXPIRED = "Idea was already Closed"


# Convert Enum to choices that can be used in Django models
ORDER_TYPE_CHOICES = [(e.name, e.value) for e in OrderTypeChoices]
ORDER_STATUS_CHOICES = [(e.name, e.value) for e in OrderStatusChoices]
IDEA_STATUS_CHOICES = [(e.name, e.value) for e in IdeaStatusChoices]
