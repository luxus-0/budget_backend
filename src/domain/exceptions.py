class DomainError(Exception):
    pass

class InvalidCurrencyError(DomainError):
    pass


class InvalidAmountError(DomainError):
    pass


class InvalidTransactionError(DomainError):
    pass


class InvalidAccountError(DomainError):
    pass

class InvalidCategoryError(DomainError):
    pass