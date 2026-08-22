from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from src.domain.exceptions import InvalidTransactionError
from src.domain.value_objects.money import Money


class TransactionType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSFER = "TRANSFER"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Transaction:
    id: UUID
    account_id: UUID
    amount: Money
    type: TransactionType
    category_id: Optional[UUID] = None
    description: str = ""

    occurred_at: datetime = field(default_factory=_utcnow)
    created_at: datetime = field(default_factory=_utcnow)

    def __post_init__(self) -> None:
        self.description = self.description.strip()

        if self.amount.is_zero() or self.amount.is_negative():
            raise InvalidTransactionError(
                "Transaction amount must be strictly positive; "
                "use `kind` to express direction, not the sign of amount"
            )

        if self.type == TransactionType.TRANSFER and self.category_id is not None:
            raise InvalidTransactionError("Transfers cannot have a category")

        if self.type != TransactionType.TRANSFER and self.category_id is None:
            raise InvalidTransactionError("transactions must have a category")

    @classmethod
    def create(
        cls,
        account_id: UUID,
        amount: Money,
        type: TransactionType,
        description: str = "",
        category_id: Optional[UUID] = None,
    ) -> "Transaction":
        return cls(
            id=uuid4(),
            account_id=account_id,
            category_id=category_id,
            amount=amount,
            type=type,
            description=description,
        )

    def signed_amount(self) -> Money:
        if self.type == TransactionType.INCOME:
            return self.amount
        return -self.amount