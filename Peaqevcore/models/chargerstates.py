from enum import Enum

class CHARGERSTATES(Enum):
    Idle = 0
    Connected = 1
    Start = 2
    Stop = 3
    Done = 4
    Error = 5
    Charging = 6
    Disabled = 7
