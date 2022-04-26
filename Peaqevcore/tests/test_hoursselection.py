import pytest
from ..hoursselection import Hoursselectionbase as h

MOCKPRICES1 =[0.129, 0.123, 0.077, 0.064, 0.149, 0.172, 1, 2.572, 2.688, 2.677, 2.648, 2.571, 2.561, 2.07, 2.083, 2.459, 2.508, 2.589, 2.647, 2.648, 2.603, 2.588, 1.424, 0.595]
MOCKPRICES2 =[0.392, 0.408, 0.418, 0.434, 0.408, 0.421, 0.45, 0.843, 0.904, 1.013, 0.939, 0.915, 0.703, 0.445, 0.439, 0.566, 0.913, 1.4, 2.068, 2.182, 1.541, 2.102, 1.625, 1.063]
MOCKPRICES3 = [0.243, 0.282, 0.279, 0.303, 0.299, 0.314, 0.304, 0.377, 0.482, 0.484, 0.482, 0.268, 0.171, 0.174, 0.171, 0.277, 0.52, 0.487, 0.51, 0.487, 0.451, 0.397, 0.331, 0.35]

def test_mockprices1_non_hours():
    r = h()
    r.prices = MOCKPRICES1
    r.update()

    assert r.non_hours == [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

def test_mockprices1_caution_hours():
    r = h()
    r.prices = MOCKPRICES1
    r.update()
        
    assert r.caution_hours == [6, 22, 23]

def test_mockprices2_non_hours():
    r = h()
    r.prices = MOCKPRICES2
    r.update()

    assert r.non_hours == [17, 18, 19, 20, 21, 22]

def test_mockprices2_caution_hours():
    r = h()
    r.prices = MOCKPRICES2
    r.update()
        
    assert r.caution_hours == [9, 10, 11, 16, 23]

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
