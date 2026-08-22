from dataclasses import dataclass
from decimal import Decimal
from numbers import Number

from domain.exceptions import InvalidCurrencyError, InvalidAmountError


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str = 'USD'

    def __post_init__(self):
        currency = self.currency.strip().upper()

        if len(currency) != 3 or not currency.isalpha():
            raise InvalidCurrencyError(f'Currency must be 3 big letter!!')

        if self.amount < 0 or self.amount.is_zero():
            raise InvalidAmountError('Amount cannot be zero or negative!')

    def _ensure_same_currency(self, other: "Money"):
        if self.currency != other.currency:
            raise InvalidCurrencyError(f'Currencies must be the same')

    def __add__(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, number: Number) -> "Money":
        return Money(self.amount * Decimal(str(number)), self.currency)

    def __neg__(self) -> "Money":
        return Money(-self.amount, self.currency)

    def __lt__(self, other: "Money") -> bool:
        self._ensure_same_currency(other)
        return self.amount < other.amount

    def __le__(self, other: "Money") -> bool:
        self._ensure_same_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other: "Money") -> bool:
        self._ensure_same_currency(other)
        return self.amount > other.amount

    def __ge__(self, other: "Money") -> bool:
        self._ensure_same_currency(other)
        return self.amount >= other.amount


    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"
