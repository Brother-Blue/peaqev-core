
from custom_components.peaqev.peaqservice.util.constants import (
    QUERYTYPE_AVERAGEOFTHREEHOURS,
    QUERYTYPE_AVERAGEOFTHREEHOURS_MIN
)
from ..locale_model import Locale_Type
from dataclasses import dataclass

@dataclass(frozen=True)
class SE_Nacka_normal(Locale_Type):
    observed_peak = QUERYTYPE_AVERAGEOFTHREEHOURS_MIN
    charged_peak = QUERYTYPE_AVERAGEOFTHREEHOURS
    super().__init__(
        observedpeak=observed_peak,
        chargedpeak=charged_peak
    )


@dataclass(frozen=True)
class SE_NACKA_timediff(Locale_Type):
    pass
    #this class is for nacka time differentiated peaks.



#https://www.nackaenergi.se/images/downloads/natavgifter/FAQ_NYA_TARIFFER.pdf
