from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest

from domain.entities.transaction import Transaction, TransactionType
from domain.exceptions import InvalidTransactionError
from domain.value_objects.money import Money


def test_transaction_create_creates_transaction() -> None:
    account_id = uuid4()
    category_id = uuid4()
    amount = Money(Decimal("100.00"), "PLN")

    transaction = Transaction.create(
        account_id=account_id,
        amount=amount,
        kind=TransactionType.INCOME,
        category_id=category_id,
        description="Salary",
    )

    assert transaction.account_id == account_id
    assert transaction.amount == amount
    assert transaction.kind is TransactionType.INCOME
    assert transaction.category_id == category_id
    assert transaction.description == "Salary"


def test_transaction_create_generates_id() -> None:
    transaction = Transaction.create(
        account_id=uuid4(),
        amount=Money(Decimal("100.00"), "PLN"),
        kind=TransactionType.INCOME,
        category_id=uuid4(),
    )

    assert transaction.id is not None


def test_transaction_create_sets_created_at_in_utc() -> None:
    transaction = Transaction.create(
        account_id=uuid4(),
        amount=Money(Decimal("100.00"), "PLN"),
        kind=TransactionType.INCOME,
        category_id=uuid4(),
    )

    assert transaction.created_at.tzinfo == timezone.utc


def test_transaction_create_sets_occurred_at_in_utc() -> None:
    transaction = Transaction.create(
        account_id=uuid4(),
        amount=Money(Decimal("100.00"), "PLN"),
        kind=TransactionType.INCOME,
        category_id=uuid4(),
    )

    assert transaction.occurred_at.tzinfo == timezone.utc


def test_transaction_strips_description() -> None:
    transaction = Transaction.create(
        account_id=uuid4(),
        amount=Money(Decimal("100.00"), "PLN"),
        kind=TransactionType.INCOME,
        category_id=uuid4(),
        description="  Salary  ",
    )

    assert transaction.description == "Salary"


def test_transaction_uses_empty_description_by_default() -> None:
    transaction = Transaction.create(
        account_id=uuid4(),
        amount=Money(Decimal("100.00"), "PLN"),
        kind=TransactionType.INCOME,
        category_id=uuid4(),
    )

    assert transaction.description == ""


@pytest.mark.parametrize(
    "amount",
    [
        Money(Decimal("0.00"), "PLN"),
        Money(Decimal("-1.00"), "PLN"),
    ],
)
def test_transaction_rejects_non_positive_amount(
        amount: Money,
) -> None:
    with pytest.raises(
            InvalidTransactionError,
            match="Transaction amount must be strictly positive.",
    ):
        Transaction.create(
            account_id=uuid4(),
            amount=amount,
            kind=TransactionType.INCOME,
            category_id=uuid4(),
        )


def test_income_signed_amount_is_positive() -> None:
    transaction = Transaction.create(
        account_id=uuid4(),
        amount=Money(Decimal("100.00"), "PLN"),
        kind=TransactionType.INCOME,
        category_id=uuid4(),
    )

    assert transaction.signed_amount() == Money(
        Decimal("100.00"),
        "PLN",
    )


def test_expense_signed_amount_is_negative() -> None:
    transaction = Transaction.create(
        account_id=uuid4(),
        amount=Money(Decimal("100.00"), "PLN"),
        kind=TransactionType.EXPENSE,
        category_id=uuid4(),
    )

    assert transaction.signed_amount() == Money(
        Decimal("-100.00"),
        "PLN",
    )


@pytest.mark.parametrize(
    ("kind", "expected_amount"),
    [
        (TransactionType.INCOME, Decimal("100.00")),
        (TransactionType.EXPENSE, Decimal("-100.00")),
    ],
)
def test_signed_amount_reflects_transaction_type(
        kind: TransactionType,
        expected_amount: Decimal,
) -> None:
    transaction = Transaction.create(
        account_id=uuid4(),
        amount=Money(Decimal("100.00"), "PLN"),
        kind=kind,
        category_id=uuid4(),
    )

    assert transaction.signed_amount() == Money(
        expected_amount,
        "PLN",
    )


def test_transaction_preserves_occurred_at() -> None:
    occurred_at = datetime.now(timezone.utc)

    transaction = Transaction(
        id=uuid4(),
        account_id=uuid4(),
        amount=Money(Decimal("100.00"), "PLN"),
        kind=TransactionType.EXPENSE,
        category_id=uuid4(),
        user_id=uuid4(),
        occurred_at=occurred_at,
    )

    assert transaction.occurred_at == occurred_at


def test_transaction_preserves_created_at() -> None:
    created_at = datetime.now(timezone.utc)

    transaction = Transaction(
        id=uuid4(),
        account_id=uuid4(),
        amount=Money(Decimal("100.00"), "PLN"),
        kind=TransactionType.EXPENSE,
        category_id=uuid4(),
        user_id=uuid4(),
        created_at=created_at,
    )

    assert transaction.created_at == created_at
