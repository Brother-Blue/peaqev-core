from enum import Enum

class CHARGERSTATES(Enum):
    Idle = 0
    Connected = 1
    Start = 2
    Stop = 3
    Done = 4
    Error = 5
    Charging = 6


CURRENTS_ONEPHASE_1_16 = {3600: 16, 3150: 14, 2700: 12, 2250: 10, 1800: 8, 1350: 6}
CURRENTS_THREEPHASE_1_16 = {11000: 16, 9625: 14, 8250: 12, 6875: 10, 5500: 8, 4100: 6}

CURRENTS_ONEPHASE_1_32 = {7200: 32, 6750: 30, 6300: 28, 5850: 26, 5400: 24, 4950: 22, 4500: 20, 4050: 18, 3600: 16, 3150: 14, 2700: 12, 2250: 10, 1800: 8, 1350: 6}
CURRENTS_THREEPHASE_1_32 = {22000: 32, 20625: 30, 19250: 28, 17875: 26, 16500: 24, 15125: 22, 13750: 20, 12375: 18, 11000: 16, 9625: 14, 8250: 12, 6875: 10, 5500: 8, 4100: 6}

CAUTIONHOURTYPE_SUAVE = "Suave"
CAUTIONHOURTYPE_INTERMEDIATE = "Intermediate"
CAUTIONHOURTYPE_AGGRESSIVE = "Aggressive"

CAUTIONHOURTYPE = {
    CAUTIONHOURTYPE_SUAVE: 0.4,
    CAUTIONHOURTYPE_INTERMEDIATE: 0.5,
    CAUTIONHOURTYPE_AGGRESSIVE: 0.8
}