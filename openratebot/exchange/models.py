from dataclasses import dataclass
from datetime import date
from decimal import Decimal
@dataclass(frozen=True)
class RateQuote:
    date: date; base: str; quote: str; rate: Decimal
@dataclass(frozen=True)
class CurrencyInfo:
    code: str; name: str; symbol: str|None=None
