"""Budget entity.

Represents a spending limit for a specific category within a specific
month/year period. Budget owns the invariant that its limit is always
positive and that spent_amount's currency always matches limit_amount's
currency - both checked at construction time, not just in create().
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4

from src.domain.exceptions import InvalidBudgetError
from src.domain.value_objects.budget_period import BudgetPeriod
from src.domain.value_objects.money import Money


@dataclass
class Budget:
    id: UUID
    user_id: UUID
    category_id: UUID
    period: BudgetPeriod
    limit_amount: Money
    spent_amount: Money = field(default_factory=lambda: Money(Decimal("0")))

    def __post_init__(self) -> None:
        if self.limit_amount.is_zero() or self.limit_amount.is_negative():
            raise InvalidBudgetError("Budget limit must be strictly positive")

        if self.spent_amount.currency != self.limit_amount.currency:
            raise InvalidBudgetError(
                "spent_amount currency must match limit_amount currency"
            )

    @classmethod
    def create(
            cls,
            user_id: UUID,
            category_id: UUID,
            period: BudgetPeriod,
            limit: Money,
    ) -> "Budget":
        return cls(
            id=uuid4(),
            user_id=user_id,
            category_id=category_id,
            period=period,
            limit_amount=limit,
            spent_amount=Money(Decimal("0"), currency=limit.currency),
        )

    def add_expense(self, amount: Money) -> None:
        """Adds an expense to the budget. Does not raise when the limit
        is exceeded by design - callers check `is_exceeded` to decide
        what to do (e.g. warn the user), the budget itself only tracks."""
        if amount.currency != self.limit_amount.currency:
            raise InvalidBudgetError(
                f"Currency mismatch: expense is {amount.currency}, "
                f"budget is {self.limit_amount.currency}"
            )
        if amount.is_zero() or amount.is_negative():
            raise InvalidBudgetError("Expense amount must be strictly positive")

        self.spent_amount = self.spent_amount + amount

    @property
    def is_exceeded(self) -> bool:
        return self.spent_amount > self.limit_amount

    @property
    def remaining(self) -> Money:
        return self.limit_amount - self.spent_amount
