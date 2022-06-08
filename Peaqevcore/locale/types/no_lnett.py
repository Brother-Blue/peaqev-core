from custom_components.peaqev.peaqservice.util.constants import (
    QUERYTYPE_AVERAGEOFTHREEHOURS_MIN, QUERYTYPE_AVERAGEOFTHREEHOURS
)
from ..locale_model import Locale_Type
from dataclasses import dataclass

#https://www.l-nett.no/nynettleie/slik-blir-ny-nettleie-og-pris

@dataclass(frozen=True)
class NO_LNett(Locale_Type):
    observed_peak = QUERYTYPE_AVERAGEOFTHREEHOURS_MIN
    charged_peak = QUERYTYPE_AVERAGEOFTHREEHOURS
        
