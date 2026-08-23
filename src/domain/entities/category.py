from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from domain.exceptions import InvalidCategoryError


class CategoryType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Category:
    id: UUID
    name: str
    kind: CategoryType
    parent_id: Optional[UUID] = None
    created_at: datetime = field(default_factory=_utcnow)

    def __post_init__(self):
        self.name = self.name.strip()
        if not self.name:
            raise InvalidCategoryError('Invalid category name cannot be empty')

        if len(self.name) > 70:
            raise InvalidCategoryError('Category name is too long(max 70 characters)')

    @classmethod
    def create(
            cls,
            name: str,
            kind: CategoryType,
            parent_id: Optional[UUID] = None,
    ) -> "Category":
        return cls(id=uuid4(), name=name, kind=kind, parent_id=parent_id)

