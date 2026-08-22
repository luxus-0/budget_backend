from src.domain.exceptions import InvalidCurrencyError

VALID_CURRENCIES = frozenset({
    "PLN", "USD", "EUR", "GBP", "CHF", "JPY", "CZK", "NOK", "SEK",
})


def validate_currency(currency: str) -> str:
    normalized = currency.strip().upper()
    if normalized not in VALID_CURRENCIES:
        raise InvalidCurrencyError(f"Unsupported currency: {normalized}")
    return normalized