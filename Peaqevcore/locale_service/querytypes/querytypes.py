from datetime import date, datetime, time
import logging

from .const import (
    QUERYTYPE_AVERAGEOFTHREEHOURS,
    QUERYTYPE_AVERAGEOFTHREEDAYS,
    QUERYTYPE_AVERAGEOFTHREEHOURS_MON_FRI_07_19,
    QUERYTYPE_BASICMAX,
    QUERYTYPE_AVERAGEOFFIVEDAYS,
    QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR,
    QUERYTYPE_HIGHLOAD,
    QUERYTYPE_MAX_NOV_MAR_MON_FRI_06_22,
    QUERYTYPE_SOLLENTUNA
    )
from .queryservice import QueryService
from .models.peaks_model import PeaksModel
from .models.enums import SumTypes, TimePeriods
from .models.sumcounter import SumCounter
from .models.queryproperties import QueryProperties

from .querysets import QUERYSETS

_LOGGER = logging.getLogger(__name__)


class LocaleQuery:
    def __init__(
        self, 
        sum_type: SumTypes, 
        time_calc: TimePeriods, 
        cycle: TimePeriods, 
        sum_counter: SumCounter = None,
        query_service: QueryService = QueryService()
        ) -> None:    
        self._peaks: PeaksModel = PeaksModel({})
        self._props = QueryProperties(
            sum_type, 
            time_calc, 
            cycle,
            query_service
            )
        self._sum_counter: SumCounter= sum_counter
        self._observed_peak_value: float = 0 
        self._charged_peak_value: float = 0

    def reset(self) -> None:
        self._peaks.reset()
        self._observed_peak_value = 0
        self._charged_peak_value = 0

    @property
    def peaks_export(self) -> dict:
        ppdict = {}
        for pp in self._peaks.p:
            ppkey = f"{pp[0]}h{pp[1]}"
            ppdict[ppkey] = self._peaks.p.get(pp)
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
    def sum_counter(self) -> SumCounter:
        if self._sum_counter is not None:
            return self._sum_counter
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

    def try_update(self, new_val, timestamp: datetime=datetime.now()):
        if self._props.queryservice.should_register_peak(dt=timestamp) is False:
            return
        if self.peaks.is_dirty:
            self._sanitize_values()
        _dt = (timestamp.day, timestamp.hour)
        if len(self.peaks.p) == 0:
            """first addition for this month"""
            self._peaks.p[_dt] = new_val
            self._peaks.m = timestamp.month
        elif timestamp.month != self._peaks.m:
            """new month, reset"""
            self.reset_values(new_val, timestamp)
        else:
            self._set_update_for_groupby(new_val, _dt)
        if len(self.peaks.p) > self.sum_counter.counter:
                self.peaks.p.pop(min(self.peaks.p, key=self._peaks.p.get))
        self._update_peaks()

    def _set_update_for_groupby(self, new_val, dt):
        if self.sum_counter.groupby in [TimePeriods.Daily, TimePeriods.UnSet]:
            _datekeys = [k for k,v in self.peaks.p.items() if dt[0] in k]
            if len(_datekeys) > 0:
                if new_val > self.peaks.p[_datekeys[0]]:
                        self.peaks.p.pop(_datekeys[0])
                        self.peaks.p[dt] = new_val
            else:
                self.peaks.p[dt] = new_val
        elif self.sum_counter.groupby == TimePeriods.Hourly:
            if dt in self._peaks.p.keys():
                if new_val > self.peaks.p.get(dt):
                        self.peaks.p[dt] = new_val
            else:
                self.peaks.p[dt] = new_val

    def _update_peaks(self):
        if self._props.sumtype is SumTypes.Max:
            self.charged_peak = max(self._peaks.p.values())
        elif self._props.sumtype is SumTypes.Avg:
            self.observed_peak = min(self._peaks.p.values())
            self.charged_peak = sum(self._peaks.p.values()) / len(self._peaks.p)

    def reset_values(self, new_val, dt = datetime.now()):
        self._peaks.p.clear()
        self.try_update(new_val, dt)

    def _sanitize_values(self):
        countX = lambda arr, x: len([a for a in arr if a[0] == x])
        # def countX(lst, x):
        #     for ele in lst:
        #         if ele[0] == x:
        #             count = count + 1
        #     return count
        if self.sum_counter.groupby == TimePeriods.Daily:
            duplicates = {}
            for k in self._peaks.p.keys():
                if countX(self._peaks.p.keys(), k[0]) > 1:
                    duplicates[k] = self._peaks.p.get(k)
            if duplicates:
                minkey = min(duplicates, key=duplicates.get)
                self._peaks.p.pop(minkey)
                    
        while len(self._peaks.p) > self.sum_counter.counter:
            self._peaks.p.pop(min(self._peaks.p, key=self._peaks.p.get))
        self._peaks.is_dirty = False
        self._update_peaks()

QUERYTYPES = {
    QUERYTYPE_AVERAGEOFTHREEHOURS: LocaleQuery(sum_type=SumTypes.Avg, time_calc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sum_counter=SumCounter(counter=3, groupby=TimePeriods.Hourly)),
    QUERYTYPE_AVERAGEOFTHREEDAYS: LocaleQuery(sum_type=SumTypes.Avg, time_calc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sum_counter=SumCounter(counter=3, groupby=TimePeriods.Daily)),
    QUERYTYPE_BASICMAX: LocaleQuery(sum_type=SumTypes.Max, time_calc=TimePeriods.Hourly, cycle=TimePeriods.Monthly),
    QUERYTYPE_AVERAGEOFFIVEDAYS: LocaleQuery(sum_type=SumTypes.Avg, time_calc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sum_counter=SumCounter(counter=5, groupby=TimePeriods.Daily)),
    QUERYTYPE_SOLLENTUNA: LocaleQuery(sum_type=SumTypes.Avg, time_calc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sum_counter=SumCounter(counter=3, groupby=TimePeriods.Hourly), query_service=QueryService(QUERYSETS[QUERYTYPE_SOLLENTUNA])),
    QUERYTYPE_MAX_NOV_MAR_MON_FRI_06_22: LocaleQuery(sum_type=SumTypes.Max, time_calc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, query_service=QueryService(QUERYSETS[QUERYTYPE_MAX_NOV_MAR_MON_FRI_06_22])),
    QUERYTYPE_AVERAGEOFTHREEHOURS_MON_FRI_07_19: LocaleQuery(sum_type=SumTypes.Avg, time_calc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sum_counter=SumCounter(counter=3, groupby=TimePeriods.Hourly), query_service=QueryService(QUERYSETS[QUERYTYPE_AVERAGEOFTHREEHOURS_MON_FRI_07_19])),
    QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR: LocaleQuery(sum_type=SumTypes.Max, time_calc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, query_service=QueryService(QUERYSETS[QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR])),
    QUERYTYPE_HIGHLOAD: LocaleQuery(sum_type=SumTypes.Max, time_calc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, query_service=QueryService(QUERYSETS[QUERYTYPE_HIGHLOAD]))
}
