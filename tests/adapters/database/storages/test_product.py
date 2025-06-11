from collections.abc import Callable
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsUUID

from bakery.adapters.database.storages.product import ProductStorage
from bakery.adapters.database.storages.user import UserStorage
from bakery.adapters.database.tables import ProductTable
from bakery.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from bakery.domains.entities.product import (
    CreateProduct,
    Product,
    ProductCategory,
    ProductListParams,
    UpdateProduct,
)
from tests.utils import now_utc


async def test__create(
    product_storage: ProductStorage,
) -> None:
    create_data = CreateProduct(
        name="test_name",
        description="test_description",
        category=ProductCategory.BREAD,
        weight=300,
        volume=0,
        protein=10,
        fat=10,
        carbohydrate=10,
        price=100,
    )
    user = await product_storage.create(input_dto=create_data)
    assert user == Product(
        id=IsUUID,
        name=create_data.name,
        description=create_data.description,
        category=create_data.category,
        weight=create_data.weight,
        volume=create_data.volume,
        protein=create_data.protein,
        fat=create_data.fat,
        carbohydrate=create_data.carbohydrate,
        price=create_data.price,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__create__entity_already_exists_exception(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    db_product: ProductTable = await create_product()
    create_data = CreateProduct(
        name=db_product.name,
        description="test_description",
        category=ProductCategory.BREAD,
        weight=300,
        volume=0,
        protein=10,
        fat=10,
        carbohydrate=10,
        price=100,
    )
    with pytest.raises(EntityAlreadyExistsException):
        await product_storage.create(input_dto=create_data)


async def test__get_by_id(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    db_product: ProductTable = await create_product()
    product = await product_storage.get_by_id(input_id=db_product.id)
    assert product == Product(
        id=db_product.id,
        name=db_product.name,
        description=db_product.description,
        category=db_product.category,
        weight=db_product.weight,
        volume=db_product.volume,
        protein=db_product.protein,
        fat=db_product.fat,
        carbohydrate=db_product.carbohydrate,
        price=db_product.price,
        created_at=db_product.created_at,
        updated_at=db_product.updated_at,
    )


async def test__get_by_id__none(product_storage: ProductStorage) -> None:
    assert await product_storage.get_by_id(input_id=uuid4()) is None


async def test__get_by_id__deleted(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    db_product: ProductTable = await create_product(deleted_at=now_utc())
    assert await product_storage.get_by_id(input_id=db_product.id) is None


async def test__get_list(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    db_products: list[ProductTable] = sorted(
        [await create_product() for _ in range(2)],
        key=lambda p: p.name,
    )
    products = await product_storage.get_list(
        input_dto=ProductListParams(limit=10, offset=0, category=None)
    )
    assert products == [
        Product(
            id=db_product.id,
            name=db_product.name,
            description=db_product.description,
            category=db_product.category,
            weight=db_product.weight,
            volume=db_product.volume,
            protein=db_product.protein,
            fat=db_product.fat,
            carbohydrate=db_product.carbohydrate,
            price=db_product.price,
            created_at=db_product.created_at,
            updated_at=db_product.updated_at,
        )
        for db_product in db_products
    ]


async def test__get_list__validate_filter__category(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    db_products: list[ProductTable] = sorted(
        [await create_product(category=ProductCategory.BREAD) for _ in range(2)],
        key=lambda p: p.name,
    )
    await create_product(category=ProductCategory.OIL)
    products = await product_storage.get_list(
        input_dto=ProductListParams(limit=10, offset=0, category=ProductCategory.BREAD)
    )
    assert products == [
        Product(
            id=db_product.id,
            name=db_product.name,
            description=db_product.description,
            category=db_product.category,
            weight=db_product.weight,
            volume=db_product.volume,
            protein=db_product.protein,
            fat=db_product.fat,
            carbohydrate=db_product.carbohydrate,
            price=db_product.price,
            created_at=db_product.created_at,
            updated_at=db_product.updated_at,
        )
        for db_product in db_products
    ]


async def test__get_list__validate_limit(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    db_products: list[ProductTable] = sorted(
        [await create_product() for _ in range(2)],
        key=lambda p: p.name,
    )
    products = await product_storage.get_list(
        input_dto=ProductListParams(limit=1, offset=0, category=None)
    )
    assert (
        products
        == [
            Product(
                id=db_product.id,
                name=db_product.name,
                description=db_product.description,
                category=db_product.category,
                weight=db_product.weight,
                volume=db_product.volume,
                protein=db_product.protein,
                fat=db_product.fat,
                carbohydrate=db_product.carbohydrate,
                price=db_product.price,
                created_at=db_product.created_at,
                updated_at=db_product.updated_at,
            )
            for db_product in db_products
        ][:1]
    )


async def test__get_list__validate_offset(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    db_products: list[ProductTable] = sorted(
        [await create_product() for _ in range(2)],
        key=lambda p: p.name,
    )
    products = await product_storage.get_list(
        input_dto=ProductListParams(limit=2, offset=1, category=None)
    )
    assert (
        products
        == [
            Product(
                id=db_product.id,
                name=db_product.name,
                description=db_product.description,
                category=db_product.category,
                weight=db_product.weight,
                volume=db_product.volume,
                protein=db_product.protein,
                fat=db_product.fat,
                carbohydrate=db_product.carbohydrate,
                price=db_product.price,
                created_at=db_product.created_at,
                updated_at=db_product.updated_at,
            )
            for db_product in db_products
        ][1:]
    )


async def test__get_list__empty_list(
    product_storage: ProductStorage,
) -> None:
    users = await product_storage.get_list(
        input_dto=ProductListParams(limit=10, offset=0, category=None)
    )
    assert users == []


async def test__count(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    await create_product()
    count = await product_storage.count(
        input_dto=ProductListParams(limit=10, offset=0, category=None)
    )
    assert count == 1


async def test__count__validate_filter__category(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    await create_product(category=ProductCategory.BREAD)
    db_product: ProductTable = await create_product(category=ProductCategory.OIL)
    count = await product_storage.count(
        input_dto=ProductListParams(limit=10, offset=0, category=db_product.category)
    )
    assert count == 1


async def test__count__zero(
    product_storage: ProductStorage,
) -> None:
    count = await product_storage.count(
        input_dto=ProductListParams(limit=10, offset=0, category=None)
    )
    assert count == 0


async def test__exists_by_id(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    db_product: ProductTable = await create_product()
    assert await product_storage.exists_by_id(input_id=db_product.id)


async def test__exists_by_id__false(product_storage: ProductStorage) -> None:
    assert await product_storage.exists_by_id(input_id=uuid4()) is False


async def test__exists_by_id__deleted(
    product_storage: UserStorage,
    create_product: Callable,
) -> None:
    db_product: ProductTable = await create_product(deleted_at=now_utc())
    assert await product_storage.exists_by_id(input_id=db_product.id) is False


async def test__update_by_id(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    db_product: ProductTable = await create_product()
    update_data = UpdateProduct(
        id=db_product.id,
        name="test_name",
        description="test_description",
        category=ProductCategory.BREAD,
        weight=300,
        volume=0,
        protein=10,
        fat=10,
        carbohydrate=10,
        price=100,
    )
    product = await product_storage.update_by_id(input_dto=update_data)
    assert product == Product(
        id=db_product.id,
        name=update_data.name,
        description=update_data.description,
        category=update_data.category,
        weight=update_data.weight,
        volume=update_data.volume,
        protein=update_data.protein,
        fat=update_data.fat,
        carbohydrate=update_data.carbohydrate,
        price=update_data.price,
        created_at=db_product.created_at,
        updated_at=IsDatetime,
    )


async def test__update_by_id__entity_already_exists_exception(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    db_products: list[ProductTable] = [await create_product() for _ in range(2)]
    update_data = UpdateProduct(
        id=db_products[0].id,
        name=db_products[1].name,
        description="test_description",
        category=ProductCategory.BREAD,
        weight=300,
        volume=0,
        protein=10,
        fat=10,
        carbohydrate=10,
        price=100,
    )
    with pytest.raises(EntityAlreadyExistsException):
        await product_storage.update_by_id(input_dto=update_data)


async def test__update_by_id__entity_not_found_exception(
    product_storage: ProductStorage,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await product_storage.update_by_id(
            input_dto=UpdateProduct(
                id=uuid4(),
                name="test_name",
                description="test_description",
                category=ProductCategory.BREAD,
                weight=300,
                volume=0,
                protein=10,
                fat=10,
                carbohydrate=10,
                price=100,
            )
        )


async def test__delete_by_id(
    product_storage: ProductStorage,
    create_product: Callable,
) -> None:
    db_product: ProductTable = await create_product()
    await product_storage.delete_by_id(input_id=db_product.id)
    assert db_product.deleted_at is not None


async def test__delete_by_id__none(product_storage: ProductStorage) -> None:
    assert await product_storage.delete_by_id(input_id=uuid4()) is None
