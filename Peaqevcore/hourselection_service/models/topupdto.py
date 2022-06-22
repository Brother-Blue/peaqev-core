from dataclasses import dataclass
from .hourobject import HourObject

@dataclass
class HoursDTO:
    nh: list
    ch: list
    dyn_ch: dict
    top_price:float
    min_price:float

@dataclass
class TopUpDTO(HoursDTO):
    """DTO-object to transfer between hourselection and top_up"""
    hour:int
    today_hours:HourObject
    tomorrow_hours:HourObject
    prices: list
    prices_tomorrow:list