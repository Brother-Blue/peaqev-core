from enum import Enum
from datetime import date, datetime, time
from dataclasses import dataclass

@dataclass
class QueryHelper:
    #the following logic is a must to count a specific timing as peak
    pass


class QueryService:
    @staticmethod
    def is_in_schema() -> bool:
        pass

    @staticmethod
    def query(*params: str):
        paramret = ""
        for p in params:
            paramret = paramret+p
        return paramret

    @staticmethod
    #todo make groups be either and or or)
    def group(*contents: str) -> str:
        ret = ""
        for c in contents:
            ret += c
        return f"({ret})"

    AND = "AND"
    OR = "OR"

    DIVIDERS = {
        AND: lambda a, b : a == b,
        OR: lambda a, b : a == b
    }

    LOGIC = {
        "eq": lambda a, dtp : dtp == a,
        "lt": lambda a, dtp : dtp < a,
        "gt": lambda a, dtp : dtp > a,
        "not": lambda a, dtp : dtp != a,
        "lteq": lambda a, dtp : dtp <= a,
        "gteq": lambda a, dtp : dtp >= a,
        "in": lambda a, dtp : dtp in a
    }

    DATETIMEPARTS = {
        "weekday": lambda d : d.weekday(),
        "month":  lambda d : d.month,
        "hour":  lambda d : d.hour,
    }

    @staticmethod
    def datepart(divident: str, dtpart: str, *args: int) -> str:
        _base = QueryService._strftime_base(QueryService.DATETIMEPARTS[dtpart])
        _arg = str(args) if len(args) > 1 else str(args[0])
        _divident = QueryService.LOGIC[divident]
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
    queryparams: QueryHelper

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



# test = QueryService.query(
#                     QueryService.AND,
#                     QueryService.datepart("gteq", "hour", 7),
#                     QueryService.AND,
#                     QueryService.datepart("lteq", "hour", 18),
#                     QueryService.AND,
#                     QueryService.datepart("lteq", "weekday", 4)
#                 )
#print(test)


# test = QueryService.query(
#                     QueryService.groupAND(
#                     QueryService.datepart("gteq", "hour", 7),
#                     QueryService.datepart("lteq", "hour", 18),
#                     QueryService.datepart("lteq", "weekday", 4)
#                     )
#                 )
print(QueryService.LOGIC["in"](datetime.now().year, [2022]))
print(QueryService.DATETIMEPARTS["month"](datetime.now()))
