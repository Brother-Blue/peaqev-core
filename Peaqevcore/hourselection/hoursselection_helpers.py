import statistics as stat
from dataclasses import dataclass


@dataclass
class HourObject:
    nh: list
    ch: list
    dyn_ch: dict


@dataclass
class HourObjectExtended(HourObject):
    pricedict: dict


class HourSelectionHelpers:
    @staticmethod
    def _create_dict(input: list):
        ret = {}
        for idx, val in enumerate(input):
            ret[idx] = val
        try:
            assert len(ret) == 24
        except Exception:
            raise ValueError
        return ret

    @staticmethod
    def _try_parse(input:str, parsetype:type):
        try:
            ret = parsetype(input)
            return ret
        except:
            return False
    
    @staticmethod
    def _convert_none_list(lst:list) -> list:
        try:
            ret = []
            for l in lst:
                if l is None:
                    return ret
            return lst
        except:
            return HourSelectionHelpers._make_array_from_empty(lst)

    @staticmethod
    def _make_array_from_empty(input) -> list:
        array = input.split(",")
        list = [p for p in array if len(p) > 0]
        ret = []
        if len(list) > 24:
            try:
                for l in list:
                    parsed_item = HourSelectionHelpers._try_parse(l, float)
                    if not parsed_item:
                        parsed_item = HourSelectionHelpers._try_parse(l, int)
                    assert type(parsed_item) is float or type(parsed_item) is int
                    ret.append(parsed_item)
                return ret
            except:
                return []
        return []

    @staticmethod
    def _create_partial_dict(input: list, hour:int, today:bool = True):
        ret = {}
        if today:
            dictrange = range(hour,24)
        else:
            dictrange = range(0,hour-1)
        assert len(dictrange) == len(input)
        for idx, val in enumerate(input):
            ret[dictrange[idx]] = val
        return ret

    @staticmethod
    def _normalize_prices(prices:list) -> list:
        min_price = min(prices)
        ret = []
        for p in prices:
            ret.append(p/min_price)
        return ret

    @staticmethod
    def _rank_prices(hourdict: dict, normalized_hourdict: dict) -> dict:
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
        return HourSelectionHelpers._discard_excessive_hours(ret)

    @staticmethod
    def _discard_excessive_hours(hours: dict):
        """There should always be at least four regular hours before absolute_top_price kicks in."""
        if len(hours) < 20:
            return hours
        while len(hours) >= 20:
            to_pop = dict(sorted(hours.items(), key=lambda item: item[1]['val']))    
            hours.pop(list(to_pop.keys())[0])
        return hours