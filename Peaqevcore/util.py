def _convert_quarterly_minutes(minute:int, is_quarterly:bool) -> int:
    if is_quarterly is True:
        return (minute%15) * 4
    else:
        return minute