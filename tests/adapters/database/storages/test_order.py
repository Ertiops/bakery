from collections.abc import Callable, Mapping
from typing import Any
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsStr, IsUUID

from bakery.adapters.database.storages.order import OrderStorage
from bakery.adapters.database.tables import OrderTable, PickupAddressTable, UserTable
from bakery.application.exceptions import (
    EntityNotFoundException,
    ForeignKeyViolationException,
)
from bakery.domains.entities.order import (
    CreateOrder,
    Order,
    OrderListParams,
    OrderStatus,
    UpdateOrder,
)
from tests.utils import now_utc


async def test__create(
    order_storage: OrderStorage,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    create_data = CreateOrder(
        user_id=db_user.id,
        pickup_address_name="pickup_address_name",
        status=OrderStatus.CREATED,
        products=[
            dict(name="name", quantity=2),
        ],
        delivered_at=now_utc().date(),
        total_price=1000,
        delivery_price=200,
        delivered_at_id=1,
        payment_file_id="payment_file_id",
    )
    order = await order_storage.create(input_dto=create_data)
    assert order == Order(
        id=IsUUID,
        user_id=create_data.user_id,
        pickup_address_name=create_data.pickup_address_name,
        status=create_data.status,
        products=create_data.products,
        delivered_at=create_data.delivered_at,
        total_price=create_data.total_price,
        delivery_price=create_data.delivery_price,
        delivered_at_id=create_data.delivered_at_id,
        payment_file_id=IsStr,
        rating=create_data.rating,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__create__foreign_key_violation_exception__user_id(
    order_storage: OrderStorage,
    create_pickup_address: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    create_data = CreateOrder(
        user_id=uuid4(),
        pickup_address_name=db_pickup_address.name,
        status=OrderStatus.CREATED,
        products=[
            dict(name="name", quantity=2),
        ],
        delivered_at=now_utc().date(),
        total_price=1000,
        delivery_price=200,
        delivered_at_id=1,
        payment_file_id="payment_file_id",
    )
    with pytest.raises(ForeignKeyViolationException):
        await order_storage.create(input_dto=create_data)


async def test__get_by_id(
    order_storage: OrderStorage,
    create_order: Callable,
) -> None:
    db_order: OrderTable = await create_order()
    order = await order_storage.get_by_id(input_id=db_order.id)
    assert order == Order(
        id=db_order.id,
        user_id=db_order.user_id,
        pickup_address_name=db_order.pickup_address_name,
        status=db_order.status,
        products=db_order.products,
        delivered_at=db_order.delivered_at,
        total_price=db_order.total_price,
        delivery_price=db_order.delivery_price,
        delivered_at_id=db_order.delivered_at_id,
        payment_file_id=db_order.payment_file_id,
        rating=db_order.rating,
        created_at=db_order.created_at,
        updated_at=db_order.updated_at,
    )


async def test__get_by_id__none(order_storage: OrderStorage) -> None:
    assert await order_storage.get_by_id(input_id=uuid4()) is None


async def test__get_by_id__deleted(
    order_storage: OrderStorage,
    create_order: Callable,
) -> None:
    db_order: OrderTable = await create_order(deleted_at=now_utc())
    assert await order_storage.get_by_id(input_id=db_order.id) is None


async def test__get_list(
    order_storage: OrderStorage,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    db_orders: list[OrderTable] = [
        await create_order(pickup_address_name=db_pickup_address.name) for _ in range(2)
    ][::-1]
    orders = await order_storage.get_list(input_dto=OrderListParams(limit=10, offset=0))
    assert orders == [
        Order(
            id=db_order.id,
            user_id=db_order.user_id,
            pickup_address_name=db_order.pickup_address_name,
            status=db_order.status,
            products=db_order.products,
            delivered_at=db_order.delivered_at,
            total_price=db_order.total_price,
            delivery_price=db_order.delivery_price,
            delivered_at_id=db_order.delivered_at_id,
            payment_file_id=db_order.payment_file_id,
            rating=db_order.rating,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at,
        )
        for db_order in db_orders
    ]


async def test__get_list__validate_limit(
    order_storage: OrderStorage,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    db_orders: list[OrderTable] = [
        await create_order(pickup_address_name=db_pickup_address.name) for _ in range(2)
    ][::-1]
    orders = await order_storage.get_list(input_dto=OrderListParams(limit=1, offset=0))
    assert (
        orders
        == [
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_name=db_order.pickup_address_name,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                total_price=db_order.total_price,
                delivery_price=db_order.delivery_price,
                delivered_at_id=db_order.delivered_at_id,
                payment_file_id=db_order.payment_file_id,
                rating=db_order.rating,
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
            for db_order in db_orders
        ][:1]
    )


async def test__get_list__validate_offset(
    order_storage: OrderStorage,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    db_orders: list[OrderTable] = [
        await create_order(pickup_address_name=db_pickup_address.name) for _ in range(2)
    ][::-1]
    orders = await order_storage.get_list(input_dto=OrderListParams(limit=2, offset=1))
    assert (
        orders
        == [
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_name=db_order.pickup_address_name,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                total_price=db_order.total_price,
                delivery_price=db_order.delivery_price,
                delivered_at_id=db_order.delivered_at_id,
                payment_file_id=db_order.payment_file_id,
                rating=db_order.rating,
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
            for db_order in db_orders
        ][1:]
    )


async def test__get_list__validate_order(
    order_storage: OrderStorage,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    db_orders: list[OrderTable] = [
        await create_order(
            pickup_address_name=db_pickup_address.name, created_at=now_utc(days=-i)
        )
        for i in range(2)
    ][::-1]
    orders = await order_storage.get_list(input_dto=OrderListParams(limit=10, offset=0))
    assert (
        orders
        == [
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_name=db_order.pickup_address_name,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                total_price=db_order.total_price,
                delivery_price=db_order.delivery_price,
                delivered_at_id=db_order.delivered_at_id,
                payment_file_id=db_order.payment_file_id,
                rating=db_order.rating,
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
            for db_order in db_orders
        ][::-1]
    )


async def test__get_list__validate_filter__delivered_at(
    order_storage: OrderStorage,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    delivered_at = now_utc().date()
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    await create_order(delivered_at=now_utc(days=1).date())
    db_order: OrderTable = await create_order(
        pickup_address_name=db_pickup_address.name, delivered_at=delivered_at
    )
    orders = await order_storage.get_list(
        input_dto=OrderListParams(
            limit=10,
            offset=0,
            delivered_at=delivered_at,
        )
    )
    assert orders == [
        Order(
            id=db_order.id,
            user_id=db_order.user_id,
            pickup_address_name=db_order.pickup_address_name,
            status=db_order.status,
            products=db_order.products,
            delivered_at=db_order.delivered_at,
            total_price=db_order.total_price,
            delivery_price=db_order.delivery_price,
            delivered_at_id=db_order.delivered_at_id,
            payment_file_id=db_order.payment_file_id,
            rating=db_order.rating,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at,
        )
    ]


async def test__get_list__validate_filter__statuses(
    order_storage: OrderStorage,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    await create_order(status=OrderStatus.DELIVERED)
    db_order: OrderTable = await create_order(
        pickup_address_name=db_pickup_address.name,
        status=OrderStatus.CREATED,
    )
    orders = await order_storage.get_list(
        input_dto=OrderListParams(
            limit=10,
            offset=0,
            statuses=(OrderStatus.CREATED,),
        )
    )
    assert orders == [
        Order(
            id=db_order.id,
            user_id=db_order.user_id,
            pickup_address_name=db_order.pickup_address_name,
            status=db_order.status,
            products=db_order.products,
            delivered_at=db_order.delivered_at,
            total_price=db_order.total_price,
            delivery_price=db_order.delivery_price,
            delivered_at_id=db_order.delivered_at_id,
            payment_file_id=db_order.payment_file_id,
            rating=db_order.rating,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at,
        )
    ]


async def test__get_list__validate_filter__pickup_address_id(
    order_storage: OrderStorage,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    await create_order(
        status=OrderStatus.DELIVERED, delivered_at=now_utc(days=1).date()
    )
    db_order: OrderTable = await create_order(
        pickup_address_name=db_pickup_address.name,
    )
    orders = await order_storage.get_list(
        input_dto=OrderListParams(
            limit=10, offset=0, pickup_address_name=db_pickup_address.name
        )
    )
    assert orders == [
        Order(
            id=db_order.id,
            user_id=db_order.user_id,
            pickup_address_name=db_order.pickup_address_name,
            status=db_order.status,
            products=db_order.products,
            delivered_at=db_order.delivered_at,
            total_price=db_order.total_price,
            delivery_price=db_order.delivery_price,
            delivered_at_id=db_order.delivered_at_id,
            payment_file_id=db_order.payment_file_id,
            rating=db_order.rating,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at,
        )
    ]


async def test__get_list__validate_filter__user_id(
    order_storage: OrderStorage,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    await create_order(
        status=OrderStatus.DELIVERED, delivered_at=now_utc(days=1).date()
    )
    db_order: OrderTable = await create_order(
        pickup_address_name=db_pickup_address.name,
    )
    orders = await order_storage.get_list(
        input_dto=OrderListParams(limit=10, offset=0, user_id=db_order.user_id)
    )
    assert orders == [
        Order(
            id=db_order.id,
            user_id=db_order.user_id,
            pickup_address_name=db_order.pickup_address_name,
            status=db_order.status,
            products=db_order.products,
            delivered_at=db_order.delivered_at,
            total_price=db_order.total_price,
            delivery_price=db_order.delivery_price,
            delivered_at_id=db_order.delivered_at_id,
            payment_file_id=db_order.payment_file_id,
            rating=db_order.rating,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at,
        )
    ]


async def test__get_list__empty_list(
    order_storage: OrderStorage,
) -> None:
    orders = await order_storage.get_list(input_dto=OrderListParams(limit=10, offset=0))
    assert orders == []


async def test__count(
    order_storage: OrderStorage,
    create_order: Callable,
) -> None:
    await create_order()
    assert await order_storage.count(input_dto=OrderListParams(limit=10, offset=0)) == 1


@pytest.mark.parametrize(
    "filters",
    (
        dict(
            statuses=(OrderStatus.CREATED,),
        ),
        dict(
            delivered_at=now_utc().date(),
        ),
    ),
)
async def test__count__validate_filters(
    order_storage: OrderStorage,
    create_pickup_address: Callable,
    create_order: Callable,
    filters: Mapping[str, Any],
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    await create_order(
        status=OrderStatus.DELIVERED, delivered_at=now_utc(days=1).date()
    )
    await create_order(
        pickup_address_name=db_pickup_address.name,
        status=OrderStatus.CREATED,
        delivered_at=now_utc().date(),
    )
    count = await order_storage.count(
        input_dto=OrderListParams(
            limit=10,
            offset=0,
            statuses=filters.get("statuses"),
            delivered_at=filters.get("delivered_at"),
        )
    )
    assert count == 1


async def test__count__validate_filter__pickup_address_name(
    order_storage: OrderStorage,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    await create_order(
        status=OrderStatus.DELIVERED, delivered_at=now_utc(days=1).date()
    )
    await create_order(
        pickup_address_name=db_pickup_address.name,
    )
    count = await order_storage.count(
        input_dto=OrderListParams(
            limit=10, offset=0, pickup_address_name=db_pickup_address.name
        )
    )
    assert count == 1


async def test__count__validate_filter__user_id(
    order_storage: OrderStorage,
    create_order: Callable,
) -> None:
    await create_order(
        status=OrderStatus.DELIVERED, delivered_at=now_utc(days=1).date()
    )
    db_order: OrderTable = await create_order()
    count = await order_storage.count(
        input_dto=OrderListParams(limit=10, offset=0, user_id=db_order.user_id)
    )
    assert count == 1


async def test__count__zero(
    order_storage: OrderStorage,
) -> None:
    assert await order_storage.count(input_dto=OrderListParams(limit=10, offset=0)) == 0


async def test__count_by_delivered_at(
    order_storage: OrderStorage,
    create_order: Callable,
) -> None:
    db_order: OrderTable = await create_order(delivered_at=now_utc().date())
    assert (
        await order_storage.count_by_delivered_at(input_dto=db_order.delivered_at) == 1
    )


async def test__count_by_delivered_at__zero(
    order_storage: OrderStorage,
) -> None:
    assert await order_storage.count_by_delivered_at(input_dto=now_utc().date()) == 0


async def test__exists_by_id(
    order_storage: OrderStorage, create_order: Callable
) -> None:
    db_order: OrderTable = await create_order()
    assert await order_storage.exists_by_id(input_id=db_order.id)


async def test__exists_by_id__false(order_storage: OrderStorage) -> None:
    assert await order_storage.exists_by_id(input_id=uuid4()) is False


async def test__exists_by_id__deleted(
    order_storage: OrderStorage,
    create_order: Callable,
) -> None:
    db_order: OrderTable = await create_order(deleted_at=now_utc())
    assert await order_storage.exists_by_id(input_id=db_order.id) is False


async def test__update_by_id(
    order_storage: OrderStorage,
    create_order: Callable,
    create_pickup_address: Callable,
    create_user: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    db_user: UserTable = await create_user()
    db_order: OrderTable = await create_order()
    update_data = UpdateOrder(
        id=db_order.id,
        user_id=db_user.id,
        pickup_address_name=db_pickup_address.name,
        status=OrderStatus.PAID,
        products=[],
        delivered_at=now_utc().date(),
        total_price=1000,
        delivery_price=200,
        payment_file_id="payment_file_id",
        rating=4,
    )
    order = await order_storage.update_by_id(input_dto=update_data)
    assert order == Order(
        id=db_order.id,
        user_id=update_data.user_id,
        pickup_address_name=update_data.pickup_address_name,
        status=update_data.status,
        products=update_data.products,
        delivered_at=update_data.delivered_at,
        total_price=update_data.total_price,
        delivery_price=update_data.delivery_price,
        delivered_at_id=db_order.delivered_at_id,
        payment_file_id=db_order.payment_file_id,
        rating=update_data.rating,
        created_at=db_order.created_at,
        updated_at=db_order.updated_at,
    )


async def test__update_by_id__foreign_key_violation_exception__user_id(
    order_storage: OrderStorage,
    create_order: Callable,
    create_pickup_address: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    db_order: OrderTable = await create_order()
    update_data = UpdateOrder(
        id=db_order.id,
        user_id=uuid4(),
        pickup_address_name=db_pickup_address.name,
        status=OrderStatus.PAID,
        products=[],
        delivered_at=now_utc().date(),
        total_price=1000,
        delivery_price=200,
        payment_file_id="payment_file_id",
    )
    with pytest.raises(ForeignKeyViolationException):
        await order_storage.update_by_id(input_dto=update_data)


async def test__update_by_id__entity_not_found_exception(
    order_storage: OrderStorage,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await order_storage.update_by_id(input_dto=UpdateOrder(id=uuid4()))


async def test__delete_by_id(
    order_storage: OrderStorage,
    create_order: Callable,
) -> None:
    db_order: OrderTable = await create_order()
    await order_storage.delete_by_id(input_id=db_order.id)
    assert db_order.deleted_at is not None


async def test__delete_by_id__none(order_storage: OrderStorage) -> None:
    assert await order_storage.delete_by_id(input_id=uuid4()) is None
