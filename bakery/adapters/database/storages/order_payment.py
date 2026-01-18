from typing import NoReturn

from sqlalchemy import insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.converters.order_payment import convert_order_payment
from bakery.adapters.database.tables import OrderPaymentTable
from bakery.application.exceptions import (
    EntityNotFoundException,
    StorageException,
)
from bakery.domains.entities.order_payment import (
    CreateOrderPayment,
    OrderPayment,
    UpdateOrderPayment,
)
from bakery.domains.interfaces.storages.order_payment import IOrderPaymentStorage


class OrderPaymentStorage(IOrderPaymentStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, *, input_dto: CreateOrderPayment) -> OrderPayment:
        stmt = (
            insert(OrderPaymentTable)
            .values(**input_dto.to_dict())
            .returning(OrderPaymentTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_order_payment(result=result)

    async def get_last(self) -> OrderPayment | None:
        stmt = (
            select(OrderPaymentTable)
            .order_by(OrderPaymentTable.created_at.desc())
            .limit(1)
        )
        result = await self.__session.scalar(stmt)
        return convert_order_payment(result=result) if result else None

    async def update_by_id(self, *, input_dto: UpdateOrderPayment) -> OrderPayment:
        stmt = (
            update(OrderPaymentTable)
            .where(OrderPaymentTable.id == input_dto.id)
            .values(**input_dto.to_dict())
            .returning(OrderPaymentTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except NoResultFound as e:
            raise EntityNotFoundException(
                entity=OrderPayment, entity_id=input_dto.id
            ) from e
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_order_payment(result=result)

    def __raise_exception(self, e: DBAPIError) -> NoReturn:
        raise StorageException(self.__class__.__name__) from e
