from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from src.domain.exceptions import InvalidAccountError
from src.domain.value_objects.currency import validate_currency


class AccountType(str, Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"
    CASH = "CASH"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Account:
    id: UUID
    name: str
    currency: str
    kind: AccountType
    created_at: datetime = field(default_factory=_utcnow)

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise InvalidAccountError("Account name cannot be empty")

        self.currency = validate_currency(self.currency)

    @classmethod
    def create(cls, name: str, currency: str, kind: AccountType) -> "Account":
        return cls(id=uuid4(), name=name, currency=currency, kind=kind)