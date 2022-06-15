from datetime import datetime, date, time
import pytest

from ..locale.querytypes.const import QUERYTYPE_AVERAGEOFTHREEDAYS, QUERYTYPE_AVERAGEOFTHREEHOURS, QUERYTYPE_SOLLENTUNA
from ..locale.querytypes.querytypes import QUERYTYPES
from ..country.sweden import SE_Bjerke_Energi, SE_Gothenburg, SE_Sollentuna

def test_SE_Bjerke_Energi():
    p = SE_Bjerke_Energi
    assert p.free_charge(p, mockdt=datetime.combine(date(2005, 7, 14), time(22, 30))) is True
    assert p.free_charge(p, mockdt=datetime.combine(date(2005, 7, 14), time(15,00))) is False
    del(p)

def test_generic_querytype_avg_threedays():
    pt = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
    pt.reset()
    pt.try_update(newval=1.2, dt=datetime.combine(date(2022, 7, 14), time(20, 30)))
    pt.try_update(newval=2, dt=datetime.combine(date(2022, 7, 14), time(21, 30)))
    to_state_machine = pt.peaks_export
    pt.peaks.set_init_dict(to_state_machine)
    pt.try_update(newval=0.6, dt=datetime.combine(date(2022, 7, 15), time(21, 30)))
    assert len(pt.peaks.p) == 2
    assert pt._charged_peak_value == 1.3

def test_generic_querytype_avg_threedays2():
    pg = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
    pg.reset()
    pg.try_update(newval=1.2, dt=datetime.combine(date(2022, 7, 14), time(20, 30)))
    pg.try_update(newval=2, dt=datetime.combine(date(2022, 7, 14), time(21, 30)))
    assert len(pg.peaks.p) == 1
    assert pg._charged_peak_value == 2

def test_generic_querytype_avg_threedays3():
    to_state_machine = {'m': 7, 'p': {'14h21': 2}}
    p1 = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
    p1.reset()
    p1.try_update(newval=1, dt=datetime.combine(date(2022, 7, 15), time(21, 30)))
    p1.peaks.set_init_dict(to_state_machine, datetime.combine(date(2022, 7, 15), time(21, 30)))
    assert len(p1.peaks.p) == 2
    assert p1.charged_peak == 1.5
    assert p1.observed_peak == 1
    p1.try_update(newval=2, dt=datetime.combine(date(2022, 7, 15), time(22, 30)))
    assert len(p1.peaks.p) == 2
    assert p1.charged_peak == 2
    assert p1.observed_peak == 2

def test_faulty_number_in_import():
    to_state_machine = {'m': 7, 'p': {'14h21': 2, '11h22': 1.49, '12h9': 1.93, '12h14': 0.73}}
    p1 = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
    p1.reset()
    p1.try_update(newval=1, dt=datetime.combine(date(2022, 7, 15), time(21, 30)))
    p1.peaks.set_init_dict(to_state_machine, datetime.combine(date(2022, 7, 15), time(21, 30)))
    #print(len(p1.peaks.p))
    #print(p1.peaks.p)
    assert len(p1.peaks.p) == 3
    #print(p1.charged_peak)
    assert p1.charged_peak == 1.81
    #print(p1.observed_peak)
    assert p1.observed_peak == 1.49
    p1.try_update(newval=1.5, dt=datetime.combine(date(2022, 7, 15), time(22, 30)))
    #print(len(p1.peaks.p))
    #print(p1.peaks.p)
    assert len(p1.peaks.p) == 3
    #print(p1.charged_peak)
    assert p1.charged_peak == 1.81
    #print(p1.observed_peak)
    assert p1.observed_peak == 1.5
    
def test_overridden_number_in_import():
    to_state_machine = {'m': 7, 'p': {'11h22': 1.49, '12h9': 1.93, '13h16': 0.86}}
    p1 = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
    p1.reset()
    p1.try_update(newval=0.22, dt=datetime.combine(date(2022, 7, 13), time(21, 30)))
    p1.peaks.set_init_dict(to_state_machine, datetime.combine(date(2022, 7, 13), time(21, 30)))
    print(p1.peaks.p)
    assert p1.charged_peak == 1.43

def test_SE_Gothenburg():
    p = SE_Gothenburg
    assert p.converted
    assert p.free_charge(p) is False
    p.query_model.try_update(newval=1.2, dt=datetime.combine(date(2022, 7, 14), time(22, 30)))
    p.query_model.try_update(newval=1, dt=datetime.combine(date(2022, 7, 16), time(22, 30)))
    p.query_model.try_update(newval=1.5, dt=datetime.combine(date(2022, 7, 17), time(22, 30)))
    p.query_model.try_update(newval=1.7, dt=datetime.combine(date(2022, 7, 17), time(22, 30)))
    p.query_model.try_update(newval=1.5, dt=datetime.combine(date(2022, 7, 19), time(22, 30)))
    assert p.query_model.observed_peak > 0
    del(p)

# def test_generic_querytype_avg_threehours():
#     p2 = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEHOURS]
#     p2.try_update(newval=1.2, dt=datetime.combine(date(2022, 7, 14), time(20, 30)))
#     p2.try_update(newval=2, dt=datetime.combine(date(2022, 7, 14), time(21, 30)))
#     assert len(p2._peaks.p) == 2
#     del(p2)

def test_generic_querytype_avg_threehour2s():
    p = SE_Sollentuna
    assert p.converted
    # p.query_model.try_update(newval=1.2, dt=datetime.combine(date(2022, 7, 14), time(22, 30)))
    # p.query_model.try_update(newval=1, dt=datetime.combine(date(2022, 7, 16), time(22, 30)))
    # p.query_model.try_update(newval=1.5, dt=datetime.combine(date(2022, 7, 17), time(22, 30)))
    # p.query_model.try_update(newval=1.7, dt=datetime.combine(date(2022, 7, 17), time(22, 30)))
    # p.query_model.try_update(newval=1.5, dt=datetime.combine(date(2022, 7, 19), time(22, 30)))
    #assert p.query_model.observed_peak == 0
    p.query_model.try_update(newval=1.5, dt=datetime.combine(date(2022, 6, 15), time(15, 30)))
    assert p.query_model.observed_peak == 1.5
    del(p)

    # p2 = QUERYTYPES[QUERYTYPE_SOLLENTUNA]
    # p2.try_update(newval=1.2, dt=datetime.combine(date(2022, 7, 14), time(15, 30)))
    # p2.try_update(newval=2, dt=datetime.combine(date(2022, 7, 14), time(20, 30)))
    # p2.try_update(newval=2, dt=datetime.combine(date(2022, 7, 14), time(21, 30)))
    # assert len(p2._peaks.p) == 1
    # del(p2)