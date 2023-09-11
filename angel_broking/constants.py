from enum import Enum

PER_ORDER_AMOUNT = 15000


class Variety(Enum):
    NORMAL = "NORMAL"
    STOPLOSS = "STOPLOSS"
    AMO = "AMO"
    ROBO = "ROBO"


class TransactionType(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOPLOSS_LIMIT = "STOPLOSS_LIMIT"
    STOPLOSS_MARKET = "STOPLOSS_MARKET"


class ProductType(Enum):
    DELIVERY = "DELIVERY"
    CARRYFORWARD = "CARRYFORWARD"
    MARGIN = "MARGIN"
    INTRADAY = "INTRADAY"
    BO = "BO"


class Duration(Enum):
    DAY = "DAY"
    IOC = "IOC"


class Exchange(Enum):
    BSE = "BSE"
    NSE = "NSE"
    NFO = "NFO"
    MCX = "MCX"


class OrderParams(Enum):
    VARIETY = "variety"
    TRADINGSYMBOL = "tradingsymbol"
    SYMBOLTOKEN = "symboltoken"
    TRANSACTIONTYPE = "transactiontype"
    EXCHANGE_NSE = "NSE"
    EXCHANGE_BSE = "BSE"
    ORDERTYPE = "ordertype"
    PRODUCTTYPE = "producttype"
    DURATION = "duration"
    PRICE = "price"
    SQUAREOFF = "squareoff"
    STOPLOSS = "stoploss"
    QUANTITY = "quantity"
