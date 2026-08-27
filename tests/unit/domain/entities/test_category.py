from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest

from domain.entities.category import Category, CategoryType
from domain.exceptions import InvalidCategoryError


def test_category_creates_income_category() -> None:
    category = Category.create(
        name="Salary",
        kind=CategoryType.INCOME,
    )

    assert category.name == "Salary"
    assert category.kind is CategoryType.INCOME


def test_category_creates_expense_category() -> None:
    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    assert category.name == "Food"
    assert category.kind is CategoryType.EXPENSE


def test_category_generates_uuid() -> None:
    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    assert isinstance(category.id, UUID)
    assert category.id.version == 4


def test_category_creates_system_category_without_user_id() -> None:
    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    assert category.user_id is None


def test_category_creates_user_category() -> None:
    user_id = uuid4()

    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
        user_id=user_id,
    )

    assert category.user_id == user_id


def test_category_creates_category_without_parent() -> None:
    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    assert category.parent_id is None


def test_category_creates_child_category() -> None:
    parent_id = uuid4()

    category = Category.create(
        name="Restaurants",
        kind=CategoryType.EXPENSE,
        parent_id=parent_id,
    )

    assert category.parent_id == parent_id


def test_category_strips_leading_and_trailing_whitespace() -> None:
    category = Category.create(
        name="  Food  ",
        kind=CategoryType.EXPENSE,
    )

    assert category.name == "Food"


def test_category_accepts_name_with_internal_whitespace() -> None:
    category = Category.create(
        name="Food and Restaurants",
        kind=CategoryType.EXPENSE,
    )

    assert category.name == "Food and Restaurants"


def test_category_accepts_name_with_exactly_70_characters() -> None:
    name = "A" * 70

    category = Category.create(
        name=name,
        kind=CategoryType.EXPENSE,
    )

    assert category.name == name
    assert len(category.name) == 70


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
def test_category_rejects_empty_name(name: str) -> None:
    with pytest.raises(
            InvalidCategoryError,
            match="Category name cannot be empty.",
    ):
        Category.create(
            name=name,
            kind=CategoryType.EXPENSE,
        )


def test_category_rejects_name_longer_than_70_characters() -> None:
    name = "A" * 71

    with pytest.raises(
            InvalidCategoryError,
            match="Category name cannot exceed 70 characters.",
    ):
        Category.create(
            name=name,
            kind=CategoryType.EXPENSE,
        )


def test_category_rejects_name_that_exceeds_70_characters_after_stripping() -> None:
    name = f"  {'A' * 71}  "

    with pytest.raises(
            InvalidCategoryError,
            match="Category name cannot exceed 70 characters.",
    ):
        Category.create(
            name=name,
            kind=CategoryType.EXPENSE,
        )


def test_category_is_immutable() -> None:
    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    with pytest.raises(AttributeError):
        setattr(category, "name", "Travel")


def test_category_created_at_is_set_automatically() -> None:
    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    assert category.created_at.tzinfo == timezone.utc


def test_category_preserves_created_at() -> None:
    created_at = datetime.now(timezone.utc)

    category = Category(
        id=uuid4(),
        name="Food",
        kind=CategoryType.EXPENSE,
        created_at=created_at,
    )

    assert category.created_at == created_at


def test_category_create_generates_different_ids() -> None:
    first = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    second = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    assert first.id != second.id


def test_category_rename_creates_new_category() -> None:
    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    renamed = category.rename("Restaurants")

    assert renamed.name == "Restaurants"
    assert renamed is not category


def test_category_rename_preserves_id() -> None:
    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    renamed = category.rename("Restaurants")

    assert renamed.id == category.id


def test_category_rename_preserves_kind() -> None:
    category = Category.create(
        name="Salary",
        kind=CategoryType.INCOME,
    )

    renamed = category.rename("Employment")

    assert renamed.kind is CategoryType.INCOME


def test_category_rename_preserves_user_id() -> None:
    user_id = uuid4()

    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
        user_id=user_id,
    )

    renamed = category.rename("Restaurants")

    assert renamed.user_id == user_id


def test_category_rename_preserves_parent_id() -> None:
    parent_id = uuid4()

    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
        parent_id=parent_id,
    )

    renamed = category.rename("Restaurants")

    assert renamed.parent_id == parent_id


def test_category_rename_preserves_created_at() -> None:
    created_at = datetime.now(timezone.utc)

    category = Category(
        id=uuid4(),
        name="Food",
        kind=CategoryType.EXPENSE,
        created_at=created_at,
    )

    renamed = category.rename("Restaurants")

    assert renamed.created_at == created_at


def test_category_rename_strips_new_name() -> None:
    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    renamed = category.rename("  Restaurants  ")

    assert renamed.name == "Restaurants"


@pytest.mark.parametrize(
    "name",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_category_rename_rejects_empty_name(name: str) -> None:
    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    with pytest.raises(
            InvalidCategoryError,
            match="Category name cannot be empty.",
    ):
        category.rename(name)


def test_category_rename_rejects_name_longer_than_70_characters() -> None:
    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    with pytest.raises(
            InvalidCategoryError,
            match="Category name cannot exceed 70 characters.",
    ):
        category.rename("A" * 71)


def test_category_rename_does_not_modify_original_category() -> None:
    category = Category.create(
        name="Food",
        kind=CategoryType.EXPENSE,
    )

    renamed = category.rename("Restaurants")

    assert category.name == "Food"
    assert renamed.name == "Restaurants"
