"""Transaction entity.

A Transaction is a single financial event on one account: an income,
an expense, or one leg of a transfer. The amount is always stored as
a strictly positive Money value - direction is expressed via `type`,
never via the sign of `amount`. This avoids a whole class of bugs where
"negative expense" and "positive income" get confused.
"""
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
        if self.type == TransactionType.TRANSFER and self.category_id is not None:
            raise InvalidTransactionError("Transfers cannot have a category")
        if self.type != TransactionType.TRANSFER and self.category_id is None:
            raise InvalidTransactionError(
                f"{self.type.value} transactions must have a category"
            )

    @classmethod
    def create(
        cls,
        account_id: UUID,
        amount: Money,
        type: TransactionType,
        description: str = "",
        category_id: Optional[UUID] = None,
    ) -> "Transaction":
        """Czytelny punkt wejścia do tworzenia transakcji. Nie duplikuje
        walidacji - cała logika i tak siedzi w __post_init__, więc
        `Transaction(...)` i `Transaction.create(...)` są równoważne
        i obie są bezpieczne. Zostawiamy `create()` na przyszłość, np.
        pod emisję zdarzenia domenowego przy tworzeniu."""
        return cls(
            account_id=account_id,
            amount=amount,
            type=type,
            description=description,
            category_id=category_id,
        )

    def signed_amount(self) -> Money:
        """Amount signed for balance calculations: positive for INCOME,
        negative for EXPENSE and outgoing TRANSFER legs."""
        if self.type == TransactionType.INCOME:
            return self.amount
        return -self.amount