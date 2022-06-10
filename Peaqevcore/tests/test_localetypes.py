from datetime import datetime, date, time
import pytest
from ..sweden import SE_Bjerke_Energi, SE_Gothenburg

def test_SE_Bjerke_Energi():
    p = SE_Bjerke_Energi
    d = date(2005, 7, 14)
    t = time(22, 30)
    dt = datetime.combine(d, t)
    assert p.free_charge(p, mockdt=dt) is True
    t2 = time(15,00)
    dt2 = datetime.combine(d, t2)
    assert p.free_charge(p, mockdt=dt2) is False


def test_SE_Gothenburg():
    p = SE_Gothenburg
    assert p.converted
    assert p.free_charge(p) is False
    assert p.query_model.observed_peak == 0
    # d = date(2005, 7, 14)
    # t = time(22, 30)
    # dt = datetime.combine(d, t)
    # assert p.free_charge(p, mockdt=dt) is True
    # t2 = time(15,00)
    # dt2 = datetime.combine(d, t2)
    # assert p.free_charge(p, mockdt=dt2) is False


