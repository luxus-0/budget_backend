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