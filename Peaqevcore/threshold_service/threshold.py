from ..util import _convert_quarterly_minutes

class ThresholdBase:
    BASECURRENT = 6

    @staticmethod
    def stop(
              nowmin:int,
              is_cautionhour:bool,
              is_quarterly:bool=False
              ) -> float:
        minute = _convert_quarterly_minutes(nowmin, is_quarterly)
        
        if is_cautionhour is True and minute < 45:
            ret = (((minute+pow(1.075, minute)) * 0.0032) + 0.7)
        else:
            ret = (((minute + pow(1.071, minute)) * 0.00165) + 0.8)
        return round(ret * 100, 2)

    @staticmethod
    def start(
               nowmin: int,
               is_cautionhour: bool,
               is_quarterly:bool=False
               ) -> float:
        minute = _convert_quarterly_minutes(nowmin, is_quarterly)
        if is_cautionhour is True and minute < 45:
            ret = (((minute+pow(1.081, minute)) * 0.0049) + 0.4)
        else:
            ret = (((minute + pow(1.066, minute)) * 0.0045) + 0.5)
        return round(ret * 100, 2)
    
    @staticmethod
    def allowedcurrent(
            nowmin: int,
            movingavg: float,
            charger_enabled: bool,
            charger_done: bool,
            currentsdict: dict,
            totalenergy: float,
            peak: float,
            is_quarterly:bool=False
            ) -> int:
        minute = _convert_quarterly_minutes(nowmin, is_quarterly)
        ret = ThresholdBase.BASECURRENT
        if charger_enabled is False or charger_done is True or movingavg == 0:
            return ret
        currents = currentsdict
        for key, value in currents.items():
            if ((((movingavg + key) / 60) * (60 - minute) + totalenergy * 1000) / 1000) < peak:
                ret = value
                break
        return ret
    
