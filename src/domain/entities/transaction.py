from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from src.domain.exceptions import InvalidTransactionError
from src.domain.value_objects.money import Money


class TransactionType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Transaction:
    """
    Represents a financial transaction associated with an account.

    A transaction represents either an income or an expense.
    The transaction amount is always positive; its direction is determined
    by the transaction type.

    Transactions must be assigned to a category.
    """

    id: UUID
    account_id: UUID
    amount: Money
    kind: TransactionType
    category_id: UUID
    description: str = ""
    occurred_at: datetime = field(default_factory=_utcnow)
    created_at: datetime = field(default_factory=_utcnow)

    def __post_init__(self) -> None:
        self.description = self.description.strip()

        if self.amount.is_zero() or self.amount.is_negative():
            raise InvalidTransactionError(
                "Transaction amount must be strictly positive."
            )

    @classmethod
    def create(
        cls,
        account_id: UUID,
        amount: Money,
        kind: TransactionType,
        category_id: UUID,
        description: str = "",
    ) -> "Transaction":
        """
        Create a new financial transaction.

        Args:
            account_id: Identifier of the account associated with the transaction.
            amount: Positive transaction amount.
            kind: Type of the transaction.
            category_id: Identifier of the category assigned to the transaction.
            description: Optional description of the transaction.

        Returns:
            A new Transaction instance.
        """
        return cls(
            id=uuid4(),
            account_id=account_id,
            amount=amount,
            kind=kind,
            category_id=category_id,
            description=description,
        )

    def signed_amount(self) -> Money:
        """
        Return the transaction amount with its financial direction.

        Income returns a positive amount.
        Expense returns a negative amount.

        Returns:
            Positive amount for income or negative amount for expense.
        """
        if self.kind is TransactionType.INCOME:
            return self.amount

        return -self.amount