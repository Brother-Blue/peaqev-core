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
            absolute_top_price: float = None,
            cautionhour_type: float = CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE]
    ):
        self._prices = []
        self._prices_tomorrow = []
        self._non_hours = []
        self._caution_hours = []
        self._absolute_top_price = absolute_top_price if absolute_top_price is not None else float("inf")
        self._cautionhour_type = cautionhour_type
        self._validate()
        self.update()

    def _validate(self):
        assert 0 < self._cautionhour_type <= 1
        assert type(self._absolute_top_price) is float or type(self._absolute_top_price) is int
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
    def prices_tomorrow(self):
        return self._prices_tomorrow

    @prices_tomorrow.setter
    def prices_tomorrow(self, val):
        self._prices_tomorrow = self._check_tomorrow_prices(val)
        self.update()

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
        if len(prices) > 1:
            pricedict = self._create_dict(prices)
            """
            Curve is too flat if stdev is <= 0.05. 
            If so we don't do any specific non or caution-hours based on pricing.
            """
            if stat.stdev(prices) > 0.05:
                prices_ranked = self._rank_prices(pricedict)
                ready_hours = self._determine_hours(prices_ranked)
            else:
                ready_hours = ret
            if self._absolute_top_price is not None:
                ret = self._add_expensive_non_hours(pricedict, ready_hours)
            else: 
                ret = ready_hours
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

    def _rank_prices(self, hourdict: dict):
        ret = {}
        _maxval = max(hourdict.values())
        for key in hourdict:
            if hourdict[key] > abs(_maxval * (1 - stat.stdev(hourdict.values()))):
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
            if round(abs(price_list[p]["permax"] - 1), 2) <= self._cautionhour_type:
                _nh.append(p)
            else:
                _ch.append(p)
                #_ch[p] = round(abs(price_list[p]["permax"] - 1), 2)

        return HourObject(_nh, _ch)
    
    def _check_tomorrow_prices(self, input) -> list:
        if type(input) is list:
            return self._convert_none_list(input)
        return self._make_array_from_empty(input)

    def _convert_none_list(self, lst:list):
        ret = []
        for l in lst:
            if l is None:
                return ret
        return lst

    def _make_array_from_empty(self, input) -> list:
        array = input.split(",")
        list = [p for p in array if len(p) > 0]
        ret = []
        if len(list) > 0:
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
