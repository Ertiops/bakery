from collections.abc import Sequence
from datetime import date
from uuid import UUID

from bakery.application.constants.common import PAGINATION_LIMIT_BREAKER
from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.delivery_cost import DeliveryCost
from bakery.domains.entities.order import (
    CreateOrder,
    CreateOrderAsUser,
    DeleteOrderParams,
    Order,
    OrderList,
    OrderListByDateWithProductParams,
    OrderListParams,
    OrderListWithDeletedProductsParams,
    OrderListWithUsersParams,
    OrderProduct,
    OrderStatus,
    OrderTopProductsParams,
    OrderWithUser,
    UpdateOrder,
)
from bakery.domains.entities.order_schedule import OrderSchedule
from bakery.domains.entities.pickup_address import PickupAddressListParams
from bakery.domains.entities.product import Product
from bakery.domains.entities.user import User, UserRole
from bakery.domains.interfaces.adapters.order_report_pdf import IOrderReportPdfAdapter
from bakery.domains.interfaces.storages.cart import ICartStorage
from bakery.domains.interfaces.storages.delivery_cost import IDeliveryCostStorage
from bakery.domains.interfaces.storages.order import IOrderStorage
from bakery.domains.interfaces.storages.order_schedule import IOrderScheduleStorage
from bakery.domains.interfaces.storages.pickup_address import IPickupAddressStorage
from bakery.domains.interfaces.storages.user import IUserStorage
from bakery.domains.utils.delivery_price import calculate_delivery_price
from bakery.domains.utils.get_available_delivery_dates import is_order_date_available


