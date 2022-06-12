from enum import Enum

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

class Dividents(Enum):
    AND = 1
    OR = 2

def between_hours(fromhour: int, tohour: int):
    pass

def between_months(frommonth: int, tomonth: int):
    pass

def group(*contents: any):
    pass

class SumCounter:
    def __init__(self, counter: int = 1, groupby: TimePeriods = None):
        self._counter = counter
        self._groupby = groupby

    @property
    def counter(self) -> int:
        return self._counter
    
    @property
    def grouper(self) -> TimePeriods|None:
        return self._groupby

class query:
    def __init__(self, sumtype: SumTypes, timecalc: TimePeriods, cycle: TimePeriods):    
        self._sumtype = sumtype
        self._timecalc = timecalc
        self._cycle = cycle
        self._sumcounter: SumCounter

    @property
    def sumtype(self) -> SumTypes:
        return self._sumtype

    @property
    def timecalc(self) -> TimePeriods:
        return self._timecalc

    @property
    def cycle(self) -> TimePeriods:
        return self._cycle

    @property
    def sumcounter(self) -> SumCounter|None:
        return self._sumcounter

    @sumcounter.setter
    def sumcounter(self, val):
        self._sumcounter = val


#partille
partille = query(sumtype=SumTypes.Max, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly)
#partille

#goteborg_avg
goteborg_avg = query(sumtype=SumTypes.Avg, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly)
goteborg_avg.sumcounter = SumCounter(3, TimePeriods.Daily)
#goteborg_avg

#goteborg_min
goteborg_min = query(sumtype=SumTypes.Min, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly)
goteborg_min.sumcounter = SumCounter(counter=3, groupby=TimePeriods.Daily)
#goteborg_min






# class sql:
#     @staticmethod
#     def query(prefix: str, suffix: str, *params: str):
#         paramret = ""
#         for p in params:
#             paramret = paramret+p
#         return prefix+paramret+suffix

#     @staticmethod
#     def group(*contents: str) -> str:
#         ret = ""
#         for c in contents:
#             ret += c
#         return f"({ret})"

#     AND = " AND "
#     OR = " OR "
#     DIVIDENTS = {
#         "eq": "= ",
#         "lt": "< ",
#         "gt": "> ",
#         "not": "<> ",
#         "lteq": "<= ",
#         "gteq": ">= ",
#         "in": "IN "
#     }

#     DATETIMEPARTS = {
#         "weekday": "w",
#         "month": "m",
#         "hour": "H"
#     }

#     @staticmethod
#     def datepart(divident: str, dtpart: str, *args: int) -> str:
#         _base = sql._strftime_base(sql.DATETIMEPARTS[dtpart])
#         _arg = str(args) if len(args) > 1 else str(args[0])
#         _divident = sql.DIVIDENTS[divident]
#         return _base + _divident + _arg

#     @staticmethod
#     def _strftime_base(time_type: str) -> str:
#         return f"cast(strftime(\'%{time_type}\', start) as int) "