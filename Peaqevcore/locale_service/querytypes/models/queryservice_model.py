from dataclasses import dataclass, field
from typing import List
from .enums import Dividents

@dataclass
class datepart_model:
    type: str = field(default_factory=lambda : "")
    dttype: str = field(default_factory=lambda : "")
    values: List[int] = field(default_factory=lambda : [])

@dataclass
class group:
    divident: Dividents = field(default_factory=lambda: Dividents.UNSET)
    dateparts: List[datepart_model] = field(default_factory=lambda : [datepart_model()])

@dataclass
class queryservicemodel:
    groups: List[group] = field(default_factory=lambda : [group()])
