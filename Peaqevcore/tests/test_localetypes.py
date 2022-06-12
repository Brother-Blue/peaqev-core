from datetime import datetime, date, time
import pytest
from ..country.sweden import SE_Bjerke_Energi, SE_Gothenburg

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
    d1 = date(2022, 7, 14)
    t = time(22, 30)
    dt1 = datetime.combine(d1, t)
    p.query_model.try_update(newval=1.2, dt=dt1)
    d2 = date(2022, 7, 16)
    dt2 = datetime.combine(d2, t)
    p.query_model.try_update(newval=1, dt=dt2)
    d3 = date(2022, 7, 17)
    dt3 = datetime.combine(d3, t)
    p.query_model.try_update(newval=1.5, dt=dt3)
    d3 = date(2022, 7, 17)
    dt3 = datetime.combine(d3, t)
    p.query_model.try_update(newval=1.7, dt=dt3)
    d4 = date(2022, 7, 19)
    dt4 = datetime.combine(d4, t)
    p.query_model.try_update(newval=1.5, dt=dt4)
    print(p.query_model._peaks)
    print(p.query_model.peaks)


