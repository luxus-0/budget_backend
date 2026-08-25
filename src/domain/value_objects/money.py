from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from functools import total_ordering
from numbers import Number

from src.domain.exceptions import InvalidAmountError, InvalidCurrencyError
from src.domain.value_objects.currency import validate_currency


@total_ordering
@dataclass(frozen=True, slots=True)
class Money:
    """
    Represents a monetary amount with a specific currency.

    Money instances support arithmetic and comparison operations only
    when both values use the same currency.
    """

    amount: Decimal
    currency: str = "PLN"

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            raise InvalidAmountError(
                "Amount must be a Decimal instance."
            )

        object.__setattr__(
            self,
            "currency",
            validate_currency(self.currency),
        )

    def _ensure_same_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise InvalidCurrencyError(
                f"Currencies must match: "
                f"{self.currency} != {other.currency}"
            )

    def __add__(self, other: Money) -> Money:
        self._ensure_same_currency(other)

        return Money(
            self.amount + other.amount,
            self.currency,
        )

    def __sub__(self, other: Money) -> Money:
        self._ensure_same_currency(other)

        return Money(
            self.amount - other.amount,
            self.currency,
        )

    def __mul__(self, factor: Number) -> Money:
        return Money(
            self.amount * Decimal(str(factor)),
            self.currency,
        )

    def __rmul__(self, factor: Number) -> Money:
        return self.__mul__(factor)

    def __truediv__(self, divisor: Number) -> Money:
        return Money(
            self.amount / Decimal(str(divisor)),
            self.currency,
        )

    def __neg__(self) -> Money:
        return Money(
            -self.amount,
            self.currency,
        )

    def __abs__(self) -> Money:
        return Money(
            abs(self.amount),
            self.currency,
        )

    def __lt__(self, other: Money) -> bool:
        self._ensure_same_currency(other)

        return self.amount < other.amount

    def is_zero(self) -> bool:
        """Return True if the monetary amount is zero."""
        return self.amount.is_zero()

    def is_negative(self) -> bool:
        """Return True if the monetary amount is negative."""
        return self.amount < 0

    def is_positive(self) -> bool:
        """Return True if the monetary amount is greater than zero."""
        return self.amount > 0

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"
