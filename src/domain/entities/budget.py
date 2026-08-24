"""Domain module containing the Budget entity and related value objects.

This module is responsible for managing spending limits per category
within a specific monthly period.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4

from domain.value_objects.budget_period import BudgetPeriod
from domain.value_objects.money import Money


@dataclass
class Budget:
    budget_id: UUID
    user_id: UUID
    category_id: UUID
    period: BudgetPeriod
    limit_amount: Money
    spent_amount: Money = field(
        default_factory=lambda: Money(Decimal("0.00"))
    )

    @classmethod
    def create(
        cls,
        user_id: UUID,
        category_id: UUID,
        month: int,
        year: int,
        limit: Money,
    ) -> "Budget":
        """Factory method to create a new budget with initial zero spent amount."""
        return cls(
            budget_id=uuid4(),
            user_id=user_id,
            category_id=category_id,
            period=BudgetPeriod(month=month, year=year),
            limit_amount=limit,
            spent_amount=Money(Decimal("0.00"), currency=limit.currency),
        )

    def add_expense(self, amount: Money) -> None:
        """Adds an expense to the budget, ensuring currency consistency."""
        if amount.currency != self.limit_amount.currency:
            raise ValueError("Currency mismatch between transaction and budget.")

        new_spent = self.spent_amount.amount + amount.amount
        self.spent_amount = Money(new_spent, currency=self.limit_amount.currency)

    @property
    def is_exceeded(self) -> bool:
        """Checks whether the budget limit has been exceeded."""
        return self.spent_amount.amount > self.limit_amount.amount