
from custom_components.peaqev.peaqservice.util.constants import (
    QUERYTYPE_BASICMAX
)
from ..locale_model import Locale_Type
from dataclasses import dataclass

@dataclass(frozen=True)
class SE_Karlstad(Locale_Type):
    
    observed_peak = QUERYTYPE_BASICMAX #todo check if correct
    charged_peak = QUERYTYPE_BASICMAX #todo check if correct
        
"""
Note, high load extra is added on weekdays from 6-18 during november - march. 
This does not affect the peak, but should in future updates be cause for forced non-/or caution-hours to lessen the cost for the consumer.
"""

#https://karlstadsnat.se/elnat/kund/priser-och-tariffer/effekttariff/
