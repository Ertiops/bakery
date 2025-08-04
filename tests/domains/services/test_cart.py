from collections.abc import Callable
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsInstance, IsList
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import CartTable, ProductTable, UserTable
from bakery.application.exceptions import (
    EntityNotFoundException,
    ForeignKeyViolationException,
)
from bakery.domains.entities.cart import (
    Cart,
    CartListParams,
    CartWProduct,
    CreateCart,
    GetCartByUserProductIds,
)
from bakery.domains.entities.product import Product
from bakery.domains.services.cart import CartService
from tests.utils import now_utc


async def test__create_or_update_by_id__validate_create(
    cart_service: CartService,
    create_user: Callable,
    create_product: Callable,
) -> None:
    db_user: UserTable = await create_user()
    db_product: ProductTable = await create_product()
    create_data = CreateCart(
        user_id=db_user.id,
        product_id=db_product.id,
        quantity=1,
    )
    cart = await cart_service.create_or_update(input_dto=create_data)
    assert cart == Cart(
        user_id=db_user.id,
        product_id=create_data.product_id,
        quantity=create_data.quantity,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__create_or_update_by_id__validate_update(
    cart_service: CartService,
    create_cart: Callable,
    session: AsyncSession,
) -> None:
    db_cart: CartTable = await create_cart()
    create_data = CreateCart(
        user_id=db_cart.user_id,
        product_id=db_cart.product_id,
        quantity=3,
    )
    await cart_service.create_or_update(input_dto=create_data)
    await session.refresh(db_cart)
    assert db_cart.quantity == 3


async def test__create__entity_not_found_exception__user_id(
    create_product: Callable,
    cart_service: CartService,
) -> None:
    db_product: ProductTable = await create_product()
    create_data = CreateCart(
        user_id=uuid4(),
        product_id=db_product.id,
        quantity=1,
    )
    with pytest.raises(ForeignKeyViolationException):
        await cart_service.create_or_update(input_dto=create_data)


async def test__create__entity_not_found_exception__product_id(
    create_user: UserTable,
    cart_service: CartService,
) -> None:
    db_user: UserTable = await create_user()
    create_data = CreateCart(
        user_id=db_user.id,
        product_id=uuid4(),
        quantity=1,
    )
    with pytest.raises(ForeignKeyViolationException):
        await cart_service.create_or_update(input_dto=create_data)


async def test__get_w_product_by_user_product_ids(
    cart_service: CartService,
    create_cart: Callable,
) -> None:
    db_cart: CartTable = await create_cart()
    cart = await cart_service.get_w_product_by_user_product_ids(
        input_dto=GetCartByUserProductIds(
            user_id=db_cart.user_id,
            product_id=db_cart.product_id,
        )
    )
    assert cart == CartWProduct(
        user_id=db_cart.user_id,
        quantity=db_cart.quantity,
        product=IsInstance(Product),
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__get_w_product_by_user_product_ids__none(
    cart_service: CartService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await cart_service.get_w_product_by_user_product_ids(
            input_dto=GetCartByUserProductIds(
                user_id=uuid4(),
                product_id=uuid4(),
            )
        )


async def test__get_w_product_by_user_product_ids__none__validate_deleted_product(
    cart_service: CartService,
    create_cart: Callable,
    create_product: Callable,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    db_product: ProductTable = await create_product(deleted_at=now_utc())
    db_cart: CartTable = await create_cart(
        user_id=db_user.id,
        product_id=db_product.id,
    )
    with pytest.raises(EntityNotFoundException):
        await cart_service.get_w_product_by_user_product_ids(
            input_dto=GetCartByUserProductIds(
                user_id=db_cart.user_id,
                product_id=db_cart.product_id,
            )
        )


async def test__get_list(
    cart_service: CartService,
    create_cart: Callable,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    db_carts: list[CartTable] = [
        await create_cart(user_id=db_user.id) for i in range(2)
    ]
    carts = await cart_service.get_list(
        input_dto=CartListParams(
            user_id=None,
            has_non_zero_quantity=False,
        )
    )
    assert carts == IsList(
        *[
            CartWProduct(
                user_id=db_cart.user_id,
                quantity=db_cart.quantity,
                product=IsInstance(Product),
                created_at=IsDatetime,
                updated_at=IsDatetime,
            )
            for db_cart in db_carts
        ],
        check_order=False,
        length=len(db_carts),
    )


async def test__get_list__validate_filter__user_id(
    cart_service: CartService,
    create_cart: Callable,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    db_carts: list[CartTable] = [
        await create_cart(user_id=db_user.id) for i in range(2)
    ]
    await create_cart()
    carts = await cart_service.get_list(
        input_dto=CartListParams(
            user_id=db_user.id,
            has_non_zero_quantity=False,
        )
    )
    assert carts == [
        CartWProduct(
            user_id=db_cart.user_id,
            quantity=db_cart.quantity,
            product=IsInstance(Product),
            created_at=IsDatetime,
            updated_at=IsDatetime,
        )
        for db_cart in db_carts
    ]


async def test__get_list__validate_filter__has_non_zero_quantity(
    cart_service: CartService,
    create_cart: Callable,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    db_carts: list[CartTable] = [
        await create_cart(user_id=db_user.id, quantity=i) for i in range(2)
    ]
    carts = await cart_service.get_list(
        input_dto=CartListParams(
            user_id=None,
            has_non_zero_quantity=True,
        )
    )
    assert (
        carts
        == [
            CartWProduct(
                user_id=db_cart.user_id,
                quantity=db_cart.quantity,
                product=IsInstance(Product),
                created_at=IsDatetime,
                updated_at=IsDatetime,
            )
            for db_cart in db_carts
        ][1:]
    )


async def test__get_list__validate_deleted_product(
    cart_service: CartService,
    create_cart: Callable,
    create_product: Callable,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    db_products: list[ProductTable] = [await create_product()]
    db_products.append(await create_product(deleted_at=now_utc()))
    db_carts: list[CartTable] = [
        await create_cart(
            user_id=db_user.id,
            product_id=p.id,
        )
        for p in db_products
    ]
    carts = await cart_service.get_list(
        input_dto=CartListParams(
            user_id=None,
            has_non_zero_quantity=False,
        )
    )
    assert (
        carts
        == [
            CartWProduct(
                user_id=db_cart.user_id,
                quantity=db_cart.quantity,
                product=IsInstance(Product),
                created_at=IsDatetime,
                updated_at=IsDatetime,
            )
            for db_cart in db_carts
        ][:1]
    )


async def test__get_list_by_user_id__validate_deleted_cart(
    cart_service: CartService,
    create_cart: Callable,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    db_carts: list[CartTable] = [await create_cart(user_id=db_user.id)]
    db_carts.append(await create_cart(user_id=db_user.id, deleted_at=now_utc()))
    carts = await cart_service.get_list(
        input_dto=CartListParams(
            user_id=None,
            has_non_zero_quantity=False,
        )
    )
    assert (
        carts
        == [
            CartWProduct(
                user_id=db_cart.user_id,
                quantity=db_cart.quantity,
                product=IsInstance(Product),
                created_at=IsDatetime,
                updated_at=IsDatetime,
            )
            for db_cart in db_carts
        ][:1]
    )
