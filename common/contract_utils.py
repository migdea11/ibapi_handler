import enum


class SecurityType(enum.Enum):
    """
    The security's type:
    STK - stock (or ETF)
    OPT - option
    FUT - future
    IND - index
    FOP - futures option
    CASH - forex pair
    BAG - combo
    WAR - warrant
    BOND- bond
    CMDTY- commodity
    NEWS- news
    FUND- mutual fund
    """
    STOCK = 'STK'
    OPTION = 'OPT'
    FUTURE = 'FUT'
    INDEX = 'IND'
    # TODO finish the rest


class OptionRight(enum.Enum):
    CALL = 'CALL'
    PUT = 'PUT'
