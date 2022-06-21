import time

class PowerReading:
    def __init__(self, price, power, td) -> None:
        self._price = price
        self._power = power
        self._time_delta = td
    
    @property
    def reading_integral(self):
        return self.power/1000 * (self.time_delta/3600)

    @property
    def reading_cost(self):
        return self.reading_integral * self.price

    @property
    def price(self):
        return self._price

    @property
    def power(self):
        return self._power

    @property
    def time_delta(self):
        return self._time_delta


class SessionPrice:
    def __init__(self) -> None:
        self._total_price = 0
        self._price = 0
        self._current_power = 0
        self._total_power = 0
        self._current_time = 0
        self._time_delta = 0
        self._readings = []
    
    @property
    def total_power(self):
        return round(self._total_power,5)

    def terminate(self, mock_time:float=None):
        print("called terminate")
        self.update_power_reading(0, mock_time)
        self.get_status()
        
    def get_status(self) -> dict:
        self._total_power = 0
        self._total_price = 0
        for i in self._readings:
            self._total_power += i.reading_integral
            self._total_price += i.reading_cost
        return {
            "energy": {
                "value": self._total_power,
                "unit": "kWh"
            },
            "price": self._total_price
        }
            
    def update_power_reading(self, power:float, mock_time:float=None):
        self._set_delta(mock_time)
        p = PowerReading(self._price, self._current_power, self._time_delta)
        print(p.power, p.price, p.reading_cost, p.reading_integral)
        self._readings.append(p)
        self._current_power = power
        
    def update_price(self, price:float, mock_time:float=None):
        if self._current_power > 0:
            self.update_power_reading(
                power=self._current_power, 
                mock_time=mock_time
                )
        self._price = price

    def _set_delta(self, mock_time:float=None) -> None:
        now = time.time() if mock_time is None else mock_time
        self._time_delta = (now - self._current_time)
        self._current_time = now

    @property
    def readings(self) -> list:
        return self._readings

    @property
    def total_price(self) -> float:
        return self._total_price

    @total_price.setter
    def total_price(self, val):
        self.total_price = val

