from uuid import UUID

from domain.entities.account import Account


class FakeAccountRepository:
    def __init__(self) -> None:
        self._accounts: dict[UUID, Account] = {}

    async def save(self, account: Account) -> None:
        self._accounts[account.id] = account

    async def get_by_id(self, account_id: UUID) -> Account | None:
        return self._accounts.get(account_id)

    async def exists_with_name(self, user_id: UUID, name: str) -> bool:
        return any(a.user_id == user_id and a.name == name for a in self._accounts.values())
