import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID


@dataclass
class Transaction:
    id: UUID
    amount: Decimal
    description: str
    currency: str = 'USD'
    date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(cls, amount:Decimal, description:str, currency:str) -> 'Transaction':
        if amount == Decimal("0.00") or amount == 0:
            raise ValueError("Transaction amount cannot be zero.")
        if not description.strip():
            raise ValueError("Description cannot be empty")

        return cls(id=uuid.uuid4(),
                   amount=Decimal(str(amount)),
                   description=description.strip(),
                   currency=currency.upper())