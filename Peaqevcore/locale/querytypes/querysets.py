from .const import QUERYTYPE_SOLLENTUNA
from .querytypes_helper import QueryService as Q

QUERYSETS = {
    QUERYTYPE_SOLLENTUNA: 
                Q.query(
                    Q.AND,
                    Q.datepart("gteq", "hour", 7),
                    Q.AND,
                    Q.datepart("lteq", "hour", 18),
                    Q.AND,
                    Q.datepart("lteq", "weekday", 4)
                )
}