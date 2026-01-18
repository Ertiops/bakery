from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.order_payment import (
    CreateOrderPayment,
    OrderPayment,
    UpdateOrderPayment,
)
from bakery.domains.interfaces.storages.order_payment import IOrderPaymentStorage


class OrderPaymentService:
    __order_payment_storage: IOrderPaymentStorage

    def __init__(self, order_payment_storage: IOrderPaymentStorage) -> None:
        self.__order_payment_storage = order_payment_storage

    async def create(self, *, input_dto: CreateOrderPayment) -> OrderPayment:
        return await self.__order_payment_storage.create(input_dto=input_dto)

    async def get_last(self) -> OrderPayment:
        order_payment = await self.__order_payment_storage.get_last()
        if order_payment is None:
            raise EntityNotFoundException(entity=OrderPayment, entity_id=None)
        return order_payment

    async def update_by_id(self, *, input_dto: UpdateOrderPayment) -> OrderPayment:
        return await self.__order_payment_storage.update_by_id(input_dto=input_dto)
