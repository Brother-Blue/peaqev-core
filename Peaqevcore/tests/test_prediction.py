import pytest
from Peaqevcore.Prediction import PredictionBase as p

def test_prediction():
       ret = p.predictedenergy(
       nowmin=13,
       nowsec=37,
       poweravg=420,
       totalhourlyenergy=0.24
       )

       assert ret == 0.565

def test_prediction_percentage():
       ret = p.predictedenergy(
       nowmin=13,
       nowsec=37,
       poweravg=420,
       totalhourlyenergy=0.24
       )
       retperc = p.predictedpercentageofpeak(2, ret)

       assert retperc == 28.25

def test_prediction_minute_overflow():
       with pytest.raises(ValueError):
              p.predictedenergy(
              nowmin=60,
              nowsec=37,
              poweravg=420,
              totalhourlyenergy=0.24)

def test_prediction_second_overflow():
       with pytest.raises(ValueError):
              p.predictedenergy(
              nowmin=50,
              nowsec=60,
              poweravg=420,
              totalhourlyenergy=0.24)

def test_prediction_hour_overflow():
       with pytest.raises(ValueError):
              p.predictedenergy(
              nowmin=-5,
              nowsec=37,
              poweravg=420,
              totalhourlyenergy=0.24)

def test_prediction_second_negative():
       with pytest.raises(ValueError):
              p.predictedenergy(
              nowmin=50,
              nowsec=-2,
              poweravg=420,
              totalhourlyenergy=0.24)

def test_prediction_hourlyenergy_negative():
       with pytest.raises(ValueError):
              p.predictedenergy(
              nowmin=50,
              nowsec=4,
              poweravg=420,
              totalhourlyenergy=-0.24)


