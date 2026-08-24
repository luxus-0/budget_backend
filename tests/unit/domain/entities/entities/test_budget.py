from decimal import Decimal
from uuid import uuid4
import pytest

from domain.entities.budget import Budget
from domain.value_objects.budget_period import BudgetPeriod
from domain.value_objects.money import Money


class TestBudgetPeriod:
    def test_valid_period(self):
        # Given / When
        period = BudgetPeriod(month=8, year=2026)

        # Then
        assert period.month == 8
        assert period.year == 2026

    @pytest.mark.parametrize("invalid_month", [0, 13, -1])
    def test_invalid_month_raises_error(self, invalid_month):
        with pytest.raises(ValueError, match="Month must be between 1 and 12"):
            BudgetPeriod(month=invalid_month, year=2026)

    @pytest.mark.parametrize("invalid_year", [0, -2026])
    def test_invalid_year_raises_error(self, invalid_year):
        with pytest.raises(ValueError):
            BudgetPeriod(month=5, year=invalid_year)


class TestBudget:
    def test_create_budget_successfully(self):
        # Given
        user_id = uuid4()
        category_id = uuid4()
        limit = Money(Decimal("500.00"), "PLN")

        # When
        budget = Budget.create(
            user_id=user_id,
            category_id=category_id,
            month=8,
            year=2026,
            limit=limit,
        )

        # Then
        assert budget.budget_id is not None
        assert budget.user_id == user_id
        assert budget.category_id == category_id
        assert budget.period.month == 8
        assert budget.period.year == 2026
        assert budget.limit_amount == limit
        assert budget.spent_amount == Money(Decimal("0.00"), "PLN")
        assert not budget.is_exceeded

    def test_add_expense_updates_spent_amount(self):
        # Given
        budget = Budget.create(
            user_id=uuid4(),
            category_id=uuid4(),
            month=8,
            year=2026,
            limit=Money(Decimal("500.00"), "PLN"),
        )
        expense = Money(Decimal("150.50"), "PLN")

        # When
        budget.add_expense(expense)

        # Then
        assert budget.spent_amount == Money(Decimal("150.50"), "PLN")
        assert not budget.is_exceeded

    def test_multiple_expenses_accumulate_correctly(self):
        # Given
        budget = Budget.create(
            user_id=uuid4(),
            category_id=uuid4(),
            month=8,
            year=2026,
            limit=Money(Decimal("1000.00"), "PLN"),
        )

        # When
        budget.add_expense(Money(Decimal("200.00"), "PLN"))
        budget.add_expense(Money(Decimal("350.25"), "PLN"))

        # Then
        assert budget.spent_amount == Money(Decimal("550.25"), "PLN")
        assert not budget.is_exceeded

    def test_add_expense_currency_mismatch_raises_error(self):
        # Given
        budget = Budget.create(
            user_id=uuid4(),
            category_id=uuid4(),
            month=8,
            year=2026,
            limit=Money(Decimal("500.00"), "PLN"),
        )
        expense_in_usd = Money(Decimal("50.00"), "USD")

        # When / Then
        with pytest.raises(ValueError, match="Currency mismatch"):
            budget.add_expense(expense_in_usd)

    def test_is_exceeded_returns_false_when_limit_is_exact(self):
        # Given - wydatki równe limitowi nie oznaczają jeszcze *przekroczenia* (strict >)
        budget = Budget.create(
            user_id=uuid4(),
            category_id=uuid4(),
            month=8,
            year=2026,
            limit=Money(Decimal("100.00"), "PLN"),
        )

        # When
        budget.add_expense(Money(Decimal("100.00"), "PLN"))

        # Then
        assert budget.spent_amount == Money(Decimal("100.00"), "PLN")
        assert not budget.is_exceeded

    def test_is_exceeded_returns_true_when_limit_crossed(self):
        # Given
        budget = Budget.create(
            user_id=uuid4(),
            category_id=uuid4(),
            month=8,
            year=2026,
            limit=Money(Decimal("100.00"), "PLN"),
        )

        # When
        budget.add_expense(Money(Decimal("100.50"), "PLN"))

        # Then
        assert budget.is_exceeded