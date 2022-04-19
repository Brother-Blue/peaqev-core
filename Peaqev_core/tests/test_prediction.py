import pytest
import Prediction as p


def test_prediction():
       ret = p.PredictionBase.predictedenergy(
       nowmin=13,
       nowsec=37,
       poweravg=420,
       totalhourlyenergy=0.24
       )

       assert ret == 0.565

# def test_prediction_percentage():
#        ret = p.predictedenergy(
#        nowmin=13,
#        nowsec=37,
#        poweravg=420,
#        totalhourlyenergy=0.24
#        )
#        retperc = p.predictedpercentageofpeak(2, ret)

#        assert retperc == 28.25

# def test_prediction_valueerrors():
#        self.assertRaises(
#               ValueError,
#               p.PredictionBase._predictedenergy,
#               nowmin=60,
#               nowsec=37,
#               poweravg=420,
#               totalhourlyenergy=0.24
#        )
#        self.assertRaises(
#               ValueError,
#               p.PredictionBase._predictedenergy,
#               nowmin=50,
#               nowsec=-1,
#               poweravg=420,
#               totalhourlyenergy=-1
#        )
#        self.assertRaises(ValueError, p.PredictionBase._predictedenergy, nowmin=50, nowsec=-1, poweravg=-1,
#                      totalhourlyenergy=0.05)
#        self.assertRaises(ValueError, p.PredictionBase._predictedenergy, nowmin=50, nowsec=37, poweravg=420,
#                      totalhourlyenergy=-1)


