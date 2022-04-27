import statistics as stat
from .Models import (
    CAUTIONHOURTYPE_AGGRESSIVE,
    CAUTIONHOURTYPE
)

class Hoursselectionbase:
    def __init__(
            self,      
            absolute_top_price: float = None,
            cautionhour_type: float = CAUTIONHOURTYPE[CAUTIONHOURTYPE_AGGRESSIVE]
    ):
        self._prices = []
        self._non_hours = []
        self._caution_hours = []
        self._absolute_top_price = absolute_top_price if absolute_top_price is not None else float("inf")
        self._cautionhour_type = cautionhour_type
        self.update()

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

    def update(self):
        if len(self.prices) > 1:
            pricedict = self._create_dict(self.prices)
            """
            Curve is too flat if stdev is <= 0.05. 
            If so we don't do any specific non or caution-hours based on pricing.
            """
            if stat.stdev(self.prices) > 0.05:
                prices_ranked = self._rank_prices(pricedict)
                self._determine_hours(prices_ranked)
            if self._absolute_top_price is not None:
                self._add_expensive_non_hours(pricedict)

    def _add_expensive_non_hours(self, hourdict: dict):
        lst = (h for h in hourdict if hourdict[h] >= self._absolute_top_price)
        for h in lst:
            if h not in self.non_hours:
                self.non_hours.append(h)
                if h in self.caution_hours:
                    del self.caution_hours[h]
        self.non_hours.sort()

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

    def _determine_hours(self, price_list: dict):
        _nh = []
        #_ch = {}
        _ch = []
        for p in price_list:
            if round(abs(price_list[p]["permax"] - 1), 2) <= self._cautionhour_type:
                _nh.append(p)
            else:
                _ch.append(p)
                #_ch[p] = round(abs(price_list[p]["permax"] - 1), 2)

        self.non_hours = _nh
        self.caution_hours = _ch