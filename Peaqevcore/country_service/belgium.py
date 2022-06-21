from ..locale_service.querytypes.querytypes import QUERYTYPES
from ..locale_service.querytypes.const import (QUARTER_HOURLY, QUERYTYPE_BASICMAX)
from dataclasses import dataclass
from ..locale_service.locale_model import Locale_Type


@dataclass(frozen=True)
class VregBelgium(Locale_Type):
    observed_peak = QUERYTYPE_BASICMAX
    charged_peak = QUERYTYPE_BASICMAX
    converted = True
    query_model = QUERYTYPES[QUERYTYPE_BASICMAX]
    #TODO: to be decided. Should charged_peak be turned into the real charged peak, ie the average of the months in a year? could be issues with the long term stats there and it won't help peaq in any way.
    peak_cycle = QUARTER_HOURLY

#https://www.vreg.be/nl/nieuwe-nettarieven        
