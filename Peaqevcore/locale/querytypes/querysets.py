from .const import (
    QUERYTYPE_SOLLENTUNA,
    QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR
    )
from .querytypes_helper import QueryService, Dividents

QUERYSETS = {
    QUERYTYPE_SOLLENTUNA: [
                            {
                                "divident": Dividents.AND,
                                "args": [
                                {
                                    "type": "lteq",
                                    "dttype": "hour",
                                    "values": [7]
                                },
                                {
                                    "type": "lteq",
                                    "dttype": "hour",
                                    "values": [18]
                                },
                                {
                                    "type": "lteq",
                                    "dttype": "weekday",
                                    "values": [4]
                                }
                                ]
                            }
                        ]
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

# QUERYSETS = {
#     QUERYTYPE_SOLLENTUNA: 
#                 lambda: QueryService(
#                     QueryService.group(
#                         Dividents.AND,
#                         QueryService.datepart("gteq", "hour", 7),
#                         QueryService.datepart("lteq", "hour", 18),
#                         QueryService.datepart("lteq", "weekday", 4)
#                         )
#                     ),
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

