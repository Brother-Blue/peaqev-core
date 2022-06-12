from ..locale.querytypes import (
    QUERYTYPE_AVERAGEOFTHREEDAYS,
    QUERYTYPE_AVERAGEOFTHREEDAYS_MIN,
    QUERYTYPE_AVERAGEOFTHREEHOURS_MIN, QUERYTYPE_AVERAGEOFTHREEHOURS,
    QUERYTYPE_BASICMAX,
    QUERYTYPES
)
from ..locale.locale_model import Locale_Type
from dataclasses import dataclass

@dataclass(frozen=True)
class NO_Tensio(Locale_Type):
    observed_peak = QUERYTYPE_AVERAGEOFTHREEDAYS_MIN
    charged_peak = QUERYTYPE_AVERAGEOFTHREEDAYS
    converted = True
    query_model = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]

@dataclass(frozen=True)
class NO_LNett(Locale_Type):
    observed_peak = QUERYTYPE_AVERAGEOFTHREEHOURS_MIN
    charged_peak = QUERYTYPE_AVERAGEOFTHREEHOURS
    converted = True
    query_model = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEHOURS]

#docs: https://www.l-nett.no/nynettleie/slik-blir-ny-nettleie-og-pris        


@dataclass(frozen=True)
class NO_GlitreEnergi(Locale_Type):
    observed_peak = QUERYTYPE_BASICMAX
    charged_peak = QUERYTYPE_BASICMAX
    converted = True
    query_model = QUERYTYPES[QUERYTYPE_BASICMAX]

#docs: https://www.glitreenergi-nett.no/smart-nettleie/


@dataclass(frozen=True)
class NO_AgderEnergi(Locale_Type):
    observed_peak = QUERYTYPE_AVERAGEOFTHREEDAYS_MIN
    charged_peak = QUERYTYPE_AVERAGEOFTHREEDAYS
    converted = True    
    query_model = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
