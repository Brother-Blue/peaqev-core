from datetime import datetime
from .models.enums import Dividents
from .models.queryservice_model import queryservicemodel as model

class QueryService:
    def __init__(self, args: model=model()):
        self._settings = args
    
    def should_register_peak(self, dt: datetime) -> bool:
        main_ret = []
        main_grouping = (s for s in self._settings.groups if s.divident is not Dividents.UNSET)
        print("hej2")
        for s in main_grouping:
            group_ret = []
            grouping = (a for a in s.dateparts if len(a.values) > 0)
            for a in grouping:
                group_ret.append(QueryService.datepart(a.type, a.dttype, a.values, dt))
            if s.divident is Dividents.AND:
                main_ret.append(all(group_ret))
            else:
                main_ret.append(any(group_ret))
        return any(main_ret) if len(main_ret) > 0 else True

    @staticmethod
    def datepart(logic: str, dtpart: str, args: list[int], timer: datetime) -> bool:
        if not args:
            return True
        arg = args if len(args) > 1 else args[0]
        _logic = QueryService.LOGIC.get(logic)(
            QueryService.DATETIMEPARTS.get(dtpart)(timer), 
            arg
            )
        print(f"{dtpart}: {_logic}. datetime: {timer}")
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










