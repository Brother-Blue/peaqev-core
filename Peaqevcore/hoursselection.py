from datetime import datetime
import statistics as stat
import operator
from .Models import (
    CAUTIONHOURTYPE_SUAVE,
    CAUTIONHOURTYPE_INTERMEDIATE,
    CAUTIONHOURTYPE_AGGRESSIVE,
    CAUTIONHOURTYPE
)

from .hourselection.hoursselection_helpers import HourObject, HourObjectExtended, HourSelectionHelpers

class Hoursselectionbase:
    def __init__(
            self,      
            absolute_top_price: float = 0,
            min_price: float = 0,
            cautionhour_type: float = CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE],
            allow_top_up: bool = False
    ):
        self._prices = None
        self._prices_tomorrow = None
        self._non_hours = []
        self._caution_hours = []
        self._dynamic_caution_hours = {}
        self._absolute_top_price = self._set_absolute_top_price(absolute_top_price)
        self._cautionhour_type: float = cautionhour_type
        self._min_price: float = min_price
        self._allow_top_up: bool = allow_top_up
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
        if self._prices == self.prices_tomorrow:
            self.prices_tomorrow = None
        else:
            self.update()

    @property
    def prices_tomorrow(self) -> list:
        return self._prices_tomorrow

    @prices_tomorrow.setter
    def prices_tomorrow(self, val):
        self._prices_tomorrow = HourSelectionHelpers._convert_none_list(val)
        self.update()

    @property
    def absolute_top_price(self) -> float:
        return self._absolute_top_price

    @property
    def min_price(self) -> float:
        return self._min_price

    def update(self, testhour:int = None):
        today_ready = self._update_per_day(self.prices)
        hours_today = self._add_remove_limited_hours(today_ready)

        if self.prices_tomorrow is not None and len(self.prices_tomorrow) > 0:
            tomorrow_ready = self._update_per_day(self.prices_tomorrow)
            if tomorrow_ready is not None:
                hours_tomorrow = self._add_remove_limited_hours(tomorrow_ready)

        self.non_hours = []
        self.caution_hours = []
        self.dynamic_caution_hours = {}

        hour = datetime.now().hour if testhour is None else testhour
        self.non_hours.extend(h for h in hours_today.nh if h >= hour)
        self.caution_hours.extend(h for h in hours_today.ch if h >= hour)
        for h in hours_today.dyn_ch:
            if h >= hour:
                self._dynamic_caution_hours[h] = hours_today.dyn_ch[h]
        if self.prices_tomorrow is not None and len(self.prices_tomorrow) > 0:
            self.non_hours.extend(h for h in hours_tomorrow.nh if h < hour)
            self.caution_hours.extend(h for h in hours_tomorrow.ch if h < hour)
            for h in hours_tomorrow.dyn_ch:
                if h < hour:
                    self._dynamic_caution_hours[h] = hours_tomorrow.dyn_ch[h]
        if self._allow_top_up is True:
            self._set_top_up(hour)

    def _update_per_day(self, prices) -> HourObjectExtended:
        pricedict = dict
        if prices is not None and len(prices) > 1:
            pricedict = HourSelectionHelpers._create_dict(prices)
            normalized_pricedict = HourSelectionHelpers._create_dict(HourSelectionHelpers._normalize_prices(prices))
            """
            Curve is too flat if stdev is <= 0.05. 
            If so we don't do any specific non or caution-hours based on pricing.
            """
            if stat.stdev(prices) > 0.05:
                prices_ranked = HourSelectionHelpers._rank_prices(pricedict, normalized_pricedict)
                ready_hours = self._determine_hours(prices_ranked, prices)
                return HourObjectExtended(ready_hours.nh, ready_hours.ch, ready_hours.dyn_ch, pricedict)
            return HourObjectExtended([], [], {}, pricedict)
        
    def _add_remove_limited_hours(self, hours: HourObjectExtended) -> HourObject:
        """Removes cheap hours and adds expensive hours set by user limitation"""
        if self._absolute_top_price is not None:
                ret = self._add_expensive_non_hours(hours)
        else: 
            ret = HourObject(hours.nh, hours.ch, hours.dyn_ch)
        if self._min_price > 0:
            ret = self._remove_cheap_hours(hours)
        return ret

    def _set_top_up(self, hour:int):
        """Sets top-up if tomorrow is x more expensive than today and vice versa"""
        if self.prices_tomorrow is None or len(self.prices_tomorrow) == 0:
            return

        today = list(self.prices[hour-1:23])
        tomorrow = list(self.prices_tomorrow[0:hour-1])
        print(f"hour: {hour} today: {today}, tomorrow: {tomorrow}")
        today_dict = HourSelectionHelpers._create_partial_dict(input=today, hour=hour, today=True)
        tomorrow_dict = HourSelectionHelpers._create_partial_dict(input=tomorrow, hour=hour, today=False)

        if max(today) < (sum(tomorrow)/len(tomorrow)):
           self._remove_and_add_for_top_up(today_dict, tomorrow_dict)
        elif max(tomorrow) < (sum(today)/len(today)):
           self._remove_and_add_for_top_up(tomorrow_dict, today_dict)
        self.non_hours.sort()
        
    def _remove_and_add_for_top_up(self, removedict:dict, adddict:dict) -> int:
            removed = 0
            popkeys = []
            for i in self.non_hours:
                if i in removedict.keys():
                    self.non_hours.remove(i)
                    removed += 1
            for i in self.caution_hours:
                if i in removedict.keys():
                    self.caution_hours.remove(i)
                    removed += 1
            for k,v in self.dynamic_caution_hours.items():
                if k in removedict.keys():
                    popkeys.append(k)
                    removed += 1
            if len(popkeys) > 0:
                for i in popkeys:
                    self.dynamic_caution_hours.pop(i)
            
            sorted_add = list(dict(sorted(adddict.items(), key=operator.itemgetter(1),reverse=True)).keys())
            added = 0
            for i in range(0, removed-1):
                try:
                    if sorted_add[i] not in self.non_hours:
                        self.non_hours.append(sorted_add[i])
                        self.dynamic_caution_hours.pop(i)
                        added += 1
                    elif sorted_add[i] in self.dynamic_caution_hours.items():
                        self.non_hours.append(sorted_add[i])
                        self.dynamic_caution_hours.pop(i)
                        added += 1
                except:
                    continue
            if added == 0:
                for a in adddict:
                    if a in self.dynamic_caution_hours.keys():
                        self.non_hours.append(a)
                        self.dynamic_caution_hours.pop(a)

    def _remove_cheap_hours(self, hours: HourObjectExtended) -> HourObject:
        lst = (h for h in hours.pricedict if hours.pricedict[h] < self._min_price)
        for h in lst:
            if h in hours.nh:
                hours.nh.remove(h)
            elif h in hours.ch:
                hours.ch.remove(h)
                hours.dyn_ch.pop(h)    
        return HourObject(hours.nh, hours.ch, hours.dyn_ch)

    def _add_expensive_non_hours(self, readyhours:HourObjectExtended) -> HourObject:
        lst = (h for h in readyhours.pricedict if readyhours.pricedict[h] >= self._absolute_top_price)
        for h in lst:
            if h not in readyhours.nh:
                readyhours.nh.append(h)
                if h in readyhours.ch:
                    readyhours.ch.remove(h)
                if len(readyhours.dyn_ch) > 0:
                    if h in readyhours.dyn_ch.keys():
                        readyhours.dyn_ch.pop(h)
        readyhours.nh.sort()
        return HourObject(readyhours.nh, readyhours.ch, readyhours.dyn_ch)

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


