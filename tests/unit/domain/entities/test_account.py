from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest

from domain.entities.account import Account, AccountType
from domain.exceptions import InvalidAccountError, InvalidCurrencyError


def test_account_creates_with_valid_data() -> None:
    user_id = uuid4()

    account = Account.create(
        user_id=user_id,
        name="Main Account",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    assert isinstance(account.id, UUID)
    assert account.user_id == user_id
    assert account.name == "Main Account"
    assert account.currency == "PLN"
    assert account.kind is AccountType.CHECKING


@pytest.mark.parametrize(
    "kind",
    [
        AccountType.CHECKING,
        AccountType.SAVINGS,
        AccountType.CASH,
    ],
)
def test_account_supports_all_account_types(
        kind: AccountType,
) -> None:
    account = Account.create(
        user_id=uuid4(),
        name="Account",
        currency="PLN",
        kind=kind,
    )

    assert account.kind is kind


def test_account_generates_uuid() -> None:
    account = Account.create(
        user_id=uuid4(),
        name="Main Account",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    assert isinstance(account.id, UUID)


def test_account_generates_unique_ids() -> None:
    first = Account.create(
        user_id=uuid4(),
        name="Account",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    second = Account.create(
        user_id=uuid4(),
        name="Account",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    assert first.id != second.id


def test_account_preserves_user_id() -> None:
    user_id = uuid4()

    account = Account.create(
        user_id=user_id,
        name="Main Account",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    assert account.user_id == user_id


def test_account_strips_leading_and_trailing_whitespace_from_name() -> None:
    account = Account.create(
        user_id=uuid4(),
        name="  Main Account  ",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    assert account.name == "Main Account"


def test_account_accepts_internal_whitespace_in_name() -> None:
    account = Account.create(
        user_id=uuid4(),
        name="Main   Account",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    assert account.name == "Main   Account"


@pytest.mark.parametrize(
    "name",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
        " \t\n ",
    ],
)
def test_account_rejects_empty_name(name: str) -> None:
    with pytest.raises(
            InvalidAccountError,
            match="Account name cannot be empty.",
    ):
        Account.create(
            user_id=uuid4(),
            name=name,
            currency="PLN",
            kind=AccountType.CHECKING,
        )


@pytest.mark.parametrize(
    "currency",
    [
        "pln",
        "PLN",
        " Pln ",
        " eur ",
        "USD",
    ],
)
def test_account_normalizes_currency(currency: str) -> None:
    account = Account.create(
        user_id=uuid4(),
        name="Account",
        currency=currency,
        kind=AccountType.CHECKING,
    )

    assert account.currency == currency.strip().upper()


def test_account_rejects_invalid_currency() -> None:
    with pytest.raises(
            InvalidCurrencyError,
            match="Unsupported currency: ABC",
    ):
        Account.create(
            user_id=uuid4(),
            name="Account",
            currency="ABC",
            kind=AccountType.CHECKING,
        )


def test_account_created_at_is_set_automatically() -> None:
    account = Account.create(
        user_id=uuid4(),
        name="Account",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    assert isinstance(account.created_at, datetime)
    assert account.created_at.tzinfo == timezone.utc


def test_account_created_at_is_close_to_current_time() -> None:
    before = datetime.now(timezone.utc)

    account = Account.create(
        user_id=uuid4(),
        name="Account",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    after = datetime.now(timezone.utc)

    assert before <= account.created_at <= after


def test_account_rename_changes_name() -> None:
    account = Account.create(
        user_id=uuid4(),
        name="Main Account",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    account.rename("Savings Account")

    assert account.name == "Savings Account"


def test_account_rename_strips_leading_and_trailing_whitespace() -> None:
    account = Account.create(
        user_id=uuid4(),
        name="Main Account",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    account.rename("  Savings Account  ")

    assert account.name == "Savings Account"


@pytest.mark.parametrize(
    "name",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
        " \t\n ",
    ],
)
def test_account_rename_rejects_empty_name(name: str) -> None:
    account = Account.create(
        user_id=uuid4(),
        name="Main Account",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    with pytest.raises(
            InvalidAccountError,
            match="Account name cannot be empty.",
    ):
        account.rename(name)


def test_account_rename_preserves_other_properties() -> None:
    user_id = uuid4()

    account = Account.create(
        user_id=user_id,
        name="Main Account",
        currency="PLN",
        kind=AccountType.CHECKING,
    )

    account_id = account.id
    created_at = account.created_at

    account.rename("Savings Account")

    assert account.id == account_id
    assert account.user_id == user_id
    assert account.currency == "PLN"
    assert account.kind is AccountType.CHECKING
    assert account.created_at == created_at


def test_account_rename_does_not_change_currency() -> None:
    account = Account.create(
        user_id=uuid4(),
        name="Main Account",
        currency="EUR",
        kind=AccountType.CHECKING,
    )

    account.rename("Travel Account")

    assert account.currency == "EUR"


def test_account_rename_does_not_change_account_type() -> None:
    account = Account.create(
        user_id=uuid4(),
        name="Main Account",
        currency="PLN",
        kind=AccountType.SAVINGS,
    )

    account.rename("Emergency Fund")

    assert account.kind is AccountType.SAVINGS
