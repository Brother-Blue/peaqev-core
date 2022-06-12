from unittest import mock
import pytest
import time
from ..charging.Chargecontroller import ChargeControllerBase
from ..Models import CHARGERSTATES

_CHARGERSTATESMOCK = {
    CHARGERSTATES.Idle: ["idle"],
    CHARGERSTATES.Connected: ["connected"],
    CHARGERSTATES.Charging: ["charging"],
}
_NONHOURSMOCK = [5,6,7]

# def test_init_chargecontrollerbase_ok():
#     c = ChargeControllerBase(
#         charger_state_translation=_CHARGERSTATESMOCK,
#         non_hours=_NONHOURSMOCK
#     )

#     print(c.latest_charger_start)
#     print(time.time())
#     time.sleep(0.1)
#     assert c.latest_charger_start < time.time()

# def test_init_chargecontrollerbase_init_fail_empty_statesdict():
#     with pytest.raises(AssertionError):
#         ChargeControllerBase(
#         charger_state_translation={},
#         non_hours=_NONHOURSMOCK
#     )

# def test_init_chargecontrollerbase_init_fail_empty_statesdict_type():
#     with pytest.raises(AssertionError):
#         ChargeControllerBase(
#         charger_state_translation={CHARGERSTATES.Idle: []},
#         non_hours=_NONHOURSMOCK
#     )

# def test_done_timeout_override():
#     mocktimeout = 60
#     c = ChargeControllerBase(
#         charger_state_translation=_CHARGERSTATESMOCK,
#         non_hours=_NONHOURSMOCK,
#         timeout= mocktimeout
#     )

#     assert c.done_timeout == mocktimeout

# def test_is_timeout_true():
#     mocktimeout = 2
#     c = ChargeControllerBase(
#         charger_state_translation=_CHARGERSTATESMOCK,
#         non_hours=_NONHOURSMOCK,
#         timeout= mocktimeout
#     )
#     time.sleep(mocktimeout)
    
#     assert c._is_timeout == True

# def test_is_timeout_false():
#     mocktimeout = 2
#     c = ChargeControllerBase(
#         charger_state_translation=_CHARGERSTATESMOCK,
#         non_hours=_NONHOURSMOCK,
#         timeout= mocktimeout
#     )

#     assert c._is_timeout == False

def test_start_threshold_should_start():
    c = ChargeControllerBase(
        charger_state_translation=_CHARGERSTATESMOCK,
        non_hours=_NONHOURSMOCK
    )

    ret = c.below_start_threshold(
        predicted_energy=0.2,
        current_peak=1,
        threshold_start=0.6
    )
    assert ret is True

def test_start_threshold_should_not_start():
    c = ChargeControllerBase(
        charger_state_translation=_CHARGERSTATESMOCK,
        non_hours=_NONHOURSMOCK
    )
    
    ret = c.below_start_threshold(
        predicted_energy=0.8,
        current_peak=1,
        threshold_start=0.6
    )
    assert ret is False

def test_stop_threshold_should_stop():
    c = ChargeControllerBase(
            charger_state_translation=_CHARGERSTATESMOCK,
            non_hours=_NONHOURSMOCK
        )
    ret = c.above_stop_threshold(
        predicted_energy=0.8,
        current_peak=1,
        threshold_stop=0.6
    )
    assert ret is True

def test_stop_threshold_should_not_stop():
    c = ChargeControllerBase(
        charger_state_translation=_CHARGERSTATESMOCK,
        non_hours=_NONHOURSMOCK
    )
    
    ret = c.above_stop_threshold(
        predicted_energy=0.2,
        current_peak=1,
        threshold_stop=0.6
    )
    assert ret is False

def test_stop_threshold_should_not_stop():
    c = ChargeControllerBase(
        charger_state_translation=_CHARGERSTATESMOCK,
        non_hours=_NONHOURSMOCK
    )
    
    ret = c.above_stop_threshold(
        predicted_energy=2,
        current_peak=1.98,
        threshold_stop=60
    )
    assert ret is False

# def test_chargecontroller_is_charging_nonhour():
#     c = ChargeControllerBase(
#         charger_state_translation=_CHARGERSTATESMOCK,
#         non_hours=_NONHOURSMOCK
#     )
    
#     ret = c.get_status(
#         charger_state="charging",
#         charger_enabled=True,
#         charger_done=False,
#         car_power_sensor=50,
#         total_energy_this_hour=0.5,
#         current_hour=6    
#     )
#     assert ret == CHARGERSTATES.Stop

# def test_chargecontroller_is_idle():
#     c = ChargeControllerBase(
#         charger_state_translation=_CHARGERSTATESMOCK,
#         non_hours=_NONHOURSMOCK
#     )
    
#     ret = c.get_status(
#         charger_state="idle",
#         charger_enabled=False,
#         charger_done=False,
#         car_power_sensor=50,
#         total_energy_this_hour=0.5,
#         current_hour=10    
#     )
#     assert ret == CHARGERSTATES.Idle

# def test_chargecontroller_is_connected():
#     c = ChargeControllerBase(
#         charger_state_translation=_CHARGERSTATESMOCK,
#         non_hours=_NONHOURSMOCK
#     )
    
#     ret = c.get_status(
#         charger_state="connected",
#         charger_enabled=False,
#         charger_done=False,
#         car_power_sensor=50,
#         total_energy_this_hour=0.5,
#         current_hour=10    
#     )
#     assert ret == CHARGERSTATES.Connected

# def test_chargecontroller_is_idle_nonhour():
#     c = ChargeControllerBase(
#         charger_state_translation=_CHARGERSTATESMOCK,
#         non_hours=_NONHOURSMOCK
#     )
    
#     ret = c.get_status(
#         charger_state="idle",
#         charger_enabled=False,
#         charger_done=False,
#         car_power_sensor=50,
#         total_energy_this_hour=0.5,
#         current_hour=6    
#     )
#     assert ret == CHARGERSTATES.Idle

# def test_chargecontroller_is_connected_nonhour():
#     c = ChargeControllerBase(
#         charger_state_translation=_CHARGERSTATESMOCK,
#         non_hours=_NONHOURSMOCK
#     )
    
#     ret = c.get_status(
#         charger_state="connected",
#         charger_enabled=False,
#         charger_done=False,
#         car_power_sensor=50,
#         total_energy_this_hour=0.5,
#         current_hour=6    
#     )
#     assert ret == CHARGERSTATES.Connected