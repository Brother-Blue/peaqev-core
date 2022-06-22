from dataclasses import dataclass

@dataclass
class PowerReading:
    price: float
    power: float
    td: float

    @property
    def reading_integral(self):
        return self.power/1000 * (self.td/3600)

    @property
    def reading_cost(self):
        return self.reading_integral * self.price
