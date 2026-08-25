from src.domain.exceptions import InvalidCurrencyError

VALID_CURRENCIES = frozenset({
    "PLN",
    "USD",
    "EUR",
    "GBP",
    "CHF",
    "JPY",
    "CZK",
    "NOK",
    "SEK",
})


def validate_currency(currency: str) -> str:
    """
    Validate and normalize a currency code.

    Args:
        currency: Currency code to validate.

    Returns:
        Normalized currency code in uppercase.

    Raises:
        InvalidCurrencyError: If the currency is not supported.
    """
    normalized = currency.strip().upper()

    if normalized not in VALID_CURRENCIES:
        raise InvalidCurrencyError(
            f"Unsupported currency: {normalized}"
        )

    return normalized
