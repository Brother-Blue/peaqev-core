from ..session import SessionPrice
import pytest

def test_session_fluctuate():
    s = SessionPrice()
    timer = 1651607299
    s._set_delta(timer)
    s.update_price(0.6, timer)
    s.update_power_reading(6000, timer)    
    timer += 1200
    s.update_price(0.3, timer)
    s.update_power_reading(3000, timer)    
    timer += 1200    
    s.terminate(timer)
    assert s.total_power == 3
    assert round(s.total_price,4) == 1.5

def test_session_fluctuate_tenfold():
    s = SessionPrice()
    timer = 1651607299
    s._set_delta(timer)
    s.update_price(6, timer)
    s.update_power_reading(6000, timer)    
    timer += 1200
    s.update_price(3, timer)
    s.update_power_reading(3000, timer)    
    timer += 1200    
    s.terminate(timer)
    assert s.total_power == 3
    assert round(s.total_price,4) == 15

def test_session_split_price():
    s = SessionPrice()
    timer = 1651607299
    s._set_delta(timer)
    s.update_price(2, timer)
    s.update_power_reading(2000, timer)
    timer += 900
    s.update_price(3, timer)
    timer += 900
    s.update_power_reading(1000, timer)
    timer += 1800
    s.terminate(timer)

    assert s.total_power == 1.5
    assert s.total_price == 4


def test_session_full_hour():
    s = SessionPrice()
    timer = 1651607299
    s._set_delta(timer)
    s.update_price(1, timer)
    s.update_power_reading(1000, timer)
    timer += 3600
    s.update_power_reading(1000, timer)
    s.terminate(timer)
    assert s.total_power == 1
    assert s.total_price == 1

def test_session_half_hour():
    s = SessionPrice()
    timer = 1651607299
    s._set_delta(timer)
    s.update_price(1, timer)
    s.update_power_reading(1000, timer)
    timer += 1800
    s.update_power_reading(1000, timer)
    s.terminate(timer)
    assert s.total_power == 0.5
    assert s.total_price == 0.5

def test_session_with_zero_periods():
    s = SessionPrice()
    timer = 1651607299
    s._set_delta(timer)
    s.update_price(2, timer)
    s.update_power_reading(4000, timer)
    timer += 900
     #2kr
    s.update_power_reading(0, timer) 
    timer += 900
     #2kr
    s.update_price(3, timer)
    timer += 900
     #2kr
    s.update_power_reading(1000, timer)
    timer += 1800
     #3.5kr
    s.terminate(timer)

    assert s.total_power == 1.5
    assert s.total_price == 3.5

def test_session_with_zero_periods_price_update_in_between():
    s = SessionPrice()
    timer = 1651607299
    s._set_delta(timer)
    s.update_price(2, timer)
    s.update_power_reading(4000, timer)
    timer += 900
     #2kr
    s.update_price(3, timer)
    timer += 900
    #5kr
    s.update_power_reading(0, timer) 
    timer += 900
     #5kr
    s.update_power_reading(1000, timer)
    timer += 1800
     #6.5kr
    s.terminate(timer)

    assert s.total_power == 2.5
    assert s.total_price == 6.5

def test_session_get_status():
    s = SessionPrice()
    timer = 1651607299
    s._set_delta(timer)
    s.update_price(2, timer)
    s.update_power_reading(4000, timer)
    timer += 900
    status = s.get_status()
    assert status["price"] == 0
    s.update_price(3, timer)
    timer += 900
    status = s.get_status()
    assert status["price"] == 2
    s.update_power_reading(0, timer) 
    timer += 900
    status = s.get_status()
    assert status["price"] == 5
     #5kr
    s.update_power_reading(1000, timer)
    timer += 1800
    status = s.get_status()
    assert status["price"] == 5
    assert status["energy"]["value"] == 2
    s.terminate(timer)

    assert s.total_power == 2.5
    assert s.total_price == 6.5



