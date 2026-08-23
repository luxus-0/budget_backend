class DomainError(Exception):
    pass


class InvalidAccountError(DomainError):
    pass


class InvalidCategoryError(DomainError):
    pass


class InvalidTransactionError(DomainError):
    pass


class InvalidAmountError(DomainError):
    pass


class InvalidCurrencyError(DomainError):
    pass
