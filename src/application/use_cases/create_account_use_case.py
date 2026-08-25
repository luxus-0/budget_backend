from application.ports.account_repository import AccountRepository
from domain.entities.account import Account


class CreateAccountUseCase:
    def __init__(self, account_repository: AccountRepository) -> None:
        self._account_repository = account_repository

    def execute(self) -> Account:
        pass
