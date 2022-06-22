from dataclasses import dataclass
from datetime import datetime
from typing import List

from .querytypes.const import (
HOURLY,
QUARTER_HOURLY
)

from .querytypes.querytypes import(
LocaleQuery
)

@dataclass(frozen=True)
class Locale_Type:
    observed_peak: str
    charged_peak: str
    query_model: LocaleQuery
    free_charge_pattern: List = None
    peak_cycle: str = HOURLY
    converted: bool = False #transition key to remove sql-dependency

    def free_charge(self, mockdt: datetime=datetime.min) -> bool:
        if self.free_charge_pattern is None or len(self.free_charge_pattern) == 0:
            return False

        now = datetime.now() if mockdt is datetime.min else mockdt
        for p in self.free_charge_pattern:
            if now.month in p.get("M"):
                if now.weekday() in p.get("D"):
                    if now.hour in p.get("H"):
                        return True
        return False

    def is_quarterly(self) -> bool:
        return self.peak_cycle == QUARTER_HOURLY


