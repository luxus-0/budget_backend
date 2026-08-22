class DomainError(Exception):
    pass

class InvalidCurrencyError(DomainError):
    pass


class InvalidAmountError(DomainError):
    pass


class InvalidTransactionError(DomainError):
    pass