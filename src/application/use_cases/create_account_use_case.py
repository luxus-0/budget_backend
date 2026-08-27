from application.commands.create_account_command import CreateAccountCommand
from application.ports.account_repository import AccountRepository
from domain.entities.account import Account
from domain.exceptions import AccountAlreadyExistsError


class CreateAccountUseCase:
    def __init__(self, account_repository: AccountRepository) -> None:
        self._account_repository = account_repository

    async def execute(self, command: CreateAccountCommand) -> Account:
        if await self._account_repository.exists_with_name(command.user_id, command.name):
            raise AccountAlreadyExistsError(command.name)

        account = Account.create(
            user_id=command.user_id,
            name=command.name,
            currency=command.currency,
            kind=command.kind,
        )
        await self._account_repository.save(account)
        return account