class OrderService:
    __order_storage: IOrderStorage
    __order_schedule_storage: IOrderScheduleStorage
    __cart_storage: ICartStorage
    __delivery_cost_storage: IDeliveryCostStorage
    __pickup_address_storage: IPickupAddressStorage
    __user_storage: IUserStorage

    def __init__(
        self,
        order_storage: IOrderStorage,
        order_schedule_storage: IOrderScheduleStorage,
        cart_storage: ICartStorage,
        delivery_cost_storage: IDeliveryCostStorage,
        pickup_address_storage: IPickupAddressStorage,
        user_storage: IUserStorage,
    ) -> None:
        self.__order_storage = order_storage
        self.__order_schedule_storage = order_schedule_storage
        self.__cart_storage = cart_storage
        self.__delivery_cost_storage = delivery_cost_storage
        self.__pickup_address_storage = pickup_address_storage
        self.__user_storage = user_storage

    async def create(self, *, input_dto: CreateOrderAsUser) -> Order:
        order_schedule = await self.__order_schedule_storage.get_last()
        if order_schedule is None:
            raise EntityNotFoundException(
                entity=OrderSchedule,
                entity_id=None,
            )
        if not is_order_date_available(
            order_schedule=order_schedule,
            delivered_at=input_dto.delivered_at,
        ):
            raise ValueError("Дата доставки пока недоступна для заказа.")
        await self.__cart_storage.delete_hard_by_user_id(input_id=input_dto.user_id)
        count_by_delivered_at = await self.__order_storage.count_by_delivered_at(
            input_dto=input_dto.delivered_at
        )
        return await self.__order_storage.create(
            input_dto=CreateOrder(
                user_id=input_dto.user_id,
                pickup_address_name=input_dto.pickup_address_name,
                pickup_address_id=input_dto.pickup_address_id,
                status=OrderStatus.CREATED,
                products=self._normalize_products(input_dto.products),
                delivered_at=input_dto.delivered_at,
                total_price=input_dto.total_price,
                delivery_price=input_dto.delivery_price,
                delivered_at_id=count_by_delivered_at + 1,
                payment_file_id="",
            )
        )

    async def get_by_id(self, *, input_id: UUID) -> Order:
        order = await self.__order_storage.get_by_id(input_id=input_id)
        if order is None:
            raise EntityNotFoundException(entity=Order, entity_id=input_id)
        return order

    async def get_list(self, *, input_dto: OrderListParams) -> OrderList:
        total = await self.__order_storage.count(input_dto=input_dto)
        items = await self.__order_storage.get_list(input_dto=input_dto)
        return OrderList(total=total, items=items)

    async def get_list_with_users_by_date(
        self,
        *,
        input_dto: OrderListWithUsersParams,
        user: User,
    ) -> Sequence[OrderWithUser]:
        _ = user
        return await self.__order_storage.get_list_with_users_by_date(
            input_dto=input_dto
        )

    async def update_by_id(self, *, input_dto: UpdateOrder, user: User) -> Order:
        normalized_input = self._normalize_update_products(input_dto)
        order = await self.__order_storage.get_by_id(input_id=input_dto.id)
        if order is None:
            raise EntityNotFoundException(entity=Order, entity_id=input_dto.id)

        if user.role != UserRole.ADMIN:
            if order.status not in (OrderStatus.CREATED, OrderStatus.CHANGED):
                update_fields = set(normalized_input.to_dict().keys())
                allow_fields = {"payment_file_id", "rating"}
                allow_with_status = (
                    update_fields.issubset(allow_fields | {"status"})
                    and normalized_input.status == OrderStatus.PAID
                    and "payment_file_id" in update_fields
                )
                if update_fields and not (
                    update_fields.issubset(allow_fields) or allow_with_status
                ):
                    return order

        return await self.__order_storage.update_by_id(input_dto=normalized_input)

    async def update_list(self, *, input_dto: Sequence[UpdateOrder]) -> Sequence[Order]:
        normalized_items = [self._normalize_update_products(item) for item in input_dto]
        return await self.__order_storage.update_list(input_dto=normalized_items)

    async def build_order_report_pdf(
        self,
        *,
        delivered_at: date,
        pdf_adapter: IOrderReportPdfAdapter,
        limit: int,
        offset: int = 0,
        user: User,
    ) -> bytes:
        _ = user
        result = await self.get_list(
            input_dto=OrderListParams(
                limit=limit,
                offset=offset,
                delivered_at=delivered_at,
            )
        )
        return pdf_adapter.build_order_report(
            title=f"Заказ на {delivered_at.strftime('%d.%m.%Y')}",
            orders=result.items,
        )

    async def build_delivery_report_pdf(
        self,
        *,
        delivered_at: date,
        pdf_adapter: IOrderReportPdfAdapter,
        limit: int,
        offset: int = 0,
        user: User,
    ) -> bytes:
        items = await self.get_list_with_users_by_date(
            input_dto=OrderListWithUsersParams(
                limit=limit,
                offset=offset,
                delivered_at=delivered_at,
            ),
            user=user,
        )
        orders = [item.order for item in items]
        users_by_id = {item.user.id: item.user for item in items}

        return pdf_adapter.build_delivery_report(
            title=f"Отчет о развозе на {delivered_at.strftime('%d.%m.%Y')}",
            orders=orders,
            users_by_id=users_by_id,
        )

    async def delete_by_id(self, *, input_dto: DeleteOrderParams, user: User) -> None:
        _ = user
        if not await self.__order_storage.exists_by_id(input_id=input_dto.id):
            raise EntityNotFoundException(entity=Order, entity_id=input_dto.id)
        await self.__order_storage.delete_by_id(input_dto=input_dto)

    async def remove_product_from_orders_by_date(
        self, *, input_dto: OrderListByDateWithProductParams, user: User
    ) -> Sequence[Order]:
        _ = user
        orders = await self.__order_storage.get_list_by_date_with_product(
            input_dto=input_dto
        )
        if not orders:
            return []

        delivery_cost = await self.__delivery_cost_storage.get_last()
        if delivery_cost is None:
            raise EntityNotFoundException(entity=DeliveryCost, entity_id=None)

        pickup_addresses = await self.__pickup_address_storage.get_list(
            input_dto=PickupAddressListParams(
                limit=PAGINATION_LIMIT_BREAKER,
                offset=0,
            )
        )
        pickup_names = {item.name for item in pickup_addresses}

        update_items: list[UpdateOrder] = []
        for order in orders:
            updated_products = []
            is_changed = False
            for item in order.products:
                item_deleted = bool(item.get("is_deleted", False))
                if item["id"] == str(input_dto.product_id) and not item_deleted:
                    item = {**item, "is_deleted": True}
                    is_changed = True
                elif "is_deleted" not in item:
                    item = {**item, "is_deleted": False}
                updated_products.append(item)
            if not is_changed:
                continue

            cart_total = sum(
                item["price"] * item["quantity"]
                for item in updated_products
                if not item.get("is_deleted", False)
            )
            delivery_price = calculate_delivery_price(
                delivery_cost=delivery_cost,
                pickup_names=pickup_names,
                pickup_address_id=order.pickup_address_id,
                pickup_address_name=order.pickup_address_name,
                cart_total=cart_total,
            )
            total_price = cart_total + delivery_price

            update_items.append(
                UpdateOrder(
                    id=order.id,
                    products=updated_products,
                    total_price=total_price,
                    delivery_price=delivery_price,
                )
            )
        return await self.__order_storage.update_list(input_dto=update_items)

    async def get_list_with_deleted_products(
        self,
        *,
        input_dto: OrderListWithDeletedProductsParams,
        user: User,
    ) -> OrderList:
        _ = user
        result = await self.get_list(
            input_dto=OrderListParams(
                limit=input_dto.limit,
                offset=input_dto.offset,
                delivered_at=input_dto.delivered_at,
            )
        )
        items = [
            order
            for order in result.items
            if any(item.get("is_deleted", False) for item in order.products)
        ]
        return OrderList(total=len(items), items=items)

    async def get_top_products_for_user(
        self, *, input_dto: OrderTopProductsParams
    ) -> Sequence[Product]:
        return await self.__order_storage.get_top_products_for_user(input_dto=input_dto)

    def _normalize_products(
        self, products: Sequence[OrderProduct]
    ) -> Sequence[OrderProduct]:
        return [
            {**item, "is_deleted": bool(item.get("is_deleted", False))}
            for item in products
        ]

    def _normalize_update_products(self, input_dto: UpdateOrder) -> UpdateOrder:
        data = dict(input_dto.to_dict())
        if "products" in data:
            data["products"] = self._normalize_products(data["products"])
            return UpdateOrder(id=input_dto.id, **data)
        return input_dto
