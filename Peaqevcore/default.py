from .querytypes import (
    QUERYTYPE_BASICMAX
)

from Peaqevcore.locale.locale_model import Locale_Type
from dataclasses import dataclass

@dataclass(frozen=True)
class Default(Locale_Type):
    observed_peak = QUERYTYPE_BASICMAX
    charged_peak = QUERYTYPE_BASICMAX
    converted = True
