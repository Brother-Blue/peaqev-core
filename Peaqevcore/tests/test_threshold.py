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
    ret = t.allowedcurrent(
        nowmin=0,
        movingavg=1,
        charger_enabled=False,
        charger_done=False,
        currentsdict=CURRENTS_THREEPHASE_1_32,
        totalenergy=0,
        peak=1
    )
    assert ret == t.BASECURRENT

def test_allowed_current_1():
    ret = t.allowedcurrent(
        nowmin=10,
        movingavg=560,
        charger_enabled=True,
        charger_done=False,
        currentsdict=CURRENTS_THREEPHASE_1_32,
        totalenergy=0.3,
        peak=10
    )
    assert ret == 16

def test_allowed_current_2():
    ret = t.allowedcurrent(
        nowmin=50,
        movingavg=560,
        charger_enabled=True,
        charger_done=False,
        currentsdict=CURRENTS_THREEPHASE_1_32,
        totalenergy=0.3,
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