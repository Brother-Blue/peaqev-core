from datetime import datetime, date, time
import pytest
from ..locale_service.types.sweden import SE_Bjerke_Energi

def test_SE_Bjerke_Energi():
    p = SE_Bjerke_Energi
    d = date(2005, 7, 14)
    t = time(22, 30)
    dt = datetime.combine(d, t)
    assert p.free_charge(p, mockdt=dt) is True
    t2 = time(15,00)
    dt2 = datetime.combine(d, t2)
    assert p.free_charge(p, mockdt=dt2) is False


