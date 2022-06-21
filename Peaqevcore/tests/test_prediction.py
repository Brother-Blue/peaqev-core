from ..Prediction import PredictionBase as p
import pytest

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

# def test_prediction_hourlyenergy_negative():
#        with pytest.raises(ValueError):
#               p.predictedenergy(
#               nowmin=50,
#               nowsec=4,
#               poweravg=420,
#               totalhourlyenergy=-0.24)


def test_prediction_quarterly():
       ret = p.predictedenergy(
       nowmin=13,
       nowsec=37,
       poweravg=420,
       totalhourlyenergy=0.24,
       is_quarterly=True
       )

       ret2 = p.predictedenergy(
       nowmin=28,
       nowsec=37,
       poweravg=420,
       totalhourlyenergy=0.24,
       is_quarterly=True
       )

       ret3 = p.predictedenergy(
       nowmin=28,
       nowsec=0,
       poweravg=420,
       totalhourlyenergy=0.24,
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