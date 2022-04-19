import pytest
from Peaqevcore.Threshold import ThresholdBase as t

MOCKCURRENTS_DICT = {22000: 32, 20625: 30, 19250: 28, 17875: 26, 16500: 24, 15125: 22, 13750: 20, 12375: 18, 11000: 16, 9625: 14, 8250: 12, 6875: 10, 5500: 8, 4100: 6}

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
        currentsdict=MOCKCURRENTS_DICT,
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
        currentsdict=MOCKCURRENTS_DICT,
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
        currentsdict=MOCKCURRENTS_DICT,
        totalenergy=0.3,
        peak=10
    )
    assert ret == 32