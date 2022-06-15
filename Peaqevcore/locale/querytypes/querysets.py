from .const import (
    QUERYTYPE_SOLLENTUNA,
    QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR
    )
from .querytypes_helper import QueryService, Dividents

QUERYSETS = {
    QUERYTYPE_SOLLENTUNA: 
                QueryService.query(
                    QueryService.group(
                        Dividents.AND,
                        QueryService.datepart("gteq", "hour", 7),
                        QueryService.datepart("lteq", "hour", 18),
                        QueryService.datepart("lteq", "weekday", 4)
                        )
                    ),
    QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR: 
            QueryService.query(
                        QueryService.group(
                            Dividents.AND,
                            QueryService.datepart("lteq", "weekday", 4),
                            QueryService.AND,
                            QueryService.datepart("in", "hour", 7, 8, 9, 10, 11, 12, 13, 14, 15, 16),
                            QueryService.AND,
                            QueryService.datepart("in", "month", 12, 1, 2, 3)
                        ),
                        QueryService.group(
                        QueryService.datepart("in", "month", 4, 5, 6, 7, 8, 9, 10, 11)
                    )
                )
}
