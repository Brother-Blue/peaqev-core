from datetime import datetime, date, time
import pytest

from ..locale_service.querytypes.const import QUERYTYPE_AVERAGEOFTHREEDAYS, QUERYTYPE_AVERAGEOFTHREEHOURS, QUERYTYPE_SOLLENTUNA
from ..locale_service.querytypes.querytypes import QUERYTYPES
from ..country_service.sweden import SE_SHE_AB, SE_Bjerke_Energi, SE_Gothenburg, SE_Kristinehamn, SE_Skovde, SE_Sollentuna

def test_SE_Bjerke_Energi():
    p = SE_Bjerke_Energi
    assert p.free_charge(p, mockdt=datetime.combine(date(2005, 7, 14), time(22, 30))) is True
    assert p.free_charge(p, mockdt=datetime.combine(date(2005, 7, 14), time(15,00))) is False
    del(p)

def test_generic_querytype_avg_threedays():
    pt = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
    pt.reset()
    pt.try_update(newval=1.2, timestamp=datetime.combine(date(2022, 7, 14), time(20, 30)))
    pt.try_update(newval=2, timestamp=datetime.combine(date(2022, 7, 14), time(21, 30)))
    to_state_machine = pt.peaks_export
    pt.peaks.set_init_dict(to_state_machine)
    pt.try_update(newval=0.6, timestamp=datetime.combine(date(2022, 7, 15), time(21, 30)))
    assert len(pt.peaks.p) == 2
    assert pt._charged_peak_value == 1.3

def test_generic_querytype_avg_threedays2():
    pg = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
    pg.reset()
    pg.try_update(newval=1.2, timestamp=datetime.combine(date(2022, 7, 14), time(20, 30)))
    pg.try_update(newval=2, timestamp=datetime.combine(date(2022, 7, 14), time(21, 30)))
    assert len(pg.peaks.p) == 1
    assert pg._charged_peak_value == 2

def test_generic_querytype_avg_threedays3():
    to_state_machine = {'m': 7, 'p': {'14h21': 2}}
    p1 = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
    p1.reset()
    p1.try_update(newval=1, timestamp=datetime.combine(date(2022, 7, 15), time(21, 30)))
    p1.peaks.set_init_dict(to_state_machine, datetime.combine(date(2022, 7, 15), time(21, 30)))
    assert len(p1.peaks.p) == 2
    assert p1.charged_peak == 1.5
    assert p1.observed_peak == 1
    p1.try_update(newval=2, timestamp=datetime.combine(date(2022, 7, 15), time(22, 30)))
    assert len(p1.peaks.p) == 2
    assert p1.charged_peak == 2
    assert p1.observed_peak == 2

def test_faulty_number_in_import():
    to_state_machine = {'m': 7, 'p': {'14h21': 2, '11h22': 1.49, '12h9': 1.93, '12h14': 0.73}}
    p1 = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
    p1.reset()
    p1.try_update(newval=1, timestamp=datetime.combine(date(2022, 7, 15), time(21, 30)))
    p1.peaks.set_init_dict(to_state_machine, datetime.combine(date(2022, 7, 15), time(21, 30)))
    assert len(p1.peaks.p) == 3
    assert p1.charged_peak == 1.81
    assert p1.observed_peak == 1.49
    p1.try_update(newval=1.5, timestamp=datetime.combine(date(2022, 7, 15), time(22, 30)))
    assert len(p1.peaks.p) == 3
    assert p1.charged_peak == 1.81
    assert p1.observed_peak == 1.5
    
def test_overridden_number_in_import():
    to_state_machine = {'m': 7, 'p': {'11h22': 1.49, '12h9': 1.93, '13h16': 0.86}}
    p1 = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
    p1.reset()
    p1.try_update(newval=0.22, timestamp=datetime.combine(date(2022, 7, 13), time(21, 30)))
    p1.peaks.set_init_dict(to_state_machine, datetime.combine(date(2022, 7, 13), time(21, 30)))
    print(p1.peaks.p)
    assert p1.charged_peak == 1.43

def test_SE_Gothenburg():
    p = SE_Gothenburg
    assert p.free_charge(p) is False
    p.query_model.try_update(newval=1.2, timestamp=datetime.combine(date(2022, 7, 14), time(22, 30)))
    p.query_model.try_update(newval=1, timestamp=datetime.combine(date(2022, 7, 16), time(22, 30)))
    p.query_model.try_update(newval=1.5, timestamp=datetime.combine(date(2022, 7, 17), time(22, 30)))
    p.query_model.try_update(newval=1.7, timestamp=datetime.combine(date(2022, 7, 17), time(22, 30)))
    p.query_model.try_update(newval=1.5, timestamp=datetime.combine(date(2022, 7, 19), time(22, 30)))
    assert p.query_model.observed_peak > 0
    del(p)

def test_generic_querytype_avg_threehour2s():
    p = SE_Sollentuna
    p.query_model.try_update(newval=1.2, timestamp=datetime.combine(date(2022, 7, 14), time(22, 30)))
    p.query_model.try_update(newval=1, timestamp=datetime.combine(date(2022, 7, 16), time(22, 30)))
    p.query_model.try_update(newval=1.5, timestamp=datetime.combine(date(2022, 7, 17), time(22, 30)))
    p.query_model.try_update(newval=1.7, timestamp=datetime.combine(date(2022, 7, 17), time(22, 30)))
    p.query_model.try_update(newval=1.5, timestamp=datetime.combine(date(2022, 7, 19), time(22, 30)))
    assert p.query_model.observed_peak == 0
    d1 = date(2022, 7, 14)
    t = time(22, 30)
    dt1 = datetime.combine(d1, t)
    p.query_model.try_update(new_val=1.2, dt=dt1)
    d2 = date(2022, 7, 16)
    dt2 = datetime.combine(d2, t)
    p.query_model.try_update(new_val=1, dt=dt2)
    d3 = date(2022, 7, 17)
    dt3 = datetime.combine(d3, t)
    p.query_model.try_update(new_val=1.5, dt=dt3)
    d3 = date(2022, 7, 17)
    dt3 = datetime.combine(d3, t)
    p.query_model.try_update(new_val=1.7, dt=dt3)
    d4 = date(2022, 7, 19)
    dt4 = datetime.combine(d4, t)
    p.query_model.try_update(new_val=1.5, dt=dt4)
    print(p.query_model._peaks)
    print(p.query_model.peaks)


def test_SE_Kristinehamn():
    p = SE_Kristinehamn
    p.query_model.try_update(newval=0.5, timestamp=datetime.combine(date(2022, 6, 14), time(20, 30)))
    assert p.query_model.charged_peak == 0.5
    p.query_model.try_update(newval=1.2, timestamp=datetime.combine(date(2022, 2, 14), time(16, 30)))
    assert p.query_model.charged_peak == 1.2
