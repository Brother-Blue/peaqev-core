from custom_components.peaqev.peaqservice.util.constants import (
    QUERYTYPE_AVERAGEOFTHREEDAYS,
    QUERYTYPE_AVERAGEOFTHREEDAYS_MIN
)
from ..locale_model import Locale_Type
from dataclasses import dataclass

@dataclass(frozen=True)
class SE_Gothenburg(Locale_Type):
    observed_peak = QUERYTYPE_AVERAGEOFTHREEDAYS_MIN
    charged_peak = QUERYTYPE_AVERAGEOFTHREEDAYS
        