from .const import (
    QUERYTYPE_SOLLENTUNA,
    QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR
    )
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
                ),
    QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR: 
            Q.query(
                    Q.group(
                        Q.group(
                            Q.AND,
                            Q.datepart("lteq", "weekday", 4),
                            Q.AND,
                            Q.datepart("in", "hour", 7, 8, 9, 10, 11, 12, 13, 14, 15, 16),
                            Q.AND,
                            Q.datepart("in", "month", 12, 1, 2, 3)
                        ),
                        Q.OR,
                        Q.datepart("in", "month", 4, 5, 6, 7, 8, 9, 10, 11)
                    )
                )
}