import pytest
from ..hoursselection import Hoursselectionbase as h
from ..Models import (CAUTIONHOURTYPE_AGGRESSIVE, CAUTIONHOURTYPE_INTERMEDIATE, CAUTIONHOURTYPE_SUAVE, CAUTIONHOURTYPE)

MOCKPRICES1 =[0.129, 0.123, 0.077, 0.064, 0.149, 0.172, 1, 2.572, 2.688, 2.677, 2.648, 2.571, 2.561, 2.07, 2.083, 2.459, 2.508, 2.589, 2.647, 2.648, 2.603, 2.588, 1.424, 0.595]
MOCKPRICES2 =[0.392, 0.408, 0.418, 0.434, 0.408, 0.421, 0.45, 0.843, 0.904, 1.013, 0.939, 0.915, 0.703, 0.445, 0.439, 0.566, 0.913, 1.4, 2.068, 2.182, 1.541, 2.102, 1.625, 1.063]
MOCKPRICES3 = [0.243, 0.282, 0.279, 0.303, 0.299, 0.314, 0.304, 0.377, 0.482, 0.484, 0.482, 0.268, 0.171, 0.174, 0.171, 0.277, 0.52, 0.487, 0.51, 0.487, 0.451, 0.397, 0.331, 0.35]
MOCKPRICES_FLAT = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
MOCKPRICES_SHORT = [0.51, 0.487, 0.451, 0.397, 0.331, 0.35]

def test_mockprices1_non_hours():
    r = h()
    r.prices = MOCKPRICES1
    r.update()
    assert r.non_hours == [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

def test_mockprices1_caution_hours():
    r = h()
    r.prices = MOCKPRICES1
    r.update()
    assert r.caution_hours == []

def test_mockprices1_caution_hours_aggressive():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_AGGRESSIVE])
    r.prices = MOCKPRICES1
    r.update()
    assert r.caution_hours == []

def test_mockprices1_caution_hours_per_type():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_AGGRESSIVE])
    r.prices = MOCKPRICES1
    r.update()
    r2 = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_INTERMEDIATE])
    r2.prices = MOCKPRICES1
    r2.update()
    r3 = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    r3.prices = MOCKPRICES1
    r3.update()

    assert len(r.caution_hours) < len(r2.caution_hours)
    assert len(r2.caution_hours) < len(r3.caution_hours)
    assert len(r.non_hours) > len(r2.non_hours)
    assert len(r2.non_hours) > len(r3.non_hours)
    
def test_mockprices2_caution_hours_per_type():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_AGGRESSIVE])
    r.prices = MOCKPRICES2
    r.update()
    r2 = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_INTERMEDIATE])
    r2.prices = MOCKPRICES2
    r2.update()
    r3 = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    r3.prices = MOCKPRICES2
    r3.update()

    assert len(r.caution_hours) < len(r2.caution_hours)
    assert len(r2.caution_hours) == len(r3.caution_hours)
    assert len(r.non_hours) > len(r2.non_hours)
    assert len(r2.non_hours) == len(r3.non_hours)

def test_mockprices3_caution_hours_per_type():
    r = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_AGGRESSIVE])
    r.prices = MOCKPRICES3
    r.update()
    r2 = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_INTERMEDIATE])
    r2.prices = MOCKPRICES3
    r2.update()
    r3 = h(cautionhour_type=CAUTIONHOURTYPE[CAUTIONHOURTYPE_SUAVE])
    r3.prices = MOCKPRICES3
    r3.update()

    assert len(r.caution_hours) == len(r2.caution_hours)
    assert len(r2.caution_hours) == len(r3.caution_hours)
    assert len(r.non_hours) == len(r2.non_hours)
    assert len(r2.non_hours) == len(r3.non_hours)
    
def test_mockprices2_non_hours():
    r = h()
    r.prices = MOCKPRICES2
    r.update()
    assert r.non_hours == [9, 10, 11, 16, 17, 18, 19, 20, 21, 22, 23]

def test_mockprices2_caution_hours():
    r = h()
    r.prices = MOCKPRICES2
    r.update()
    assert r.caution_hours == []

def test_mockprices3_non_hours():
    r = h()
    r.prices = MOCKPRICES3
    r.update()
    assert r.non_hours == [8, 9, 10, 16, 17, 18,19]

def test_mockprices3_caution_hours():
    r = h()
    r.prices = MOCKPRICES3
    r.update()
    assert r.caution_hours == []

def test_cautionhour_over_max_error():
    with pytest.raises(AssertionError):
        h(cautionhour_type=2)
    
def test_cautionhour_zero_error():
    with pytest.raises(AssertionError):
        h(cautionhour_type=0)

def test_cautionhour_negative_error():
    with pytest.raises(AssertionError):
        h(cautionhour_type=-1)

def test_create_dict():
    r = h()
    ret = r._create_dict(MOCKPRICES1)
    assert ret[20] == 2.603
    assert len(ret) == 24

def test_create_dict_error():
    r = h()
    with pytest.raises(ValueError):
              r._create_dict(MOCKPRICES_SHORT)

def test_rank_prices():
    r = h()
    hourly = r._create_dict(MOCKPRICES1)
    ret = r._rank_prices(hourly)
    assert ret == {6: {'permax': 0.37, 'val': 1}, 7: {'permax': 0.96, 'val': 2.572}, 8: {'permax': 1.0, 'val': 2.688}, 9: {'permax': 1.0, 'val': 2.677},10: {'permax': 0.99, 'val': 2.648},
                    11: {'permax': 0.96, 'val': 2.571}, 12: {'permax': 0.95, 'val': 2.561}, 13: {'permax': 0.77, 'val': 2.07}, 14: {'permax': 0.77, 'val': 2.083}, 
                    15: {'permax': 0.91, 'val': 2.459}, 16: {'permax': 0.93, 'val': 2.508}, 17: {'permax': 0.96, 'val': 2.589}, 18: {'permax': 0.98, 'val': 2.647}, 
                    19: {'permax': 0.99, 'val': 2.648}, 20: {'permax': 0.97, 'val': 2.603}, 21: {'permax': 0.96, 'val': 2.588}, 22: {'permax': 0.53, 'val': 1.424}, 23: {'permax': 0.22, 'val': 0.595}}

def test_rank_prices_permax():
    r = h()
    hourly = r._create_dict(MOCKPRICES1)
    ret = r._rank_prices(hourly)
    for r in ret:
        assert 0 <= ret[r]["permax"] <= 1

def test_rank_prices_flat_curve():
    r = h()
    hourly = r._create_dict(MOCKPRICES_FLAT)
    ret = r._rank_prices(hourly)
    assert ret == {}

def test_add_expensive_non_hours():
    r = h()
    pass

def test_add_expensive_non_hours_flat_curve():
    r = h()
    r._absolute_top_price = 1
    hourly = r._create_dict(MOCKPRICES_FLAT)
    rank = r._rank_prices(hourly)
    r._determine_hours(rank)
    assert len(r.non_hours) == 0
    r._add_expensive_non_hours(hourly)
    assert len(r.non_hours) == 24

def test_add_expensive_non_hours_error():
    r = h()
    pass

def test_determine_hours():
    r = h()
    pass

def test_determine_hours_error():
    r = h()
    pass


