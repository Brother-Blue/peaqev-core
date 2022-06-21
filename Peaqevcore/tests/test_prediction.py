from ..prediction_service.prediction import PredictionBase as p
import pytest

def test_prediction():
       ret = p.predictedenergy(
       now_min=13,
       now_sec=37,
       power_avg=420,
       total_hourly_energy=0.24
       )

       assert ret == 0.565

def test_prediction_percentage():
       ret = p.predictedenergy(
       now_min=13,
       now_sec=37,
       power_avg=420,
       total_hourly_energy=0.24
       )
       retperc = p.predictedpercentageofpeak(2, ret)

       assert retperc == 28.25

def test_prediction_minute_overflow():
       with pytest.raises(ValueError):
              p.predictedenergy(
              now_min=60,
              now_sec=37,
              power_avg=420,
              total_hourly_energy=0.24)

def test_prediction_second_overflow():
       with pytest.raises(ValueError):
              p.predictedenergy(
              now_min=50,
              now_sec=60,
              power_avg=420,
              total_hourly_energy=0.24)

def test_prediction_hour_overflow():
       with pytest.raises(ValueError):
              p.predictedenergy(
              now_min=-5,
              now_sec=37,
              power_avg=420,
              total_hourly_energy=0.24)

def test_prediction_second_negative():
       with pytest.raises(ValueError):
              p.predictedenergy(
              now_min=50,
              now_sec=-2,
              power_avg=420,
              total_hourly_energy=0.24)

def test_prediction_hourlyenergy_negative():
       with pytest.raises(ValueError):
              p.predictedenergy(
              now_min=50,
              now_sec=4,
              power_avg=420,
              total_hourly_energy=-0.24)


def test_prediction_quarterly():
       ret = p.predictedenergy(
       now_min=13,
       now_sec=37,
       power_avg=420,
       total_hourly_energy=0.24,
       is_quarterly=True
       )

       ret2 = p.predictedenergy(
       now_min=28,
       now_sec=37,
       power_avg=420,
       total_hourly_energy=0.24,
       is_quarterly=True
       )

       ret3 = p.predictedenergy(
       now_min=28,
       now_sec=0,
       power_avg=420,
       total_hourly_energy=0.24,
       is_quarterly=True
       )

       assert ret == ret2
       assert ret < ret3

def test_prediction_percentage_neg_poweravg():
       ret = p.predictedenergy(
       nowmin=13,
       nowsec=37,
       poweravg=-420,
       totalhourlyenergy=0.24
       )
       retperc = p.predictedpercentageofpeak(2, ret)

       assert retperc >= 0

def test_prediction_percentage_neg_energy():
       ret = p.predictedenergy(
       nowmin=13,
       nowsec=37,
       poweravg=-420,
       totalhourlyenergy=-0.24
       )
       retperc = p.predictedpercentageofpeak(2, ret)

       assert retperc >= 0

def test_prediction_percentage_neg_energy_and_poweravg():
       ret = p.predictedenergy(
       nowmin=13,
       nowsec=37,
       poweravg=-420,
       totalhourlyenergy=-0.24
       )
       retperc = p.predictedpercentageofpeak(2, ret)

       assert retperc >= 0