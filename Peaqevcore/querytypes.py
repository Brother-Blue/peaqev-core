from datetime import datetime
from enum import Enum
from dataclasses import dataclass

"""Peak querytypes"""
QUERYTYPE_BASICMAX = "BasicMax"
QUERYTYPE_AVERAGEOFTHREEDAYS = "AverageOfThreeDays"
QUERYTYPE_AVERAGEOFTHREEHOURS = "AverageOfThreeHours"
QUERYTYPE_AVERAGEOFTHREEDAYS_MIN = "AverageOfThreeDays_Min"
QUERYTYPE_AVERAGEOFTHREEHOURS_MIN = "AverageOfThreeHours_Min"
QUERYTYPE_AVERAGEOFFIVEDAYS = "AverageOfFiveDays"
QUERYTYPE_AVERAGEOFFIVEDAYS_MIN = "AverageOfFiveDays_Min"
QUERYTYPE_HIGHLOAD = "HighLoad"
QUERYTYPE_AVERAGEOFTHREEHOURS_MON_FRI_07_19 = "sala"
QUERYTYPE_AVERAGEOFTHREEHOURS_MON_FRI_07_19_MIN = "sala"
QUERYTYPE_MAX_NOV_MAR_MON_FRI_06_22 = "skövde"
QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR = "kristinehamn"
QUERYTYPE_SOLLENTUNA = "sollentuna"
QUERYTYPE_SOLLENTUNA_MIN = "sollentuna_min"

"""Misc"""
QUARTER_HOURLY = "quarter-hourly"
HOURLY = "hourly"

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


@dataclass
class PeaksModel:
    p: dict
    m:int = 0

    def set_init_dict(self, dict_data):
        self.p = dict_data["p"]
        self.m = dict_data["m"]

class LocaleQuery:
    def __init__(
        self, 
        sumtype: SumTypes, 
        timecalc: TimePeriods, 
        cycle: TimePeriods, 
        sumcounter: SumCounter = None
        ) -> None:    
        self._peaks:PeaksModel = PeaksModel({})
        self._props = QueryProperties(
            sumtype, 
            timecalc, 
            cycle
            )
        self._sumcounter:SumCounter= sumcounter
        self._observed_peak_value:float = 0 
        self._charged_peak_value:float = 0

    @property
    def sumcounter(self) -> SumCounter:
        if self._sumcounter is not None:
            return self._sumcounter
        return SumCounter()

    @property
    def charged_peak(self) -> float: 
        return self._charged_peak_value

    @charged_peak.setter
    def charged_peak(self, val):
        self._charged_peak_value = val

    @property
    def observed_peak(self) -> float: 
        return self.charged_peak if self._props.sumtype is SumTypes.Max else self._observed_peak_value

    @observed_peak.setter
    def observed_peak(self, val):
        self._observed_peak_value = val

    def try_update(self, newval, dt = datetime.now()):
        _dt = (dt.day, dt.hour)
        if len(self._peaks.p) == 0:
            """first addition for this month"""
            self._peaks.p[_dt] = newval
            self._peaks.m = dt.month
        elif dt.month != self._peaks.m:
            """new month, reset"""
            self.reset_values(newval, dt)
        elif _dt in self._peaks.p.keys():
            self._set_update_for_groupby(newval, _dt)
        elif newval > min(self._peaks.p.values()):
            self._peaks.p[_dt] = newval
        elif len(self._peaks.p) < self.sumcounter.counter:
            self._peaks.p[_dt] = newval

        if len(self._peaks.p) > self.sumcounter.counter:
                self._peaks.p.pop(min(self._peaks.p, key=self._peaks.p.get))
        self._update_peaks()

    def _set_update_for_groupby(self, newval, _dt):
        if self.sumcounter.groupby in [TimePeriods.Daily, TimePeriods.UnSet]:
            _datekey = [k for k,v in self._peaks.p.items() if _dt[0] in k][0]
            if newval > self._peaks.p[_datekey]:
                    self._peaks.p.pop(_datekey)
                    self._peaks.p[_dt] = newval
        elif self.sumcounter.groupby is TimePeriods.Hourly:
            if newval > self._peaks.p[_dt]:
                    self._peaks.p[_dt] = newval

    def _update_peaks(self):
        if self._props.sumtype is SumTypes.Max:
            self.charged_peak = max(self._peaks.p.values())
        elif self._props.sumtype is SumTypes.Avg:
            self.observed_peak = min(self._peaks.p.values())
            self.charged_peak = sum(self._peaks.p.values()) / len(self._peaks.p)

    def reset_values(self, newval, dt):
        self._peaks.p.clear()
        self.try_update(newval, dt)

QUERYTYPES = {
    QUERYTYPE_AVERAGEOFTHREEHOURS: LocaleQuery(sumtype=SumTypes.Avg, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sumcounter=SumCounter(counter=3, groupby=TimePeriods.Hourly)),
    QUERYTYPE_AVERAGEOFTHREEDAYS: LocaleQuery(sumtype=SumTypes.Avg, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sumcounter=SumCounter(counter=3, groupby=TimePeriods.Daily)),
    QUERYTYPE_BASICMAX: LocaleQuery(sumtype=SumTypes.Max, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly)
}
