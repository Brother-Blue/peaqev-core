from .util import _convert_quarterly_minutes

class ThresholdBase:
    BASECURRENT = 6

    @staticmethod
    def stop(
              now_min: int,
              is_caution_hour: bool,
              is_quarterly: bool=False
              ) -> float:
        minute = _convert_quarterly_minutes(now_min, is_quarterly)
        
        if is_caution_hour and minute < 45:
            ret = (((minute+pow(1.075, minute)) * 0.0032) + 0.7)
        else:
            ret = (((minute + pow(1.071, minute)) * 0.00165) + 0.8)
        return round(ret * 100, 2)

    @staticmethod
    def start(
               now_min: int,
               is_caution_hour: bool,
               is_quarterly:bool=False
               ) -> float:
        minute = _convert_quarterly_minutes(now_min, is_quarterly)
        if is_caution_hour and minute < 45:
            ret = (((minute+pow(1.081, minute)) * 0.0049) + 0.4)
        else:
            ret = (((minute + pow(1.066, minute)) * 0.0045) + 0.5)
        return round(ret * 100, 2)
    
    @staticmethod
    def allowed_current(
            now_min: int,
            moving_avg: float,
            charger_enabled: bool,
            charger_done: bool,
            currents_dict: dict,
            total_energy: float,
            peak: float,
            is_quarterly:bool=False
            ) -> int:
        minute = _convert_quarterly_minutes(now_min, is_quarterly)
        ret = ThresholdBase.BASECURRENT
        if not charger_enabled or charger_done or moving_avg == 0:
            return ret
        currents = currents_dict
        for key, value in currents.items():
            if ((((moving_avg + key) / 60) * (60 - minute) + total_energy * 1000) / 1000) < peak:
                ret = value
                return ret
        return ret
    
