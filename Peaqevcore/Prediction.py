from peaqevcore.util import _convert_quarterly_minutes

class PredictionBase:
    @staticmethod
    def predictedenergy(
            nowmin: int,
            nowsec: int,
            poweravg: float,
            totalhourlyenergy: float,
            is_quarterly:bool=False
    ) -> float:
        if nowmin not in range(0, 60):
            raise ValueError
        if nowsec not in range(0, 60):
            raise ValueError
        if poweravg < 0 or totalhourlyenergy < 0:
            raise ValueError

        minute = _convert_quarterly_minutes(nowmin, is_quarterly)

        if totalhourlyenergy > 0 and (minute > 0 or (minute + nowsec) > 30):
            ret = (((poweravg / 60 / 60) * (3600 - ((minute * 60) + nowsec)) + totalhourlyenergy * 1000) / 1000)
        else:
            ret = poweravg / 1000
        return round(ret, 3)

    @staticmethod
    def predictedpercentageofpeak(
            peak: float,
            predictedenergy: float
    ) -> float:
        if peak == 0.0 or peak is None:
            return 0
        elif predictedenergy == 0.0 or predictedenergy is None:
            return 0
        return round((predictedenergy / peak) * 100, 2)
