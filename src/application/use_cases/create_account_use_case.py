from application.commands.create_account_command import CreateAccountCommand
from application.ports.account_repository import AccountRepository
from domain.entities.account import Account


class CreateAccountUseCase:
    def __init__(self, account_repository: AccountRepository) -> None:
        self._account_repository = account_repository

    async def execute(self, command: CreateAccountCommand) -> Account:
        account = Account.create(
            user_id=command.user_id,
            name=command.name,
            currency=command.currency,
            kind=command.kind
        )

        await self._account_repository.save(account)
        return account
