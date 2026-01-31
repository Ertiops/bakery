from collections.abc import Awaitable, Callable
from datetime import timedelta
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsUUID

from bakery.adapters.database.storages.order_payment import OrderPaymentStorage
from bakery.adapters.database.tables import OrderPaymentTable
from bakery.application.exceptions import (
    EntityNotFoundException,
)
from bakery.domains.entities.order_payment import (
    CreateOrderPayment,
    OrderPayment,
    UpdateOrderPayment,
)
from tests.utils import now_utc


async def test__create(
    order_payment_storage: OrderPaymentStorage,
) -> None:
    create_data = CreateOrderPayment(
        phone="test_phone",
        banks=["test_bank"],
        addressee="test_addressee",
    )
    order_payment = await order_payment_storage.create(input_dto=create_data)
    assert order_payment == OrderPayment(
        id=IsUUID,
        phone=create_data.phone,
        banks=create_data.banks,
        addressee=create_data.addressee,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__get_last(
    order_payment_storage: OrderPaymentStorage,
    create_order_payment: Callable,
) -> None:
    db_order_payment: OrderPaymentTable = await create_order_payment()
    await create_order_payment(
        created_at=now_utc() - timedelta(days=1),
    )
    order_payment = await order_payment_storage.get_last()
    assert order_payment == OrderPayment(
        id=db_order_payment.id,
        phone=db_order_payment.phone,
        banks=db_order_payment.banks,
        addressee=db_order_payment.addressee,
        created_at=db_order_payment.created_at,
        updated_at=db_order_payment.updated_at,
    )


async def test__get_last__none(
    order_payment_storage: OrderPaymentStorage,
) -> None:
    assert await order_payment_storage.get_last() is None


async def test__update_by_id(
    order_payment_storage: OrderPaymentStorage,
    create_order_payment: Callable[..., Awaitable[OrderPaymentTable]],
) -> None:
    db_order_payment = await create_order_payment()
    update_data = UpdateOrderPayment(
        id=db_order_payment.id,
        phone="test_phone",
        banks=["test_bank"],
        addressee="test_addressee",
    )
    order_payment = await order_payment_storage.update_by_id(input_dto=update_data)
    assert order_payment == OrderPayment(
        id=db_order_payment.id,
        phone=update_data.phone,
        banks=update_data.banks,
        addressee=update_data.addressee,
        created_at=db_order_payment.created_at,
        updated_at=IsDatetime,
    )


async def test__update_by_id__entity_not_found_exception(
    order_payment_storage: OrderPaymentStorage,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await order_payment_storage.update_by_id(
            input_dto=UpdateOrderPayment(
                id=uuid4(),
            )
        )
