"""Port (interface) for account persistence.

Defined in the application layer, implemented in infrastructure.
This is the Dependency Inversion Principle in practice: application
owns the contract, infrastructure depends on application - never
the other way around.

Methods are limited to what CreateAccountUseCase actually needs right
now. More methods (list_all, delete, ...) get added only when a real
use case requires them - not preemptively.
"""
from typing import Protocol
from uuid import UUID

from domain.entities.account import Account


class AccountRepository(Protocol):
    def save(self, account: Account) -> None:
        pass

    def get_by_id(self, account_id: UUID, user_id: UUID) -> Account | None:
        pass
