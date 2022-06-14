from enum import Enum
from datetime import date, datetime, time
from dataclasses import dataclass
from .const import QUERYTYPE_SOLLENTUNA


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

@dataclass(frozen=True)
class SumCounter:
    counter:int = 1
    groupby: TimePeriods = TimePeriods.UnSet

@dataclass(frozen=True)
class QueryProperties:
    sumtype: SumTypes
    timecalc:TimePeriods
    cycle: TimePeriods
    queryparams: QueryExtension

@dataclass
class PeaksModel:
    p: dict
    m:int = 0
    is_dirty:bool = False

    def set_init_dict(self, dict_data, dt = datetime.now()):
        if dt.month == self.m:
            ppdict = {}
            for pp in dict_data["p"]:
                tkeys = pp.split("h")
                ppkey = (int(tkeys[0]), int(tkeys[1]))
                ppdict[ppkey] = dict_data["p"][pp]
            if len(self.p) > 0:
                ppdict = self.p | ppdict
            self.p = ppdict
            self.m = dict_data["m"]
            self.is_dirty = True

    def reset(self) -> None:
        self.m = 0
        self.is_dirty = False
        self.p = {}

QUERYSETS = {
    QUERYTYPE_SOLLENTUNA: 
                QueryService.query(
                    QueryService.AND,
                    QueryService.datepart("gteq", "hour", 7),
                    QueryService.AND,
                    QueryService.datepart("lteq", "hour", 18),
                    QueryService.AND,
                    QueryService.datepart("lteq", "weekday", 4)
                )
}