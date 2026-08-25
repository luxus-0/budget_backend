from dataclasses import dataclass
from uuid import UUID

from domain.entities.account import AccountType


@dataclass(frozen=True)
class CreateAccountCommand:
    user_id: UUID
    name: str
    currency: str
    kind: AccountType