from datetime import datetime, date, time
import pytest

from peaqevcore.locale.querytypes import QUERYTYPE_AVERAGEOFTHREEDAYS, QUERYTYPE_AVERAGEOFTHREEHOURS, QUERYTYPES
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

def test_generic_querytype_avg_threedays():
    p1 = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
    d11 = date(2022, 7, 14)
    t11 = time(20, 30)
    dt11 = datetime.combine(d11, t11)
    p1.try_update(newval=1.2, dt=dt11)
    d21 = date(2022, 7, 14)
    t21 = time(21, 30)
    dt21 = datetime.combine(d21, t21)
    p1.try_update(newval=2, dt=dt21)
    assert len(p1._peaks.p) == 1

def test_SE_Gothenburg():
    p = SE_Gothenburg
    assert p.converted
    assert p.free_charge(p) is False
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
    assert p.query_model.observed_peak > 0

def test_generic_querytype_avg_threehours():
    p2 = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEHOURS]
    d1 = date(2022, 7, 14)
    t = time(20, 30)
    dt1 = datetime.combine(d1, t)
    p2.try_update(newval=1.2, dt=dt1)
    d2 = date(2022, 7, 14)
    t2 = time(21, 30)
    dt2 = datetime.combine(d2, t2)
    p2.try_update(newval=2, dt=dt2)
    assert len(p2._peaks.p) == 2
