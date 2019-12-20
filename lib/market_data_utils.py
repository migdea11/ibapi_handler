import enum


class MarketDataType(enum.Enum):
    REAL_TIME = 1
    FROZEN = 2
    DELAYED = 3
    DELAYED_FROZEN = 4
