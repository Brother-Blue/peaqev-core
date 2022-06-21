from .util import _convert_quarterly_minutes


class PeaqValueError(ValueError):
    def __init__(self, message):
        self.message = message

class PredictionBase:
    @staticmethod
    def predictedenergy(
            now_min: int,
            now_sec: int,
            power_avg: float,
            total_hourly_energy: float,
            is_quarterly:bool=False
    ) -> float:
        if now_min not in range(0, 60):
            raise PeaqValueError("Value 'now_min' must be between 0..60")
        if now_sec not in range(0, 60):
            raise PeaqValueError("Value 'now_max' must be between 0..60")
        if power_avg < 0 or total_hourly_energy < 0:
            raise PeaqValueError("Value 'power_avg' or 'total_hourly_energy' must be greater than or equal to 0")

        minute = _convert_quarterly_minutes(now_min, is_quarterly)

        if total_hourly_energy > 0 and (minute > 0 or (minute + now_sec) > 30):
            ret = (((power_avg / 60 / 60) * (3600 - ((minute * 60) + now_sec)) + total_hourly_energy * 1000) / 1000)
        else:
            ret = power_avg / 1000
        return round(ret, 3)

    @staticmethod
    def predictedpercentageofpeak(
            peak: float,
            predicted_energy: float
    ) -> float:
        if peak == 0.0 or peak is None:
            return 0
        elif predicted_energy == 0.0 or predicted_energy is None:
            return 0
        return round((predicted_energy / peak) * 100, 2)
