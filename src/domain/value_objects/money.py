from dataclasses import dataclass
from decimal import Decimal
from functools import total_ordering
from numbers import Number

from src.domain.exceptions import InvalidAmountError, InvalidCurrencyError


@total_ordering
@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            raise InvalidAmountError(
                "Amount must be a Decimal instance"
            )

        currency = self.currency.strip().upper()

        if len(currency) != 3 or not currency.isalpha():
            raise InvalidCurrencyError(
                "Currency must be a 3-letter code"
            )

        object.__setattr__(self, "currency", currency)

    def _ensure_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise InvalidCurrencyError(
                f"Currencies must match: "
                f"{self.currency} != {other.currency}"
            )

    def __add__(self, other: object) -> "Money":
        if not isinstance(other, Money):
            return NotImplemented

        self._ensure_same_currency(other)

        return Money(
            self.amount + other.amount,
            self.currency,
        )

    def __sub__(self, other: object) -> "Money":
        if not isinstance(other, Money):
            return NotImplemented

        self._ensure_same_currency(other)

        return Money(
            self.amount - other.amount,
            self.currency,
        )

    def __mul__(self, factor: Number) -> "Money":
        return Money(
            self.amount * Decimal(str(factor)),
            self.currency,
        )

    __rmul__ = __mul__

    def __truediv__(self, divisor: Number) -> "Money":
        return Money(
            self.amount / Decimal(str(divisor)),
            self.currency,
        )

    def __neg__(self) -> "Money":
        return Money(-self.amount, self.currency)

    def __abs__(self) -> "Money":
        return Money(abs(self.amount), self.currency)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented

        self._ensure_same_currency(other)

        return self.amount < other.amount

    def is_zero(self) -> bool:
        return self.amount.is_zero()

    def is_negative(self) -> bool:
        return self.amount < 0

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"
