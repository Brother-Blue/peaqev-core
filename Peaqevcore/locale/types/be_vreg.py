
from homeassistant.components.utility_meter.sensor import (
    QUARTER_HOURLY
)

from custom_components.peaqev.peaqservice.util.constants import (
    QUERYTYPE_BASICMAX
)

from dataclasses import dataclass
from ..locale_model import Locale_Type

#https://www.vreg.be/nl/nieuwe-nettarieven

@dataclass(frozen=True)
class VregBelgium(Locale_Type):
    observed_peak = QUERYTYPE_BASICMAX
    charged_peak = QUERYTYPE_BASICMAX
    #TODO: to be decided. Should charged_peak be turned into the real charged peak, ie the average of the months in a year? could be issues with the long term stats there and it won't help peaq in any way.
    peakcycle = QUARTER_HOURLY
        
