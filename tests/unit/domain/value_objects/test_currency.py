import pytest
from _pytest.raises import raises

from domain.value_objects.currency import validate_currency
from src.domain.exceptions import InvalidCurrencyError


@pytest.mark.parametrize(
    "currency",
    [
        "PLN",
        "USD",
        "EUR",
        "GBP",
        "CHF",
        "JPY",
        "CZK",
        "NOK",
        "SEK",
    ],
)
def test_validate_currency_accepts_supported_currency(currency: str) -> None:
    assert validate_currency(currency) == currency


@pytest.mark.parametrize(
    ("currency", "expected"),
    [
        ("pln", "PLN"),
        ("usd", "USD"),
        ("eur", "EUR"),
        ("gbp", "GBP"),
        ("chf", "CHF"),
        ("jpy", "JPY"),
        ("czk", "CZK"),
        ("nok", "NOK"),
        ("sek", "SEK"),
    ],
)
def test_validate_currency_normalizes_to_uppercase(
    currency: str,
    expected: str,
) -> None:
    assert validate_currency(currency) == expected


@pytest.mark.parametrize(
    "currency",
    [
        " PLN",
        "PLN ",
        " PLN ",
        "\tUSD\t",
        "\nEUR\n",
    ],
)
def test_validate_currency_strips_whitespace(currency: str) -> None:
    assert validate_currency(currency) in {"PLN", "USD", "EUR"}


@pytest.mark.parametrize(
    "currency",
    [
        "",
        "ABC",
        "PL",
        "PLNX",
        "US",
        "USDT",
        "RUB",
        "CAD",
        "AUD",
    ],
)
def test_validate_currency_rejects_unsupported_currency(
    currency: str,
) -> None:
    with raises(InvalidCurrencyError):
        validate_currency(currency)


def test_validate_currency_error_contains_normalized_currency() -> None:
    with raises(InvalidCurrencyError, match="Unsupported currency: ABC"):
        validate_currency("abc")


def test_validate_currency_does_not_modify_original_string() -> None:
    currency = " usd "

    result = validate_currency(currency)

    assert currency == " usd "
    assert result == "USD"