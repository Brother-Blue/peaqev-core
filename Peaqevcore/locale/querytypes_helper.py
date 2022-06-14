from enum import Enum

class QueryExtension:
    pass


class QueryService:
    @staticmethod
    def query(prefix: str, suffix: str, *params: str):
        paramret = ""
        for p in params:
            paramret = paramret+p
        return prefix+paramret+suffix

    @staticmethod
    def group(*contents: str) -> str:
        ret = ""
        for c in contents:
            ret += c
        return f"({ret})"

    AND = " AND "
    OR = " OR "
    DIVIDENTS = {
        "eq": "= ",
        "lt": "< ",
        "gt": "> ",
        "not": "<> ",
        "lteq": "<= ",
        "gteq": ">= ",
        "in": "IN "
    }

    DATETIMEPARTS = {
        "weekday": "w",
        "month": "m",
        "hour": "H"
    }

    @staticmethod
    def datepart(divident: str, dtpart: str, *args: int) -> str:
        _base = QueryService._strftime_base(QueryService.DATETIMEPARTS[dtpart])
        _arg = str(args) if len(args) > 1 else str(args[0])
        _divident = QueryService.DIVIDENTS[divident]
        return _base + _divident + _arg

    @staticmethod
    def _strftime_base(time_type: str) -> str:
        return f"cast(strftime(\'%{time_type}\', start) as int) "

class SumTypes(Enum):
    Max = 1
    Avg = 2
    Min = 3

class TimePeriods(Enum):
    Hourly = 1
    Daily = 2
    Weekly = 3
    BiWeekly = 4
    Monthly = 5
    Yearly = 6
    UnSet = 7