from custom_components.peaqev.peaqservice.util.constants import (
    QUERYTYPE_BASICMAX
)
from dataclasses import dataclass
from ..locale_model import Locale_Type

@dataclass(frozen=True)
class SE_Partille(Locale_Type):
    observed_peak = QUERYTYPE_BASICMAX
    charged_peak = QUERYTYPE_BASICMAX
        