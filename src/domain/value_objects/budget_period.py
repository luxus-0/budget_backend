from dataclasses import dataclass

from domain.exceptions import InvalidBudgetPeriodError

MIN_YEAR = 2020


@dataclass(frozen=True, slots=True)
class BudgetPeriod:
    """Represents a specific month and year period for a budget."""

    month: int
    year: int

    def __post_init__(self) -> None:
        if not (1 <= self.month <= 12):
            raise InvalidBudgetPeriodError("Month must be between 1 and 12")
        if self.year < MIN_YEAR:
            raise InvalidBudgetPeriodError(f"Year must be {MIN_YEAR} or later")

    def __str__(self) -> str:
        return f"{self.year}-{self.month:02d}"
