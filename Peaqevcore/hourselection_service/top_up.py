
from .models.hourobject import HourObject
from .models.topupdto import HoursDTO, TopUpDTO
import operator

def top_up(model:TopUpDTO) -> HourObject:
    """Sets top-up if tomorrow is x more expensive than today and vice versa"""
    if model.prices_tomorrow is None or len(model.prices_tomorrow) == 0:
        return

    today = list(model.prices[model.hour-1:23])
    tomorrow = list(model.prices_tomorrow[0:model.hour-1])
    
    if max(today) < (sum(tomorrow)/len(tomorrow)):
        is_today = True
        cheap_max = max(today)
    elif max(tomorrow) < (sum(today)/len(today)):
        is_today = False
        cheap_max = max(tomorrow)
    
    result = _remove_and_add_for_top_up(
        model=HoursDTO(
            model.nh, 
            model.ch, 
            model.dyn_ch, 
            model.top_price, 
            model.min_price),
        today_dict=_create_partial_dict(
            today, 
            model.hour, 
            True), 
        tomorrow_dict=_create_partial_dict(
            tomorrow, 
            model.hour, 
            False), 
        max_cheap=cheap_max, 
        today=is_today
        )

    result.nh = list(set(result.nh))
    result.nh.sort()
    try:
        dynamic_caution_hours = {key: value for (key, value) in result.dyn_ch.items() if key not in model.nh}
    except Exception as e:
        print(f"{e}: {result.dyn_ch}")
        dynamic_caution_hours = {}

    return HourObject(
        nh=result.nh,
        ch=[],
        dyn_ch=dynamic_caution_hours
    )

def _remove_and_add_for_top_up(
    model: HoursDTO,
    today_dict:dict, 
    tomorrow_dict:dict, 
    max_cheap:float, 
    today:bool
    ) -> HoursDTO:

    nonhours_remove = []
    cautionhours_remove = []
    removed = 0
    popkeys = []

    if today is True:
        removedict = today_dict
        adddict = tomorrow_dict
    else:
        removedict = tomorrow_dict
        adddict = today_dict

    removed += _append_items_to_remove(model, nonhours_remove, cautionhours_remove, removedict)
    for k,v in model.dyn_ch.items():
        if k in removedict.keys():
            popkeys.append(k)
            removed += 1
    if len(popkeys) > 0:
        for i in popkeys:
            model.dyn_ch.pop(i)
            
    _remove_items(nonhours_remove, model.nh)
    _remove_items(cautionhours_remove, model.ch)
    sorted_add = list(dict(sorted(adddict.items(), key=operator.itemgetter(1),reverse=True)).keys())
    added = 0
    for i in range(0, removed-1):
        try:
            if adddict[sorted_add[i]] > max_cheap:
                if sorted_add[i] not in model.nh:
                    model.nh.append(sorted_add[i])
                    model.dyn_ch.pop(i)
                    added += 1
                if sorted_add[i] in model.dyn_ch.keys():
                    model.nh.append(sorted_add[i])
                    model.dyn_ch.pop(i)
                    added += 1
        except:
            continue
    if added == 0:
        for a in adddict:
            if a in model.dyn_ch.keys():
                model.nh.append(a)
                model.dyn_ch.pop(a)
    return model

def _append_items_to_remove(model:HoursDTO, nonhours_remove:list, cautionhours_remove:list,removedict:dict) -> int:
    return _append_non_hours(
        model, 
        nonhours_remove, 
        removedict
        ) + _append_caution_hours(
            model.ch, 
            cautionhours_remove, 
            removedict
            )

def _append_non_hours(model:HoursDTO, nonhours_remove:list, removedict:dict) -> int:
    _removed = 0
    for i in [i for i in model.nh if i in removedict.keys() and removedict[i] < model.top_price]:
        if i in removedict.keys():
            nonhours_remove.append(i)
            _removed += 1
    return _removed

def _append_caution_hours(cautionhours, cautionhours_remove, removedict) -> int:
    _removed = 0
    for i in cautionhours:
        if i in removedict.keys():
            cautionhours_remove.append(i)
            _removed += 1
    return _removed

def _remove_items(checklist: list, deletelist: list) -> None:
    if len(checklist) > 0:
        for i in checklist:
            deletelist.remove(i)

def _create_partial_dict(input: list, hour:int, today:bool = True) -> dict:
    ret = {}
    if today:
        dictrange = range(hour,24)
    else:
        dictrange = range(0,hour-1)
    assert len(dictrange) == len(input)
    for idx, val in enumerate(input):
        ret[dictrange[idx]] = val
    return ret