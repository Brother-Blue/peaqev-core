import statistics as stat
from datetime import datetime
from .Models import (
    CAUTIONHOURTYPE_SUAVE,
    CAUTIONHOURTYPE_INTERMEDIATE,
    CAUTIONHOURTYPE_AGGRESSIVE,
    CAUTIONHOURTYPE
)

class HourObject:
    def __init__(self, nh:list, ch:list) -> None:    
        self._nh = nh
        self._ch = ch

    @property
    def nh(self) -> list:
        return self._nh
    
    @property
    def ch(self) -> list:
        return self._ch


class Hoursselectionbase:
    def __init__(
            self,      
            absolute_top_price: float = 0,
            cautionhour_type: float = CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE]
    ):
        self._prices = None
        self._prices_tomorrow = None
        self._non_hours = []
        self._caution_hours = []
        self._absolute_top_price = self._set_absolute_top_price(absolute_top_price)
        self._cautionhour_type = cautionhour_type
        self._validate()
    
    def _set_absolute_top_price(self, val) -> float:
        if val is None:
            return float("inf")
        if val <= 0:
            return float("inf")
        return val

    def _validate(self):
        assert 0 < self._cautionhour_type <= 1
        assert type(self.absolute_top_price) is float
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

    def update(self, testhour:int = None):
        hours_today = self._update_internal(self.prices)
        hours_tomorrow = self._update_internal(self.prices_tomorrow)
        hour = datetime.now().hour if testhour is None else testhour

        self.non_hours = []
        self.caution_hours = []

        for h in hours_today.nh:
            if h >= hour:
                self.non_hours.append(h)

        for h in hours_today.ch:
            if h >= hour:
                self.caution_hours.append(h)

        for h in hours_tomorrow.nh:
            if h < hour:
                self.non_hours.append(h)

        for h in hours_tomorrow.ch:
            if h < hour:
                self.caution_hours.append(h)

    def _update_internal(self, prices) -> HourObject:
        ret = HourObject([], [])
        if prices is not None and len(prices) > 1:

            pricedict = self._create_dict(prices)
            normalized_pricedict = self._create_dict(self._normalize_prices(prices))
            
            """
            Curve is too flat if stdev is <= 0.05. 
            If so we don't do any specific non or caution-hours based on pricing.
            """
            if stat.stdev(prices) > 0.05:
                prices_ranked = self._rank_prices(pricedict, normalized_pricedict)
                ready_hours = self._determine_hours(prices_ranked)
            else:
                ready_hours = ret
            if self._absolute_top_price is not None:
                ret = self._add_expensive_non_hours(pricedict, ready_hours)
            else: 
                ret = ready_hours
        return ret

    def _normalize_prices(self, prices) -> list:
        min_price = min(prices)
        ret = []
        for p in prices:
            ret.append(p/min_price)
        return ret

    def _add_expensive_non_hours(self, hourdict: dict, readyhours:HourObject) -> HourObject:
        lst = (h for h in hourdict if hourdict[h] >= self._absolute_top_price)
        for h in lst:
            if h not in readyhours.nh:
                readyhours.nh.append(h)
                if h in readyhours.ch:
                    readyhours.ch.remove(h)
        readyhours.nh.sort()
        return readyhours

    def _rank_prices(self, hourdict: dict, normalized_hourdict: dict):
        ret = {}
        _maxval = max(hourdict.values())
        _max_normalized = max(normalized_hourdict.values())
        peaqstdev = _maxval/abs(_max_normalized/stat.stdev(normalized_hourdict.values()))
        for key in hourdict:
            if hourdict[key] > peaqstdev:
                ret[key] = {"val": hourdict[key], "permax": round(hourdict[key] / _maxval, 2)}
        return ret

    def _create_dict(self, input: list):
        ret = {}
        for idx, val in enumerate(input):
            ret[idx] = val
        try:
            assert len(ret) == 24
        except Exception:
            raise ValueError
        return ret

    def _determine_hours(self, price_list: dict) -> HourObject:
        _nh = []
        #_ch = {}
        _ch = []
        for p in price_list:
            if float(price_list[p]["permax"]) <= self._cautionhour_type:
                _ch.append(p)
                #_ch[p] = round(abs(price_list[p]["permax"] - 1), 2)
            else:
                _nh.append(p)
        return HourObject(_nh, _ch)
    
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

    @staticmethod
    def _try_parse(input:str, parsetype:type):
        try:
            ret = parsetype(input)
            return ret
        except:
            return False
