import collections
from operator import mod
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

    def update(self, test_hour: int=None):
        hours_today = self._update_internal(self.prices)
        hours_tomorrow = self._update_internal(self.prices_tomorrow)
        hour = datetime.now().hour if test_hour is None else test_hour

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
            price_dict = self._create_dict(prices)
            normalized_price_dict = self._create_dict(self._normalize_prices(prices))
            
            """
            Curve is too flat if stdev is <= 0.05. 
            If so we don't do any specific non or caution-hours based on pricing.
            """
            if stat.stdev(prices) > 0.05:
                prices_ranked = self._rank_prices(price_dict, normalized_price_dict)
                ready_hours = self._determine_hours(prices_ranked, prices)
            else:
                ready_hours = ret
            if self._absolute_top_price is not None:
                ret = self._add_expensive_non_hours(price_dict, ready_hours)
            else: 
                ret = ready_hours
            if self._min_price > 0:
                ret = self._remove_cheap_hours(price_dict, ret)
        return ret
        
    def _normalize_prices(self, prices) -> list:
        min_price = min(prices)
        ret = []
        for p in prices:
            ret.append(p/min_price)
        return ret

    def _remove_cheap_hours(self, hour_dict: dict, cheap_hours: HourObject) -> HourObject:
        hours = (hour for hour in hour_dict if hour_dict.get(hour) is not None and hour_dict.get(hour) < self._min_price)
        for hour in hours:
            if hour in cheap_hours.nh:
                cheap_hours.nh.remove(hour)
            elif hour in cheap_hours.ch:
                cheap_hours.ch.remove(cheap_hours.dyn_ch.pop(hour))
        return cheap_hours

    def _add_expensive_non_hours(self, hour_dict: dict, ready_hours: HourObject) -> HourObject:
        hours = (hour for hour in hour_dict if hour_dict.get(hour) is not None and hour_dict.get(hour) >= self._absolute_top_price)
        for hour in hours:
            if hour not in ready_hours.nh:
                ready_hours.nh.append(hour)
                if hour in ready_hours.ch:
                    ready_hours.ch.remove(hour)
                if hour in ready_hours.dyn_ch.keys():
                    ready_hours.dyn_ch.pop(hour)
        ready_hours.nh.sort()
        return ready_hours

    def _rank_prices(self, hour_dict: dict, normalized_hour_dict: dict) -> dict:
        ret = {}
        maxval = max(hour_dict.values())
        minval = min(hour_dict.values())
        max_normalized = max(normalized_hour_dict.values())
        peaq_stdev = maxval/abs(max_normalized/stat.stdev(normalized_hour_dict.values()))
        if peaq_stdev < minval:
            peaq_stdev = peaq_stdev + minval
        for key in hour_dict:
            if hour_dict.get(key) > peaq_stdev:
                _permax = round(hour_dict[key] / maxval, 2)
                ret[key] = {"val": hour_dict[key], "permax": _permax}
        return self._discard_excessive_hours(ret)

    def _discard_excessive_hours(self, hours: dict):
        """There should always be at least four regular hours before absolute_top_price kicks in."""
        if len(hours) < 20:
            return hours
        while len(hours) >= 20:
            to_pop = dict(sorted(hours.items(), key=lambda _, value: value.get('val')))    
            hours.pop(to_pop.keys()[0])
        return hours

    def _create_dict(self, arr_input: list):
        ret = {idx: val for idx, val in enumerate(arr_input)}
        try:
            assert len(ret) == 24
        except Exception:
            raise ValueError
        return ret

    def _determine_hours(self, price_list: dict, prices: list) -> HourObject:
        nh = []
        dyn_ch = {}
        ch = []
        for p in price_list:
            per_max = round(abs(price_list.get(p).get("permax") - 1), 2)
            if self._cautionhour_type == CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE]:
                per_max += 0.15
            elif self._cautionhour_type == CAUTIONHOURTYPE[CAUTIONHOURTYPE_INTERMEDIATE]:
                per_max += 0.05
            if float(price_list.get(p).get("permax")) <= self._cautionhour_type or \
               float(price_list.get(p).get("val")) <= (sum(prices)/len(prices)):
                ch.append(p)
                dyn_ch[p] = round(per_max,2)
            else:
                nh.append(p)
        return HourObject(nh, ch, dyn_ch)
    
    def _convert_none_list(self, lst: list) -> list:
        try:
            ret = []
            for l in lst:
                if l is None:
                    return ret
            return lst
        except:
            return self._make_array_from_empty(lst)

    def _make_array_from_empty(self, arr_input) -> list:
        arr = [p for p in arr_input.split(",") if len(p) > 0]
        ret = []
        if len(arr) > 24:
            try:
                for l in arr:
                    parsed_item = Hoursselectionbase._try_parse(l, float)
                    if not parsed_item:
                        parsed_item = Hoursselectionbase._try_parse(l, int)
                    assert type(parsed_item) is float or type(parsed_item) is int
                    ret.append(parsed_item)
                return ret
            except ValueError:
                return []
        return []

    def get_average_kwh_price(self, test_hour: int=None):
        hour = datetime.now().hour if test_hour is None else test_hour
        ret = {}

        def _looper(_hour: int):
            if _hour in self._dynamic_caution_hours:
                    if self._prices_tomorrow is not None:
                        if _hour < hour:
                            ret[_hour] = self._dynamic_caution_hours.get(_hour) * self._prices_tomorrow[_hour]
                    if _hour >= hour:
                        ret[_hour] = self._dynamic_caution_hours.get(_hour) * self._prices[_hour]
            elif _hour not in self._non_hours:
                ret[_hour] = self._prices_tomorrow[_hour] \
                    if _hour < hour and self._prices_tomorrow \
                    else self._prices[_hour]

        if self.prices_tomorrow is None:
            for h in range(hour, 24):
                _looper(h)
        else:
            for h in range(hour, (hour+24)):
                h = h % 24
                _looper(h)
        
        return round(sum(ret.values())/len(ret), 2)
        
    def get_total_charge(self, current_peak:float, test_hour:int = None) -> float:
        hour = datetime.now().hour if test_hour is None else test_hour
        ret = {}

        def _looper(_hour: int):
            if _hour in self._dynamic_caution_hours:
                    ret[_hour] = self._dynamic_caution_hours.get(_hour) * current_peak
            elif _hour in self._non_hours:
                ret[_hour] = 0
            else:
                ret[_hour] = current_peak

        if self.prices_tomorrow is None:
            for h in range(hour, 24):
                _looper(h)
        else:
            for h in range(hour, (hour+24)):
                h = h % 24
                _looper(h)
        
        return round(sum(ret.values()), 1)

    @staticmethod
    def _try_parse(val: str, parse_type: type):
        try:
            ret = parse_type(val)
            return ret
        except ValueError:
            return False
