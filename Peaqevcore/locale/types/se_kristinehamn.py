
from custom_components.peaqev.peaqservice.util.constants import (
    QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR
)
from ..locale_model import Locale_Type
from dataclasses import dataclass

@dataclass(frozen=True)
class SE_Kristinehamn(Locale_Type):
    observed_peak = QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR
    charged_peak = QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR
        




"""
https://kristinehamnsenergi.se/elnat/elnatsavgiften/effektavgift-villa-med-bergvarmepump/

vardagar november-mars, kl 07.00-17.00 > highload instead of normal load. other times, normal load
"""
