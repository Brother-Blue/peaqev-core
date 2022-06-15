from datetime import date, datetime, time
import logging

from .const import (
    QUERYTYPE_AVERAGEOFTHREEHOURS,
    QUERYTYPE_AVERAGEOFTHREEDAYS,
    QUERYTYPE_BASICMAX,
    QUERYTYPE_AVERAGEOFFIVEDAYS,
    QUERYTYPE_SOLLENTUNA
    )
from .querytypes_helper import (
    QueryService, 
    QueryProperties, 
    SumTypes, 
    TimePeriods,  
    SumCounter, 
    PeaksModel
    )

from .querysets import QUERYSETS

_LOGGER = logging.getLogger(__name__)


class LocaleQuery:
    def __init__(
        self, 
        sumtype: SumTypes, 
        timecalc: TimePeriods, 
        cycle: TimePeriods, 
        sumcounter: SumCounter = None,
        queryparams: QueryService = None
        ) -> None:    
        self._peaks:PeaksModel = PeaksModel({})
        self._props = QueryProperties(
            sumtype, 
            timecalc, 
            cycle,
            queryparams
            )
        self._sumcounter:SumCounter= sumcounter
        self._observed_peak_value:float = 0 
        self._charged_peak_value:float = 0

    def reset(self) -> None:
        self._peaks.reset()
        self._observed_peak_value = 0
        self._charged_peak_value = 0

    @property
    def peaks_export(self) -> dict:
        ppdict = {}
        for pp in self._peaks.p:
            ppkey = str(str(pp[0]) + "h" + str(pp[1]))
            ppdict[ppkey] = self._peaks.p[pp]
        return {
            "m": self._peaks.m,
            "p": ppdict
        }

    @property
    def peaks(self) -> PeaksModel:
        if self._peaks.is_dirty:
            self._sanitize_values()
        return self._peaks

    @property
    def sumcounter(self) -> SumCounter:
        if self._sumcounter is not None:
            return self._sumcounter
        return SumCounter()

    @property
    def charged_peak(self) -> float: 
        if self._peaks.is_dirty:
            self._sanitize_values()
        ret = self._charged_peak_value
        return round(ret,2)

    @charged_peak.setter
    def charged_peak(self, val):
        self._charged_peak_value = val

    @property
    def observed_peak(self) -> float: 
        if self._peaks.is_dirty:
            self._sanitize_values()
        ret = self.charged_peak if self._props.sumtype is SumTypes.Max else self._observed_peak_value
        return round(ret, 2)

    @observed_peak.setter
    def observed_peak(self, val):
        self._observed_peak_value = val

    def try_update(self, newval, dt = datetime.now()):
        if self.peaks.is_dirty:
            self._sanitize_values()
        _dt = (dt.day, dt.hour)
        if len(self.peaks.p) == 0:
            """first addition for this month"""
            self._peaks.p[_dt] = newval
            self._peaks.m = dt.month
        elif dt.month != self._peaks.m:
            """new month, reset"""
            self.reset_values(newval, dt)
        else:
            self._set_update_for_groupby(newval, _dt)
        if len(self.peaks.p) > self.sumcounter.counter:
                self.peaks.p.pop(min(self.peaks.p, key=self._peaks.p.get))
        self._update_peaks()

    def _set_update_for_groupby(self, newval, _dt):
        if self.sumcounter.groupby in [TimePeriods.Daily, TimePeriods.UnSet]:
            _datekey = [k for k,v in self.peaks.p.items() if _dt[0] in k]
            if len(_datekey) > 0:
                if newval > self.peaks.p[_datekey[0]]:
                        self.peaks.p.pop(_datekey[0])
                        self.peaks.p[_dt] = newval
            else:
                self.peaks.p[_dt] = newval
        elif self.sumcounter.groupby == TimePeriods.Hourly:
            if _dt in self._peaks.p.keys():
                if newval > self.peaks.p[_dt]:
                        self.peaks.p[_dt] = newval
            else:
                self.peaks.p[_dt] = newval

    def _update_peaks(self):
        if self._props.sumtype is SumTypes.Max:
            self.charged_peak = max(self._peaks.p.values())
        elif self._props.sumtype is SumTypes.Avg:
            self.observed_peak = min(self._peaks.p.values())
            self.charged_peak = sum(self._peaks.p.values()) / len(self._peaks.p)

    def reset_values(self, newval, dt = datetime.now()):
        self._peaks.p.clear()
        self.try_update(newval, dt)

    def _sanitize_values(self):
        def countX(lst, x):
            count = 0
            for ele in lst:
                if ele[0] == x:
                    count = count + 1
            return count
        if self.sumcounter.groupby == TimePeriods.Daily:
            duplicates = {}
            for k in self._peaks.p.keys():
                if countX(self._peaks.p.keys(), k[0]) > 1:
                    duplicates[k] = self._peaks.p[k]
            if len(duplicates) > 0:
                minkey = min(duplicates, key=duplicates.get)
                self._peaks.p.pop(minkey)
                    
        while len(self._peaks.p) > self.sumcounter.counter:
            self._peaks.p.pop(min(self._peaks.p, key=self._peaks.p.get))
        self._peaks.is_dirty = False
        self._update_peaks()

QUERYTYPES = {
    QUERYTYPE_AVERAGEOFTHREEHOURS: LocaleQuery(sumtype=SumTypes.Avg, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sumcounter=SumCounter(counter=3, groupby=TimePeriods.Hourly)),
    QUERYTYPE_AVERAGEOFTHREEDAYS: LocaleQuery(sumtype=SumTypes.Avg, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sumcounter=SumCounter(counter=3, groupby=TimePeriods.Daily)),
    QUERYTYPE_BASICMAX: LocaleQuery(sumtype=SumTypes.Max, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly),
    QUERYTYPE_AVERAGEOFFIVEDAYS: LocaleQuery(sumtype=SumTypes.Avg, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sumcounter=SumCounter(counter=5, groupby=TimePeriods.Daily)),
    QUERYTYPE_SOLLENTUNA: LocaleQuery(sumtype=SumTypes.Avg, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sumcounter=SumCounter(counter=3, groupby=TimePeriods.Hourly), queryparams=QUERYSETS[QUERYTYPE_SOLLENTUNA])
}


