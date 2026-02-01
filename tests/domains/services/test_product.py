from collections.abc import Callable
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsUUID

from bakery.adapters.database.storages.product import ProductStorage
from bakery.adapters.database.tables import ProductTable
from bakery.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from bakery.domains.entities.product import (
    CreateProduct,
    Product,
    ProductCategory,
    ProductList,
    ProductListParams,
    UpdateProduct,
)
from bakery.domains.services.product import ProductService


async def test__create(
    product_service: ProductService,
) -> None:
    create_data = CreateProduct(
        name="test_name",
        description="test_description",
        category=ProductCategory.BREAD,
        price=100,
        photo_file_id="photo_id",
    )
    user = await product_service.create(input_dto=create_data)
    assert user == Product(
        id=IsUUID,
        name=create_data.name,
        description=create_data.description,
        category=create_data.category,
        price=create_data.price,
        photo_file_id=create_data.photo_file_id,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__create__entity_already_exists_exception(
    product_service: ProductService,
    create_product: Callable,
) -> None:
    db_product: ProductTable = await create_product()
    create_data = CreateProduct(
        name=db_product.name,
        description="test_description",
        category=ProductCategory.BREAD,
        price=100,
        photo_file_id="photo_id",
    )
    with pytest.raises(EntityAlreadyExistsException):
        await product_service.create(input_dto=create_data)


async def test__get_by_id(
    product_service: ProductService,
    create_product: Callable,
) -> None:
    db_product: ProductTable = await create_product()
    product = await product_service.get_by_id(input_id=db_product.id)
    assert product == Product(
        id=db_product.id,
        name=db_product.name,
        description=db_product.description,
        category=db_product.category,
        price=db_product.price,
        photo_file_id=db_product.photo_file_id,
        created_at=db_product.created_at,
        updated_at=db_product.updated_at,
    )


async def test__get_by_id__entity_not_found_exception(
    product_service: ProductService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await product_service.get_by_id(input_id=uuid4())


async def test__get_list(
    product_service: ProductService,
    create_product: Callable,
) -> None:
    db_products: list[ProductTable] = sorted(
        [await create_product() for _ in range(2)],
        key=lambda p: p.name,
    )
    products = await product_service.get_list(
        input_dto=ProductListParams(limit=10, offset=0, category=None)
    )
    assert products == ProductList(
        total=len(db_products),
        items=[
            Product(
                id=db_product.id,
                name=db_product.name,
                description=db_product.description,
                category=db_product.category,
                price=db_product.price,
                photo_file_id=db_product.photo_file_id,
                created_at=db_product.created_at,
                updated_at=db_product.updated_at,
            )
            for db_product in db_products
        ],
    )


async def test__get_list__validate_filter__category(
    product_service: ProductStorage,
    create_product: Callable,
) -> None:
    db_products: list[ProductTable] = sorted(
        [await create_product(category=ProductCategory.BREAD) for _ in range(2)],
        key=lambda p: p.name,
    )
    await create_product(category=ProductCategory.OIL)
    products = await product_service.get_list(
        input_dto=ProductListParams(limit=10, offset=0, category=ProductCategory.BREAD)
    )
    assert products == ProductList(
        total=len(db_products),
        items=[
            Product(
                id=db_product.id,
                name=db_product.name,
                description=db_product.description,
                category=db_product.category,
                price=db_product.price,
                photo_file_id=db_product.photo_file_id,
                created_at=db_product.created_at,
                updated_at=db_product.updated_at,
            )
            for db_product in db_products
        ],
    )


async def test__get_list__validate_limit(
    product_service: ProductService,
    create_product: Callable,
) -> None:
    db_products: list[ProductTable] = sorted(
        [await create_product() for _ in range(2)],
        key=lambda p: p.name,
    )
    products = await product_service.get_list(
        input_dto=ProductListParams(limit=1, offset=0, category=None)
    )
    assert products == ProductList(
        total=len(db_products),
        items=[
            Product(
                id=db_product.id,
                name=db_product.name,
                description=db_product.description,
                category=db_product.category,
                price=db_product.price,
                photo_file_id=db_product.photo_file_id,
                created_at=db_product.created_at,
                updated_at=db_product.updated_at,
            )
            for db_product in db_products
        ][:1],
    )


async def test__get_list__validate_offset(
    product_service: ProductService,
    create_product: Callable,
) -> None:
    db_products: list[ProductTable] = sorted(
        [await create_product() for _ in range(2)],
        key=lambda p: p.name,
    )
    products = await product_service.get_list(
        input_dto=ProductListParams(limit=10, offset=1, category=None)
    )
    assert products == ProductList(
        total=len(db_products),
        items=[
            Product(
                id=db_product.id,
                name=db_product.name,
                description=db_product.description,
                category=db_product.category,
                price=db_product.price,
                photo_file_id=db_product.photo_file_id,
                created_at=db_product.created_at,
                updated_at=db_product.updated_at,
            )
            for db_product in db_products
        ][1:],
    )


async def test__get_list__empty_list(
    product_service: ProductStorage,
) -> None:
    users = await product_service.get_list(
        input_dto=ProductListParams(limit=10, offset=0, category=None)
    )
    assert users == ProductList(total=0, items=[])


async def test__update_by_id(
    product_service: ProductService,
    create_product: Callable,
) -> None:
    db_product: ProductTable = await create_product()
    update_data = UpdateProduct(
        id=db_product.id,
        name="test_name",
        description="test_description",
        category=ProductCategory.BREAD,
        price=100,
        photo_file_id="photo_id",
    )
    product = await product_service.update_by_id(input_dto=update_data)
    assert product == Product(
        id=db_product.id,
        name=update_data.name,
        description=update_data.description,
        category=update_data.category,
        price=update_data.price,
        photo_file_id=update_data.photo_file_id,
        created_at=db_product.created_at,
        updated_at=IsDatetime,
    )


async def test__update_by_id__entity_already_exists_exception(
    product_service: ProductService,
    create_product: Callable,
) -> None:
    db_products: list[ProductTable] = [await create_product() for _ in range(2)]
    update_data = UpdateProduct(
        id=db_products[0].id,
        name=db_products[1].name,
        description="test_description",
        category=ProductCategory.BREAD,
        price=100,
        photo_file_id="photo_id",
    )
    with pytest.raises(EntityAlreadyExistsException):
        await product_service.update_by_id(input_dto=update_data)


async def test__update_by_id__entity_not_found_exception(
    product_service: ProductService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await product_service.update_by_id(
            input_dto=UpdateProduct(
                id=uuid4(),
                name="test_name",
                description="test_description",
                category=ProductCategory.BREAD,
                price=100,
            )
        )


async def test__delete_by_id(
    product_service: ProductService,
    create_product: Callable,
) -> None:
    db_product: ProductTable = await create_product()
    await product_service.delete_by_id(input_id=db_product.id)
    assert db_product.deleted_at is not None


async def test__delete_by_id__entity_not_found_exception(
    product_service: ProductService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await product_service.delete_by_id(input_id=uuid4()) is None
