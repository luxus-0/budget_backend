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
    """
    Represents a financial account owned by a user.

    An account represents a source or place where money is held,
    such as a checking account, savings account, or cash.
    """

    id: UUID
    user_id: UUID
    name: str
    currency: str
    kind: AccountType
    created_at: datetime = field(default_factory=_utcnow)

    def __post_init__(self) -> None:
        self.name = self.name.strip()

        if not self.name:
            raise InvalidAccountError("Account name cannot be empty.")

        self.currency = validate_currency(self.currency)

    @classmethod
    def create(
            cls,
            user_id: UUID,
            name: str,
            currency: str,
            kind: AccountType,
    ) -> "Account":
        """
        Create a new financial account.

        Args:
            user_id: Identifier of the account owner.
            name: Name of the account.
            currency: ISO currency code used by the account.
            kind: Type of the account.

        Returns:
            A new Account instance.
        """
        return cls(
            id=uuid4(),
            user_id=user_id,
            name=name,
            currency=currency,
            kind=kind,
        )

    def rename(self, name: str) -> None:
        """
        Change the name of the account.

        Args:
            name: New name of the account.

        Raises:
            InvalidAccountError: If the name is empty.
        """
        name = name.strip()

        if not name:
            raise InvalidAccountError("Account name cannot be empty.")

        self.name = name
