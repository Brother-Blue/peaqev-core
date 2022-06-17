from .models.queryservice_model import queryservicemodel, group, datepart_model
from .const import (
    QUERYTYPE_AVERAGEOFTHREEHOURS_MON_FRI_07_19,
    QUERYTYPE_MAX_NOV_MAR_MON_FRI_06_22,
    QUERYTYPE_SOLLENTUNA,
    QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR
    )
from .queryservice import Dividents

QUERYSETS = {
    QUERYTYPE_SOLLENTUNA: queryservicemodel(
    [group(divident=Dividents.AND, dateparts=[
        datepart_model(type="gteq", dttype="hour", values=[7]),
        datepart_model(type="lteq", dttype="hour", values=[18]),
        datepart_model(type="lteq", dttype="weekday", values=[4])
        ]
        )
    ]
    ),
    QUERYTYPE_MAX_NOV_MAR_MON_FRI_06_22: queryservicemodel(
    [group(divident=Dividents.AND, dateparts=[
        datepart_model(type="gteq", dttype="hour", values=[6]),
        datepart_model(type="lteq", dttype="hour", values=[22]),
        datepart_model(type="lteq", dttype="weekday", values=[4]),
        datepart_model(type="in", dttype="month", values=[11, 12, 1, 2, 3])
        ]
        )
    ]
    ),
    QUERYTYPE_AVERAGEOFTHREEHOURS_MON_FRI_07_19: queryservicemodel(
    [group(divident=Dividents.AND, dateparts=[
        datepart_model(type="in", dttype="hour", values=[7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]),
        datepart_model(type="lteq", dttype="weekday", values=[4])
        ]
        )
    ]
    )
}

                        # ,
#     QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR: 
#                 QueryService(
#                         QueryService.group(
#                             Dividents.AND,
#                             QueryService.datepart("lteq", "weekday", 4),
#                             QueryService.datepart("in", "hour", 7, 8, 9, 10, 11, 12, 13, 14, 15, 16),
#                             QueryService.datepart("in", "month", 12, 1, 2, 3)
#                         ),
#                         QueryService.group(
#                         Dividents.OR,
#                         QueryService.datepart("in", "month", 4, 5, 6, 7, 8, 9, 10, 11)
#                     )
#                 )
# }
