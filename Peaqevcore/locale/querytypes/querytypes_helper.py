from ast import Raise
from enum import Enum
from datetime import date, datetime, time
from dataclasses import dataclass

class Dividents(Enum):
    AND = 1
    OR = 2


class QueryService:
    DT = datetime.now()
    def __init__(self, args:dict = {}):
        self._settings = args
    
    def should_register_peak(self, dt:datetime) -> bool:
        if len(self._settings) == 0: 
            return True
        DT = dt
        mainret = []
        for s in self._settings:
            groupret = []
            for a in s["args"]:
                groupret.append(QueryService.datepart(a["type"], a["dttype"], a["values"]))
            if s["divident"] is Dividents.AND:
                print("hehej")
                print(groupret)
                mainret.append(all(groupret))
            else:
                mainret.append(any(groupret))
        return any(mainret)

    # @staticmethod
    # def group(divident: Dividents, *contents: list[object]) -> bool:
    #     if divident is Dividents.AND:
    #         return all(contents)
    #     else:
    #         return any(contents)

    @staticmethod
    def datepart(logic: str, dtpart: str, args: list[int]) -> bool:
        _arg = args if len(args) > 1 else args[0]
        _logic = QueryService.LOGIC[logic](
            QueryService.DATETIMEPARTS[dtpart](QueryService.DT), 
            _arg
            )
        return _logic

    AND = "AND"
    OR = "OR"
    LOGIC = {
        "eq": lambda a, dtp : dtp == a,
        "lt": lambda a, dtp : a < dtp,
        "gt": lambda a, dtp : a > dtp,
        "not": lambda a, dtp : dtp != a,
        "lteq": lambda a, dtp : a <= dtp,
        "gteq": lambda a, dtp : a >= dtp,
        "in": lambda a, dtp : a in dtp
    }
    DATETIMEPARTS = {
        "weekday": lambda d : d.weekday(),
        "month":  lambda d : d.month,
        "hour":  lambda d : d.hour,
    }

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
    queryservice: QueryService

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


# QueryService.MOCKDT = datetime(2022, 5, 11, 18,10,0)
# # test = QueryService(
# #                     QueryService.group(
# #                         Dividents.AND,
# #                         QueryService.datepart("gteq", "hour", 7),
# #                         QueryService.datepart("lteq", "hour", 18),
# #                         QueryService.datepart("lteq", "weekday", 4)
# #                         )
# #                     )

# test2 =  QueryService(
#                         QueryService.group(
#                             Dividents.AND,
#                             QueryService.datepart("lteq", "weekday", 4),
#                             QueryService.datepart("in", "hour", 7, 8, 9, 10, 11, 12, 13, 14, 15, 16),
#                             QueryService.datepart("in", "month", 12, 1, 2, 3)
#                         ),
#                         QueryService.group(
#                             Dividents.OR,
#                             QueryService.datepart("in", "month", 4, 5, 6, 7, 8, 9, 10, 11)
#                     )
#                 )

# #print(f" test: {test.should_register_peak}")
# print(f" test2: {test2.should_register_peak}")
# print(QueryService.MOCKDT)
# print(QueryService.MOCKDT.weekday())
# print(QueryService.MOCKDT.month)
# print(QueryService.MOCKDT.hour)





