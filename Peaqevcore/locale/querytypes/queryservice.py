from datetime import date, datetime, time
from dataclasses import dataclass
from .models.enums import Dividents, SumTypes, TimePeriods
from .models.queryservice_model import queryservicemodel as model

class QueryService:
    DT = datetime.now()
    def __init__(self, args:model = model()):
        self._settings = args
    
    def should_register_peak(self, dt:datetime) -> bool:
        DT = dt
        mainret = []
        maingrouping = (s for s in self._settings.groups if s.divident is not Dividents.UNSET)
        for s in maingrouping:
            groupret = []
            grouping = (a for a in s.dateparts if len(a.values) > 0)
            for a in grouping:
                groupret.append(QueryService.datepart(a.type, a.dttype, a.values))
            if s.divident is Dividents.AND:
                mainret.append(all(groupret))
            else:
                mainret.append(any(groupret))
        return any(mainret) if len(mainret) > 0 else True

    @staticmethod
    def datepart(logic: str, dtpart: str, args: list[int]) -> bool:
        if len(args) == 0:
            return True
        _arg = args if len(args) > 1 else args[0]
        _logic = QueryService.LOGIC[logic](
            QueryService.DATETIMEPARTS[dtpart](QueryService.DT), 
            _arg
            )
        return _logic

    AND = "AND"
    OR = "OR"
    LOGIC = {
        "eq": lambda a, dtp : dtp == a,
        "lt": lambda a, dtp : a < dtp,
        "gt": lambda a, dtp : a > dtp,
        "not": lambda a, dtp : dtp != a,
        "lteq": lambda a, dtp : a <= dtp,
        "gteq": lambda a, dtp : a >= dtp,
        "in": lambda a, dtp : a in dtp
    }
    DATETIMEPARTS = {
        "weekday": lambda d : d.weekday(),
        "month":  lambda d : d.month,
        "hour":  lambda d : d.hour,
    }










