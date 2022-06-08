"""LOCALETYPES"""
LOCALE_SE_GOTHENBURG = "Gothenburg, Sweden"
LOCALE_SE_KARLSTAD = "Karlstad, Sweden"
LOCALE_SE_KRISTINEHAMN = "Kristinehamn, Sweden"
LOCALE_SE_NACKA_NORMAL = "Nacka, Sweden (Normal tariffe)"
#LOCALE_SE_NACKA_TIMEDIFF = "Nacka, Sweden (Time differentiated tariffe)"
LOCALE_SE_PARTILLE = "Partille, Sweden"
LOCALE_DEFAULT = "Other, just want to test"
LOCALE_SE_SALA = "Sala-Heby Energi AB, Sweden"
LOCALE_SE_MALUNG_SALEN = "Malung-Sälen, Sweden (Malungs elverk)"
LOCALE_SE_SKOVDE = "Skövde, Sweden"
LOCALE_SE_SOLLENTUNA = "Sollentuna Energi, Sweden"
LOCALE_BE_VREG = "Belgium (VREG)"
LOCALE_SE_BJERKE_ENERGI = "Bjärke Energi, Sweden"
LOCALE_NO_GLITRE_ENERGI = "Glitre Energi, Norway"
LOCALE_NO_AGDER_ENERGI = "Agder Energi, Norway"
LOCALE_NO_LNETT = "LNett, Norway"
LOCALE_NO_TENSIO = "Tensio, Norway"
LOCALE_SE_LINDE_ENERGI = "Linde Energi, Sweden"

"""Lookup locales for config flow"""
LOCALES = [
    LOCALE_BE_VREG,
    LOCALE_NO_AGDER_ENERGI,
    LOCALE_NO_GLITRE_ENERGI,
    LOCALE_NO_LNETT,
    LOCALE_NO_TENSIO,
    LOCALE_SE_GOTHENBURG,
    LOCALE_SE_KARLSTAD,
    LOCALE_SE_KRISTINEHAMN,
    LOCALE_SE_LINDE_ENERGI,
    LOCALE_SE_MALUNG_SALEN,
    LOCALE_SE_NACKA_NORMAL,
    LOCALE_SE_PARTILLE,
    LOCALE_SE_SALA,
    LOCALE_SE_SKOVDE,
    LOCALE_SE_SOLLENTUNA,
    LOCALE_SE_BJERKE_ENERGI,
    LOCALE_DEFAULT
    ]

"""Peak querytypes"""
QUERYTYPE_BASICMAX = "BasicMax"
QUERYTYPE_AVERAGEOFTHREEDAYS = "AverageOfThreeDays"
QUERYTYPE_AVERAGEOFTHREEHOURS = "AverageOfThreeHours"
QUERYTYPE_AVERAGEOFTHREEDAYS_MIN = "AverageOfThreeDays_Min"
QUERYTYPE_AVERAGEOFTHREEHOURS_MIN = "AverageOfThreeHours_Min"
QUERYTYPE_AVERAGEOFFIVEDAYS = "AverageOfFiveDays"
QUERYTYPE_AVERAGEOFFIVEDAYS_MIN = "AverageOfFiveDays_Min"
QUERYTYPE_HIGHLOAD = "HighLoad"
QUERYTYPE_AVERAGEOFTHREEHOURS_MON_FRI_07_19 = "sala"
QUERYTYPE_AVERAGEOFTHREEHOURS_MON_FRI_07_19_MIN = "sala"
QUERYTYPE_MAX_NOV_MAR_MON_FRI_06_22 = "skövde"
QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR = "kristinehamn"
QUERYTYPE_SOLLENTUNA = "sollentuna"
QUERYTYPE_SOLLENTUNA_MIN = "sollentuna_min"

"""Misc"""
QUARTER_HOURLY = "Quarter hourly"
HOURLY = "Hourly"