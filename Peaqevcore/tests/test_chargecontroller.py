import pytest
from peaqevcore.Chargecontroller import ChargeControllerBase
from Models import CHARGERSTATES

_CHARGERSTATESMOCK = {
    CHARGERSTATES.Idle: ["idle"],
    CHARGERSTATES.Connected: ["connected"],
    CHARGERSTATES.Charging: ["charging"],
}
_NONHOURSMOCK = [5,6,7]

def test_start():
    c = ChargeControllerBase(
        charger_state_translation=_CHARGERSTATESMOCK,
        non_hours=_NONHOURSMOCK
    )

    ret = c.above_stop_threshold(
        predicted_energy=1,
        current_peak=1,
        threshold_stop=0
    )
    
    assert ret is False
