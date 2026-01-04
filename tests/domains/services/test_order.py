from collections.abc import Callable
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
from bakery.domains.services.order import OrderService
from tests.utils import now_utc


async def test__create(
    order_service: OrderService,
    create_user: Callable,
    create_order_schedule: Callable,
) -> None:
    db_user: UserTable = await create_user()
    await create_order_schedule()
    create_data = CreateOrder(
        user_id=db_user.id,
        pickup_address_name="pickup_address_name",
        status=OrderStatus.CREATED,
        products=[
            dict(name="name", quantity=2),
        ],
        delivered_at=now_utc().date(),
        price=1000,
    )
    order = await order_service.create(input_dto=create_data)
    assert order == Order(
        id=IsUUID,
        user_id=create_data.user_id,
        pickup_address_name=create_data.pickup_address_name,
        status=create_data.status,
        products=create_data.products,
        delivered_at=create_data.delivered_at,
        price=create_data.price,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__create__validate_pickup_address(
    order_service: OrderService,
    create_user: Callable,
    create_pickup_address: Callable,
    create_order_schedule: Callable,
) -> None:
    db_user: UserTable = await create_user()
    await create_order_schedule()
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    create_data = CreateOrder(
        user_id=db_user.id,
        pickup_address_name=db_pickup_address.name,
        status=OrderStatus.CREATED,
        products=[
            dict(name="name", quantity=2),
        ],
        delivered_at=now_utc().date(),
        price=1000,
    )
    order = await order_service.create(input_dto=create_data)
    assert order == Order(
        id=IsUUID,
        user_id=create_data.user_id,
        pickup_address_name=create_data.pickup_address_name,
        status=create_data.status,
        products=create_data.products,
        delivered_at=create_data.delivered_at,
        price=create_data.price,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__create__foreign_key_violation_exception__user_id(
    order_service: OrderService,
    create_pickup_address: Callable,
    create_order_schedule: Callable,
) -> None:
    await create_order_schedule()
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    create_data = CreateOrder(
        user_id=uuid4(),
        pickup_address_name=db_pickup_address.name,
        status=OrderStatus.CREATED,
        products=[
            dict(name="name", quantity=2),
        ],
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
        pickup_address_name=db_order.pickup_address_name,
        status=db_order.status,
        products=db_order.products,
        delivered_at=db_order.delivered_at,
        price=db_order.price,
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
    create_order: Callable,
) -> None:
    db_orders: list[OrderTable] = [await create_order() for _ in range(2)]
    orders = await order_service.get_list(input_dto=OrderListParams(limit=10, offset=0))
    assert orders == OrderList(
        total=2,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_name=db_order.pickup_address_name,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
            for db_order in db_orders
        ],
    )


async def test__get_list__validate_limit(
    order_service: OrderService,
    create_order: Callable,
) -> None:
    db_orders: list[OrderTable] = [await create_order() for _ in range(2)]
    orders = await order_service.get_list(input_dto=OrderListParams(limit=1, offset=0))
    assert orders == OrderList(
        total=2,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_name=db_order.pickup_address_name,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
            for db_order in db_orders
        ][:1],
    )


async def test__get_list__validate_offset(
    order_service: OrderService,
    create_order: Callable,
) -> None:
    db_orders: list[OrderTable] = [await create_order() for _ in range(2)]
    orders = await order_service.get_list(input_dto=OrderListParams(limit=2, offset=1))
    assert orders == OrderList(
        total=2,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_name=db_order.pickup_address_name,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
            for db_order in db_orders
        ][1:],
    )


async def test__get_list__validate_order(
    order_service: OrderService,
    create_order: Callable,
) -> None:
    db_orders: list[OrderTable] = [
        await create_order(created_at=now_utc(days=-i)) for i in range(2)
    ]
    orders = await order_service.get_list(input_dto=OrderListParams(limit=10, offset=0))
    assert orders == OrderList(
        total=2,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_name=db_order.pickup_address_name,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
            for db_order in db_orders
        ][::-1],
    )


async def test__get_list__validate_filter__delivered_at(
    order_service: OrderService,
    create_order: Callable,
) -> None:
    delivered_at = now_utc().date()
    await create_order(delivered_at=now_utc(days=1).date())
    db_order: OrderTable = await create_order(delivered_at=delivered_at)
    orders = await order_service.get_list(
        input_dto=OrderListParams(
            limit=10,
            offset=0,
            delivered_at=delivered_at,
        )
    )
    assert orders == OrderList(
        total=1,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_name=db_order.pickup_address_name,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
        ],
    )


async def test__get_list__validate_filter__statuses(
    order_service: OrderService,
    create_order: Callable,
) -> None:
    await create_order(status=OrderStatus.DELIVERED)
    db_order: OrderTable = await create_order(
        status=OrderStatus.CREATED,
    )
    orders = await order_service.get_list(
        input_dto=OrderListParams(
            limit=10,
            offset=0,
            statuses=(OrderStatus.CREATED,),
        )
    )
    assert orders == OrderList(
        total=1,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_name=db_order.pickup_address_name,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
        ],
    )


async def test__get_list__validate_filter__pickup_address_name(
    order_service: OrderService,
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
    orders = await order_service.get_list(
        input_dto=OrderListParams(
            limit=10, offset=0, pickup_address_name=db_pickup_address.name
        )
    )
    assert orders == OrderList(
        total=1,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_name=db_order.pickup_address_name,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
        ],
    )


async def test__get_list__validate_filter__user_id(
    order_service: OrderService,
    create_order: Callable,
) -> None:
    await create_order(
        status=OrderStatus.DELIVERED, delivered_at=now_utc(days=1).date()
    )
    db_order: OrderTable = await create_order()
    orders = await order_service.get_list(
        input_dto=OrderListParams(limit=10, offset=0, user_id=db_order.user_id)
    )
    assert orders == OrderList(
        total=1,
        items=[
            Order(
                id=db_order.id,
                user_id=db_order.user_id,
                pickup_address_name=db_order.pickup_address_name,
                status=db_order.status,
                products=db_order.products,
                delivered_at=db_order.delivered_at,
                price=db_order.price,
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
        pickup_address_name=db_pickup_address.name,
        status=OrderStatus.PAID,
        products=[],
        delivered_at=now_utc().date(),
        price=1000,
    )
    order = await order_service.update_by_id(input_dto=update_data)
    assert order == Order(
        id=db_order.id,
        user_id=update_data.user_id,
        pickup_address_name=update_data.pickup_address_name,
        status=update_data.status,
        products=update_data.products,
        delivered_at=update_data.delivered_at,
        price=update_data.price,
        created_at=db_order.created_at,
        updated_at=db_order.updated_at,
    )


async def test__update_by_id__foreign_key_violation_exception__user_id(
    order_service: OrderService,
    create_order: Callable,
) -> None:
    db_order: OrderTable = await create_order()
    update_data = UpdateOrder(
        id=db_order.id,
        user_id=uuid4(),
        pickup_address_name="new_pickup_address_name",
        status=OrderStatus.PAID,
        products=[],
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
