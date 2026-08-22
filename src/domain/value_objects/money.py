from dataclasses import dataclass
from decimal import Decimal

from domain.exceptions import InvalidCurrencyError, InvalidAmountError


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = 'USD'

    def __post_init__(self):
        currency = self.currency.strip().upper()

        if len(currency) != 3 or not currency.isalpha():
            raise InvalidCurrencyError(f'Currency must be 3 big letter!!')

        if self.amount < 0 or self.amount.is_zero():
            raise InvalidAmountError('Amount cannot be zero or negative!')
        
