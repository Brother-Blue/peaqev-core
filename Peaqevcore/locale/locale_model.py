from dataclasses import dataclass
from datetime import datetime, date, time
from typing import List

HOURLY = "Hourly"
QUERYTYPE_BASICMAX = "bbfs"


@dataclass(frozen=True)
class Locale_Type:
    observed_peak:str
    charged_peak:str
    free_charge_pattern:List = None
    peakcycle:str = HOURLY

    def is_free_charge(self, mockdt:datetime = datetime.min) -> bool:
        if self.free_charge_pattern is None or len(self.free_charge_pattern) == 0:
            return False
        now = datetime.now() if mockdt is datetime.min else mockdt
        for p in self.free_charge_pattern:
            if now.month in p["M"]:
                if now.weekday() in p["D"]:
                    if now.hour in p["H"]:
                        return True
        return False




#dag kl. 06-22 nov-mars                 106,25 kr/kW/mån
#dag kl. 06-22 april-okt                50 kr/kW/mån
#natt kl. 22-06 alla dagar hela året    0 kr/kW/mån

@dataclass(frozen=True)
class SE_Bjerke_Energi(Locale_Type):
    observed_peak = QUERYTYPE_BASICMAX
    charged_peak = QUERYTYPE_BASICMAX
    free_charge_pattern = [
        {
            "M": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "D": [0, 1, 2, 3, 4, 5, 6],
            "H": [22, 23, 0, 1, 2, 3, 4, 5]
        }
    ]

"""
Note, high load extra is added from 06-22 during november - march. 
This does not affect the peak, but should in future updates be cause for forced non-/or caution-hours to lessen the cost for the consumer.
"""

#https://www.bjerke-energi.se/elnat/tariffer/effekttariff-fr-o-m-2022-02-01/


#-----------------------------------------------------

p = SE_Bjerke_Energi
d = date(2005, 7, 14)
t = time(22, 30)
dt = datetime.combine(d, t)
print(p.is_free_charge(p, mockdt=dt))


