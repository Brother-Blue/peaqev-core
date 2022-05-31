import collections
import statistics as stat
from datetime import datetime
from .Models import (
    CAUTIONHOURTYPE_SUAVE,
    CAUTIONHOURTYPE_INTERMEDIATE,
    CAUTIONHOURTYPE_AGGRESSIVE,
    CAUTIONHOURTYPE
)


class HourObject:
    def __init__(self, nh:list, ch:list, dyn_ch:dict = {}) -> None:    
        self._nh = nh
        self._ch = ch
        self._dyn_ch = dyn_ch

    @property
    def nh(self) -> list:
        return self._nh
    
    @property
    def ch(self) -> list:
        return self._ch

    @property
    def dyn_ch(self) -> dict:
        return self._dyn_ch


class Hoursselectionbase:
    def __init__(
            self,      
            absolute_top_price: float = 0,
            min_price: float = 0,
            cautionhour_type: float = CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE]
    ):
        self._prices = None
        self._prices_tomorrow = None
        self._non_hours = []
        self._caution_hours = []
        self._dynamic_caution_hours = {}
        self._absolute_top_price = self._set_absolute_top_price(absolute_top_price)
        self._min_price = min_price
        self._cautionhour_type = cautionhour_type
        self._validate()
    
    def _set_absolute_top_price(self, val) -> float:
        if val is None:
            return float("inf")
        if val <= 0:
            return float("inf")
        return float(val)

    def _validate(self):
        assert 0 < self._cautionhour_type <= 1
        assert len(self._caution_hours) == 0
        assert len(self._non_hours) == 0

    @property
    def non_hours(self):
        return self._non_hours

    @non_hours.setter
    def non_hours(self, val):
        self._non_hours = val

    @property
    def caution_hours(self):
        return self._caution_hours

    @caution_hours.setter
    def caution_hours(self, val):
        self._caution_hours = val

    @property
    def dynamic_caution_hours(self) -> dict:
        return self._dynamic_caution_hours

    @dynamic_caution_hours.setter
    def dynamic_caution_hours(self, val):
        self._dynamic_caution_hours = val

    @property
    def prices(self):
        return self._prices

    @prices.setter
    def prices(self, val):
        self._prices = val
        self.update()

    @property
    def prices_tomorrow(self) -> list:
        return self._prices_tomorrow

    @prices_tomorrow.setter
    def prices_tomorrow(self, val):
        self._prices_tomorrow = self._convert_none_list(val)
        self.update()

    @property
    def absolute_top_price(self) -> float:
        return self._absolute_top_price

    @property
    def min_price(self) -> float:
        return self._min_price

    def update(self, testhour:int = None):
        hours_today = self._update_internal(self.prices)
        hours_tomorrow = self._update_internal(self.prices_tomorrow)
        hour = datetime.now().hour if testhour is None else testhour

        self.non_hours = []
        self.caution_hours = []
        self.dynamic_caution_hours = {}

        self.non_hours.extend(h for h in hours_today.nh if h >= hour)
        self.caution_hours.extend(h for h in hours_today.ch if h >= hour)
        self.non_hours.extend(h for h in hours_tomorrow.nh if h < hour)
        self.caution_hours.extend(h for h in hours_tomorrow.ch if h < hour)

        for h in hours_today.dyn_ch:
            if h >= hour:
                self._dynamic_caution_hours[h] = hours_today.dyn_ch[h]

        for h in hours_tomorrow.dyn_ch:
            if h < hour:
                self._dynamic_caution_hours[h] = hours_tomorrow.dyn_ch[h]

    def _update_internal(self, prices) -> HourObject:
        ret = HourObject([], [], {})
        if prices is not None and len(prices) > 1:
            pricedict = self._create_dict(prices)
            normalized_pricedict = self._create_dict(self._normalize_prices(prices))
            
            """
            Curve is too flat if stdev is <= 0.05. 
            If so we don't do any specific non or caution-hours based on pricing.
            """
            if stat.stdev(prices) > 0.05:
                prices_ranked = self._rank_prices(pricedict, normalized_pricedict)
                ready_hours = self._determine_hours(prices_ranked, prices)
            else:
                ready_hours = ret
            if self._absolute_top_price is not None:
                ret = self._add_expensive_non_hours(pricedict, ready_hours)
            else: 
                ret = ready_hours
            if self._min_price > 0:
                ret = self._remove_cheap_hours(pricedict, ret)
        return ret
        
    def _normalize_prices(self, prices) -> list:
        min_price = min(prices)
        ret = []
        for p in prices:
            ret.append(p/min_price)
        return ret

    def _remove_cheap_hours(self, hourdict: dict, hours: HourObject) -> HourObject:
        lst = (h for h in hourdict if hourdict[h] < self._min_price)
        for h in lst:
            if h in hours.nh:
                hours.nh.remove(h)
            elif h in hours.ch:
                hours.ch.remove(h)
                hours.dyn_ch.pop(h)    
        return hours

    def _add_expensive_non_hours(self, hourdict: dict, readyhours:HourObject) -> HourObject:
        lst = (h for h in hourdict if hourdict[h] >= self._absolute_top_price)
        for h in lst:
            if h not in readyhours.nh:
                readyhours.nh.append(h)
                if h in readyhours.ch:
                    readyhours.ch.remove(h)
                if h in readyhours.dyn_ch.keys():
                    readyhours.dyn_ch.pop(h)
        readyhours.nh.sort()
        return readyhours

    def _rank_prices(self, hourdict: dict, normalized_hourdict: dict) -> dict:
        ret = {}
        _maxval = max(hourdict.values())
        _max_normalized = max(normalized_hourdict.values())
        peaqstdev = _maxval/abs(_max_normalized/stat.stdev(normalized_hourdict.values()))
        if peaqstdev < min(hourdict.values()):
            peaqstdev = peaqstdev + min(hourdict.values())
        for key in hourdict:
            if hourdict[key] > peaqstdev:
                _permax = round(hourdict[key] / _maxval, 2)
                ret[key] = {"val": hourdict[key], "permax": _permax}
        return self._discard_excessive_hours(ret)

    def _discard_excessive_hours(self, hours: dict):
        """There should always be at least four regular hours before absolute_top_price kicks in."""
        if len(hours) < 20:
            return hours
        while len(hours) >= 20:
            to_pop = dict(sorted(hours.items(), key=lambda item: item[1]['val']))    
            hours.pop(list(to_pop.keys())[0])
        return hours

    def _create_dict(self, input: list):
        ret = {}
        for idx, val in enumerate(input):
            ret[idx] = val
        try:
            assert len(ret) == 24
        except Exception:
            raise ValueError
        return ret

    def _determine_hours(self, price_list: dict, prices: list) -> HourObject:
        _nh = []
        _dyn_ch = {}
        _ch = []
        for p in price_list:
            _permax = round(abs(price_list[p]["permax"] - 1), 2)
            if self._cautionhour_type == CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE]:
                _permax += 0.15
            elif self._cautionhour_type == CAUTIONHOURTYPE[CAUTIONHOURTYPE_INTERMEDIATE]:
                _permax += 0.05
            if float(price_list[p]["permax"]) <= self._cautionhour_type:
                _ch.append(p)
                _dyn_ch[p] = round(_permax,2)
            elif float(price_list[p]["val"]) <= (sum(prices)/len(prices)):
                _ch.append(p)
                _dyn_ch[p] = round(_permax,2)
            else:
                _nh.append(p)
        return HourObject(_nh, _ch, _dyn_ch)
    
    def _convert_none_list(self, lst:list) -> list:
        try:
            ret = []
            for l in lst:
                if l is None:
                    return ret
            return lst
        except:
            return self._make_array_from_empty(lst)

    def _make_array_from_empty(self, input) -> list:
        array = input.split(",")
        list = [p for p in array if len(p) > 0]
        ret = []
        if len(list) > 24:
            try:
                for l in list:
                    parsed_item = Hoursselectionbase._try_parse(l, float)
                    if not parsed_item:
                        parsed_item = Hoursselectionbase._try_parse(l, int)
                    assert type(parsed_item) is float or type(parsed_item) is int
                    ret.append(parsed_item)
                return ret
            except:
                return []
        return []

    def get_average_kwh_price(self, testhour:int = None):
        hour = datetime.now().hour if testhour is None else testhour
        ret = {}

        def _looper(h:int):
            if h in self._dynamic_caution_hours:
                    if self._prices_tomorrow is not None and len(self._prices_tomorrow) > 0:
                        if h < hour and len(self._prices_tomorrow) > 0:
                            ret[h] = self._dynamic_caution_hours[h] * self._prices_tomorrow[h]
                    if h >= hour:
                        ret[h] = self._dynamic_caution_hours[h] * self._prices[h]
            elif h not in self._non_hours:
                if h < hour and len(self._prices_tomorrow) > 0:
                    ret[h] = self._prices_tomorrow[h]
                if h >= hour:
                    ret[h] = self._prices[h]

        if self.prices_tomorrow is None:
            for h in range(hour,24):
                _looper(h)
        else:
            for h in range(hour,(hour+24)):
                h = h-24 if h > 23 else h
                _looper(h)
        
        return round(sum(ret.values())/len(ret),2)
        
        
        
        # if len(self._prices) > 0:
        #     hour = datetime.now().hour if testhour is None else testhour
        #     ret = {}

        #     for h in self._dynamic_caution_hours:
        #         if len(self._prices_tomorrow) > 0:
        #             if h < hour and len(self._prices_tomorrow) > 0:
        #                 ret[h] = self._dynamic_caution_hours[h] * self._prices_tomorrow[h]
        #         if h >= hour:
        #             ret[h] = self._dynamic_caution_hours[h] * self._prices[h]

        #     for nh in self._non_hours:
        #         ret[nh] = 0

        #     for i in range(hour,24):
        #         if i not in ret.keys():
        #             if len(self._prices_tomorrow) > 0:
        #                 if i < hour and len(self._prices_tomorrow) > 0:
        #                     ret[i] = self._prices_tomorrow[i]
        #             if i >= hour:
        #                 ret[i] = self._prices[i]

        #     return round(sum(ret.values())/len(ret),2)
        # return "-"

    def get_total_charge(self, currentpeak:float, testhour:int = None) -> float:
        hour = datetime.now().hour if testhour is None else testhour
        ret = {}

        def _looper(h:int):
            if h in self._dynamic_caution_hours:
                    ret[h] = self._dynamic_caution_hours[h] * currentpeak
            elif h in self._non_hours:
                ret[h] = 0
            else:
                ret[h] = currentpeak

        if self.prices_tomorrow is None:
            for h in range(hour,24):
                _looper(h)
        else:
            for h in range(hour,(hour+24)):
                h = h-24 if h > 23 else h
                _looper(h)
        
        return round(sum(ret.values()),1)

    @staticmethod
    def _try_parse(input:str, parsetype:type):
        try:
            ret = parsetype(input)
            return ret
        except:
            return False
