from ..Threshold import ThresholdBase as t
from ..Models import CURRENTS_THREEPHASE_1_32
import pytest

def test_start():
    ret = t.start(50, False)
    assert ret == 83.49

def test_start_caution_non_caution_late():
    ret = t.start(50, False)
    ret2 = t.start(50, True)
    assert ret == ret2

def test_start_caution_non_caution_early():
    ret = t.start(40, False)
    ret2 = t.start(40, True)
    assert ret > ret2

def test_stop():
    ret = t.stop(13, False)
    assert ret == 82.55

def test_stop_caution_non_caution_late():
    ret = t.stop(50, False)
    ret2 = t.stop(50, True)
    assert ret == ret2

def test_stop_caution_non_caution_early():
    ret = t.stop(40, False)
    ret2 = t.stop(40, True)
    assert ret > ret2
    
def test_allowed_current_base():
    ret = t.allowed_current(
        now_min=0,
        moving_avg=1,
        charger_enabled=False,
        charger_done=False,
        currents_dict=CURRENTS_THREEPHASE_1_32,
        total_energy=0,
        peak=1
    )
    assert ret == t.BASECURRENT

def test_allowed_current_1():
    ret = t.allowed_current(
        now_min=10,
        moving_avg=560,
        charger_enabled=True,
        charger_done=False,
        currents_dict=CURRENTS_THREEPHASE_1_32,
        total_energy=0.3,
        peak=10
    )
    assert ret == 16

def test_allowed_current_2():
    ret = t.allowed_current(
        now_min=50,
        moving_avg=560,
        charger_enabled=True,
        charger_done=False,
        currents_dict=CURRENTS_THREEPHASE_1_32,
        total_energy=0.3,
        peak=10
    )
    assert ret == 32


def test_start_quarterly():
    ret = t.start(50, False, True)
    assert ret == 60.62

def test_start_quarterly_caution():
    ret = t.start(50, True, True)
    assert ret == 52.13

def test_stop_quarterly():
    ret = t.start(22, False, True)
    assert ret == 65.29

def test_stop_quarterly_caution():
    ret = t.start(22, True, True)
    assert ret == 58.06