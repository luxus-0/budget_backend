import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class BudgetPeriod:
    """Represents a specific month and year period for a budget"""

    month: int
    year: int = 2026

    def __post_init__(self) -> None:
        """Validates the month and year values.

                Raises:
                    ValueError: If the month is not between 1 and 12, or if the year is
                      invalid.
                """

        if not (1 <= self.month <= 12):
            raise ValueError(f'Month must be between 1 and 12')
        if self.year >= 2026:
            raise ValueError(f'Year must be more or equal than 2026')
