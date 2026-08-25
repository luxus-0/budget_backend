from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from src.domain.exceptions import InvalidCategoryError


class CategoryType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class Category:
    """
    Represents a financial category used to classify transactions.

    A category can be an income or expense category and may optionally
    belong to a parent category.

    A category without a user_id represents a system category that can
    be shared between users.
    """

    id: UUID
    name: str
    kind: CategoryType
    parent_id: UUID | None = None
    user_id: UUID | None = None
    created_at: datetime = field(default_factory=_utcnow)

    def __post_init__(self) -> None:
        name = self.name.strip()

        if not name:
            raise InvalidCategoryError("Category name cannot be empty.")

        if len(name) > 70:
            raise InvalidCategoryError("Category name cannot exceed 70 characters.")

        object.__setattr__(self, "name", name)

    @classmethod
    def create(
            cls,
            name: str,
            kind: CategoryType,
            user_id: UUID | None = None,
            parent_id: UUID | None = None,
    ) -> "Category":
        """
        Create a new category.

        Args:
            name: Name of the category.
            kind: Type of the category.
            user_id: Owner of the category. None represents a system category.
            parent_id: Identifier of the parent category.

        Returns:
            A new Category instance.
        """
        return cls(
            id=uuid4(),
            name=name,
            kind=kind,
            user_id=user_id,
            parent_id=parent_id,
        )

    def rename(self, name: str) -> "Category":
        """
        Create a new category with the specified name.
        The current category remains unchanged.

        Args:
            name: New name of the category.

        Returns:
            A new Category instance with the updated name.
        """
        return Category(
            id=self.id,
            name=name,
            kind=self.kind,
            parent_id=self.parent_id,
            user_id=self.user_id,
            created_at=self.created_at,
        )
