from collections.abc import Callable, Mapping
from typing import Any
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsUUID

from bakery.adapters.database.tables import OrderTable, PickupAddressTable, UserTable
from bakery.application.exceptions import (
    EntityNotFoundException,
    ForeignKeyViolationException,
)
from bakery.domains.entities.order import (
    CreateOrder,
    Order,
    OrderList,
    OrderListParams,
    OrderStatus,
    UpdateOrder,
)
from bakery.domains.entities.pickup_address import PickupAddress
from bakery.domains.services.order import OrderService
from tests.utils import now_utc


async def test__create(
    order_service: OrderService,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    create_data = CreateOrder(
        user_id=db_user.id,
        pickup_address_id=None,
        status=OrderStatus.ON_ACCEPT,
        products=[
            dict(name="name", quantity=2),
        ],
        address="address",
        delivered_at=now_utc().date(),
        price=1000,
    )
    order = await order_service.create(input_dto=create_data)
    assert order == Order(
        id=IsUUID,
        user_id=create_data.user_id,
        pickup_address_id=create_data.pickup_address_id,
        status=create_data.status,
        products=create_data.products,
        delivered_at=create_data.delivered_at,
        price=create_data.price,
        address=create_data.address,
        pickup_address=None,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__create__validate_pickup_address(
    order_service: OrderService,
    create_user: Callable,
    create_pickup_address: Callable,
) -> None:
    db_user: UserTable = await create_user()
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    create_data = CreateOrder(
        user_id=db_user.id,
        pickup_address_id=db_pickup_address.id,
        status=OrderStatus.ON_ACCEPT,
        products=[
            dict(name="name", quantity=2),
        ],
        address="address",
        delivered_at=now_utc().date(),
        price=1000,
    )
    order = await order_service.create(input_dto=create_data)
    assert order == Order(
        id=IsUUID,
        user_id=create_data.user_id,
        pickup_address_id=create_data.pickup_address_id,
        status=create_data.status,
        products=create_data.products,
        delivered_at=create_data.delivered_at,
        price=create_data.price,
        address=create_data.address,
        pickup_address=PickupAddress(
            id=db_pickup_address.id,
            name=db_pickup_address.name,
            created_at=db_pickup_address.created_at,
            updated_at=db_pickup_address.updated_at,
        ),
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__create__foreign_key_violation_exception__user_id(
    order_service: OrderService,
    create_pickup_address: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    create_data = CreateOrder(
        user_id=uuid4(),
        pickup_address_id=db_pickup_address.id,
        status=OrderStatus.ON_ACCEPT,
        products=[
            dict(name="name", quantity=2),
        ],
        address="address",
        delivered_at=now_utc().date(),
        price=1000,
    )
    with pytest.raises(ForeignKeyViolationException):
        await order_service.create(input_dto=create_data)


async def test__create__foreign_key_violation_exception__pickup_address_id(
    order_service: OrderService,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    create_data = CreateOrder(
        user_id=db_user.id,
        pickup_address_id=uuid4(),
        status=OrderStatus.ON_ACCEPT,
        products=[
            dict(name="name", quantity=2),
        ],
        address="address",
        delivered_at=now_utc().date(),
        price=1000,
    )
    with pytest.raises(ForeignKeyViolationException):
        await order_service.create(input_dto=create_data)


async def test__get_by_id(
    order_service: OrderService,
    create_order: Callable,
) -> None:
    db_order: OrderTable = await create_order()
    order = await order_service.get_by_id(input_id=db_order.id)
    assert order == Order(
        id=db_order.id,
        user_id=db_order.user_id,
        pickup_address_id=db_order.pickup_address_id,
        status=db_order.status,
        products=db_order.products,
        delivered_at=db_order.delivered_at,
        price=db_order.price,
        address=db_order.address,
        pickup_address=None,
        created_at=db_order.created_at,
        updated_at=db_order.updated_at,
    )


async def test__get_by_id__validate_pickup_address(
    order_service: OrderService,
    create_order: Callable,
    create_pickup_address: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    db_order: OrderTable = await create_order(pickup_address_id=db_pickup_address.id)
    order = await order_service.get_by_id(input_id=db_order.id)
    assert order == Order(
        id=db_order.id,
        user_id=db_order.user_id,
        pickup_address_id=db_order.pickup_address_id,
        status=db_order.status,
        products=db_order.products,
        delivered_at=db_order.delivered_at,
        price=db_order.price,
        address=db_order.address,
        pickup_address=PickupAddress(
            id=db_pickup_address.id,
            name=db_pickup_address.name,
            created_at=db_pickup_address.created_at,
            updated_at=db_pickup_address.updated_at,
        ),
        created_at=db_order.created_at,
        updated_at=db_order.updated_at,
    )


async def test__get_by_id__entity_not_found_exception(
    order_service: OrderService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await order_service.get_by_id(input_id=uuid4())


async def test__get_by_id__deleted(
    order_service: OrderService,
    create_order: Callable,
) -> None:
    db_order: OrderTable = await create_order(deleted_at=now_utc())
    with pytest.raises(EntityNotFoundException):
        await order_service.get_by_id(input_id=db_order.id)


async def test__get_list(
    order_service: OrderService,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    db_orders: list[OrderTable] = [
        await create_order(pickup_address_id=db_pickup_address.id) for _ in range(2)
    ]
    orders = await order_service.get_list(input_dto=OrderListParams(limit=10, offset=0))
    assert orders == OrderList(
        total=2,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_id=db_order.pickup_address_id,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                address=db_order.address,
                pickup_address=PickupAddress(
                    id=db_pickup_address.id,
                    name=db_pickup_address.name,
                    created_at=db_pickup_address.created_at,
                    updated_at=db_pickup_address.updated_at,
                ),
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
            for db_order in db_orders
        ],
    )


async def test__get_list__validate_limit(
    order_service: OrderService,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    db_orders: list[OrderTable] = [
        await create_order(pickup_address_id=db_pickup_address.id) for _ in range(2)
    ]
    orders = await order_service.get_list(input_dto=OrderListParams(limit=1, offset=0))
    assert orders == OrderList(
        total=2,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_id=db_order.pickup_address_id,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                address=db_order.address,
                pickup_address=PickupAddress(
                    id=db_pickup_address.id,
                    name=db_pickup_address.name,
                    created_at=db_pickup_address.created_at,
                    updated_at=db_pickup_address.updated_at,
                ),
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
            for db_order in db_orders
        ][:1],
    )


async def test__get_list__validate_offset(
    order_service: OrderService,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    db_orders: list[OrderTable] = [
        await create_order(pickup_address_id=db_pickup_address.id) for _ in range(2)
    ]
    orders = await order_service.get_list(input_dto=OrderListParams(limit=2, offset=1))
    assert orders == OrderList(
        total=2,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_id=db_order.pickup_address_id,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                address=db_order.address,
                pickup_address=PickupAddress(
                    id=db_pickup_address.id,
                    name=db_pickup_address.name,
                    created_at=db_pickup_address.created_at,
                    updated_at=db_pickup_address.updated_at,
                ),
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
            for db_order in db_orders
        ][1:],
    )


async def test__get_list__validate_order(
    order_service: OrderService,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    db_orders: list[OrderTable] = [
        await create_order(
            pickup_address_id=db_pickup_address.id, created_at=now_utc(days=-i)
        )
        for i in range(2)
    ]
    orders = await order_service.get_list(input_dto=OrderListParams(limit=10, offset=0))
    assert orders == OrderList(
        total=2,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_id=db_order.pickup_address_id,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                address=db_order.address,
                pickup_address=PickupAddress(
                    id=db_pickup_address.id,
                    name=db_pickup_address.name,
                    created_at=db_pickup_address.created_at,
                    updated_at=db_pickup_address.updated_at,
                ),
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
            for db_order in db_orders
        ][::-1],
    )


@pytest.mark.parametrize(
    "filters",
    (
        dict(
            status=OrderStatus.ON_ACCEPT,
        ),
        dict(
            delivered_at=now_utc().date(),
        ),
    ),
)
async def test__get_list__validate_filters(
    order_service: OrderService,
    create_pickup_address: Callable,
    create_order: Callable,
    filters: Mapping[str, Any],
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    await create_order(
        status=OrderStatus.DELIVERED, delivered_at=now_utc(days=1).date()
    )
    db_order: OrderTable = await create_order(
        pickup_address_id=db_pickup_address.id, **filters
    )
    orders = await order_service.get_list(
        input_dto=OrderListParams(limit=10, offset=0, **filters)
    )
    assert orders == OrderList(
        total=1,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_id=db_order.pickup_address_id,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                address=db_order.address,
                pickup_address=PickupAddress(
                    id=db_pickup_address.id,
                    name=db_pickup_address.name,
                    created_at=db_pickup_address.created_at,
                    updated_at=db_pickup_address.updated_at,
                ),
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
        ],
    )


async def test__get_list__validate_filter__pickup_address_id(
    order_service: OrderService,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    await create_order(
        status=OrderStatus.DELIVERED, delivered_at=now_utc(days=1).date()
    )
    db_order: OrderTable = await create_order(
        pickup_address_id=db_pickup_address.id,
    )
    orders = await order_service.get_list(
        input_dto=OrderListParams(
            limit=10, offset=0, pickup_address_id=db_pickup_address.id
        )
    )
    assert orders == OrderList(
        total=1,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_id=db_order.pickup_address_id,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                address=db_order.address,
                pickup_address=PickupAddress(
                    id=db_pickup_address.id,
                    name=db_pickup_address.name,
                    created_at=db_pickup_address.created_at,
                    updated_at=db_pickup_address.updated_at,
                ),
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
        ],
    )


async def test__get_list__validate_filter__user_id(
    order_service: OrderService,
    create_pickup_address: Callable,
    create_order: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    await create_order(
        status=OrderStatus.DELIVERED, delivered_at=now_utc(days=1).date()
    )
    db_order: OrderTable = await create_order(
        pickup_address_id=db_pickup_address.id,
    )
    orders = await order_service.get_list(
        input_dto=OrderListParams(limit=10, offset=0, user_id=db_order.user_id)
    )
    assert orders == OrderList(
        total=1,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_id=db_order.pickup_address_id,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                address=db_order.address,
                pickup_address=PickupAddress(
                    id=db_pickup_address.id,
                    name=db_pickup_address.name,
                    created_at=db_pickup_address.created_at,
                    updated_at=db_pickup_address.updated_at,
                ),
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
        ],
    )


async def test__get_list__empty_list(
    order_service: OrderService,
) -> None:
    orders = await order_service.get_list(input_dto=OrderListParams(limit=10, offset=0))
    assert orders == OrderList(total=0, items=[])


async def test__update_by_id(
    order_service: OrderService,
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
        pickup_address_id=db_pickup_address.id,
        status=OrderStatus.PAID,
        products=[],
        address="test_address",
        delivered_at=now_utc().date(),
        price=1000,
    )
    order = await order_service.update_by_id(input_dto=update_data)
    assert order == Order(
        id=db_order.id,
        user_id=update_data.user_id,
        pickup_address_id=update_data.pickup_address_id,
        status=update_data.status,
        products=update_data.products,
        address=update_data.address,
        delivered_at=update_data.delivered_at,
        price=update_data.price,
        pickup_address=PickupAddress(
            id=db_pickup_address.id,
            name=db_pickup_address.name,
            created_at=db_pickup_address.created_at,
            updated_at=db_pickup_address.updated_at,
        ),
        created_at=db_order.created_at,
        updated_at=db_order.updated_at,
    )


async def test__update_by_id__foreign_key_violation_exception__user_id(
    order_service: OrderService,
    create_order: Callable,
    create_pickup_address: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    db_order: OrderTable = await create_order()
    update_data = UpdateOrder(
        id=db_order.id,
        user_id=uuid4(),
        pickup_address_id=db_pickup_address.id,
        status=OrderStatus.PAID,
        products=[],
        address="test_address",
        delivered_at=now_utc().date(),
        price=1000,
    )
    with pytest.raises(ForeignKeyViolationException):
        await order_service.update_by_id(input_dto=update_data)


async def test__update_by_id__foreign_key_violation_exception__pickup_address_id(
    order_service: OrderService,
    create_order: Callable,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    db_order: OrderTable = await create_order()
    update_data = UpdateOrder(
        id=db_order.id,
        user_id=db_user.id,
        pickup_address_id=uuid4(),
        status=OrderStatus.PAID,
        products=[],
        address="test_address",
        delivered_at=now_utc().date(),
        price=1000,
    )
    with pytest.raises(ForeignKeyViolationException):
        await order_service.update_by_id(input_dto=update_data)


async def test__update_by_id__entity_not_found_exception(
    order_service: OrderService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await order_service.update_by_id(input_dto=UpdateOrder(id=uuid4()))


async def test__delete_by_id(
    order_service: OrderService,
    create_order: Callable,
) -> None:
    db_order: OrderTable = await create_order()
    await order_service.delete_by_id(input_id=db_order.id)
    assert db_order.deleted_at is not None


async def test__delete_by_id__entity_not_found_exception(
    order_service: OrderService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await order_service.delete_by_id(input_id=uuid4()) is None
