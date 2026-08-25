from decimal import Decimal
from typing import Any

import pytest

from src.domain.exceptions import InvalidAmountError, InvalidCurrencyError
from src.domain.value_objects.money import Money


def test_money_creates_with_decimal_amount() -> None:
    money = Money(Decimal("100.50"), "PLN")

    assert money.amount == Decimal("100.50")
    assert money.currency == "PLN"


def test_money_uses_pln_as_default_currency() -> None:
    money = Money(Decimal("100.00"))

    assert money.currency == "PLN"


def test_money_normalizes_currency_to_uppercase() -> None:
    money = Money(Decimal("100.00"), "pln")

    assert money.currency == "PLN"


def test_money_strips_currency_whitespace() -> None:
    money = Money(Decimal("100.00"), " PLN ")

    assert money.currency == "PLN"


@pytest.mark.parametrize(
    "amount",
    [
        100,
        100.0,
        "100.00",
        "100",
    ],
)
def test_money_rejects_non_decimal_amount(amount: Any) -> None:
    with pytest.raises(
            InvalidAmountError,
            match="Amount must be a Decimal instance.",
    ):
        Money(amount)


def test_money_rejects_invalid_currency() -> None:
    with pytest.raises(
            InvalidCurrencyError,
            match="Unsupported currency: ABC",
    ):
        Money(Decimal("100.00"), "abc")


def test_money_is_immutable() -> None:
    money = Money(Decimal("100.00"), "PLN")

    with pytest.raises(AttributeError):
        setattr(money, "amount", Decimal("200.00"))


def test_money_adds_same_currency() -> None:
    first = Money(Decimal("100.50"), "PLN")
    second = Money(Decimal("50.25"), "PLN")

    result = first + second

    assert result == Money(Decimal("150.75"), "PLN")


def test_money_rejects_addition_of_different_currencies() -> None:
    first = Money(Decimal("100.00"), "PLN")
    second = Money(Decimal("50.00"), "EUR")

    with pytest.raises(
            InvalidCurrencyError,
            match="Currencies must match: PLN != EUR",
    ):
        first + second


def test_money_subtracts_same_currency() -> None:
    first = Money(Decimal("100.50"), "PLN")
    second = Money(Decimal("30.25"), "PLN")

    result = first - second

    assert result == Money(Decimal("70.25"), "PLN")


def test_money_rejects_subtraction_of_different_currencies() -> None:
    first = Money(Decimal("100.00"), "PLN")
    second = Money(Decimal("50.00"), "EUR")

    with pytest.raises(
            InvalidCurrencyError,
            match="Currencies must match: PLN != EUR",
    ):
        first - second


@pytest.mark.parametrize(
    ("amount", "factor", "expected"),
    [
        ("100.00", 2, "200.00"),
        ("100.00", 2.5, "250.00"),
        ("100.00", Decimal("1.5"), "150.00"),
        ("100.00", 0, "0.00"),
        ("100.00", -2, "-200.00"),
    ],
)
def test_money_multiplies_by_factor(
        amount: str,
        factor: Any,
        expected: str,
) -> None:
    money = Money(Decimal(amount), "PLN")

    result = money.__mul__(factor)

    assert result == Money(Decimal(expected), "PLN")


def test_money_supports_right_hand_multiplication() -> None:
    money = Money(Decimal("100.00"), "PLN")

    result = money.__rmul__(2)

    assert result == Money(Decimal("200.00"), "PLN")


def test_money_divides_by_integer_divisor() -> None:
    money = Money(Decimal("100.00"), "PLN")

    result = money.__truediv__(Decimal("4"))

    assert result == Money(Decimal("25.00"), "PLN")


def test_money_divides_by_decimal_divisor() -> None:
    money = Money(Decimal("100.00"), "PLN")

    result = money.__truediv__(Decimal("2.5"))

    assert result == Money(Decimal("40.00"), "PLN")


def test_money_negates_amount() -> None:
    money = Money(Decimal("100.00"), "PLN")

    result = -money

    assert result == Money(Decimal("-100.00"), "PLN")


def test_money_returns_absolute_value() -> None:
    money = Money(Decimal("-100.00"), "PLN")

    result = abs(money)

    assert result == Money(Decimal("100.00"), "PLN")


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("100.00", "100.00", False),
        ("100.00", "200.00", True),
        ("200.00", "100.00", False),
    ],
)
def test_money_less_than(
        left: str,
        right: str,
        expected: bool,
) -> None:
    first = Money(Decimal(left), "PLN")
    second = Money(Decimal(right), "PLN")

    assert (first < second) is expected


def test_money_rejects_comparison_of_different_currencies() -> None:
    first = Money(Decimal("100.00"), "PLN")
    second = Money(Decimal("200.00"), "EUR")

    with pytest.raises(
            InvalidCurrencyError,
            match="Currencies must match: PLN != EUR",
    ):
        first < second


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        ("0", True),
        ("0.00", True),
        ("100.00", False),
        ("-100.00", False),
    ],
)
def test_money_is_zero(amount: str, expected: bool) -> None:
    money = Money(Decimal(amount))

    assert money.is_zero() is expected


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        ("-100.00", True),
        ("-0.01", True),
        ("0", False),
        ("100.00", False),
    ],
)
def test_money_is_negative(amount: str, expected: bool) -> None:
    money = Money(Decimal(amount))

    assert money.is_negative() is expected


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        ("100.00", True),
        ("0.01", True),
        ("0", False),
        ("-100.00", False),
    ],
)
def test_money_is_positive(amount: str, expected: bool) -> None:
    money = Money(Decimal(amount))

    assert money.is_positive() is expected


def test_money_str_formats_amount_with_two_decimal_places() -> None:
    money = Money(Decimal("100"), "PLN")

    assert str(money) == "100.00 PLN"


def test_money_str_formats_fractional_amount() -> None:
    money = Money(Decimal("100.5"), "EUR")

    assert str(money) == "100.50 EUR"
