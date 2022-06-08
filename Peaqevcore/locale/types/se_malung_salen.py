
from custom_components.peaqev.peaqservice.util.constants import (
    QUERYTYPE_AVERAGEOFFIVEDAYS,
    QUERYTYPE_AVERAGEOFFIVEDAYS_MIN
)
from ..locale_model import Locale_Type
from dataclasses import dataclass

#Rörlig avgift sommar april – oktober 35 kr/kW
#Rörlig avgift vinter november – mars 118,75 kr/kW

@dataclass(frozen=True)
class SE_Malung_Salen(Locale_Type):
    observed_peak = QUERYTYPE_AVERAGEOFFIVEDAYS_MIN
    charged_peak = QUERYTYPE_AVERAGEOFFIVEDAYS
    free_charge_pattern = [
        {
            "M": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "D": [0, 1, 2, 3, 4, 5, 6],
            "H": [19,20,21,22, 23, 0, 1, 2, 3, 4, 5,6]
        }
    ]
