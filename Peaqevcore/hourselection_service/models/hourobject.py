from dataclasses import dataclass

@dataclass
class HourObject:
    nh: list
    ch: list
    dyn_ch: dict


@dataclass
class HourObjectExtended(HourObject):
    pricedict: dict
