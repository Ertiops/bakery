import logging
from datetime import UTC, datetime, timedelta

from aiomisc.service.cron import CronService
from dishka import make_async_container

from bakery.adapters.database.di import DatabaseProvider
from bakery.config import MainConfig
from bakery.domains.di import DomainProvider
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.services.admin_contact import AdminContactService
from bakery.domains.services.cart import CartService
from bakery.domains.services.delivery_cost import DeliveryCostService
from bakery.domains.services.feedback_group import FeedbackGroupService
from bakery.domains.services.order import OrderService
from bakery.domains.services.order_payment import OrderPaymentService
from bakery.domains.services.order_schedule import OrderScheduleService
from bakery.domains.services.pickup_address import PickupAddressService
from bakery.domains.services.product import ProductService
from bakery.domains.services.user import UserService
from bakery.domains.uow import AbstractUow

log = logging.getLogger(__name__)


class DatabaseCleanerCronService(CronService):
    __required__ = ("config",)
    config: MainConfig

    async def start(self) -> None:
        self.__add_dependency_overrides()
        self.register(self.hard_delete_list, spec="0 0 * * *")
        await super().start()

    async def hard_delete_list(self) -> None:
        async with self.__container() as container:
            uow: AbstractUow = await container.get(AbstractUow)
            user_service: UserService = await container.get(UserService)
            product_service: ProductService = await container.get(ProductService)
            pickup_address_service: PickupAddressService = await container.get(
                PickupAddressService
            )
            cart_service: CartService = await container.get(CartService)
            order_service: OrderService = await container.get(OrderService)
            order_schedule_service: OrderScheduleService = await container.get(
                OrderScheduleService
            )
            admin_contact_service: AdminContactService = await container.get(
                AdminContactService
            )
            delivery_cost_service: DeliveryCostService = await container.get(
                DeliveryCostService
            )
            order_payment_service: OrderPaymentService = await container.get(
                OrderPaymentService
            )
            feedback_group_service: FeedbackGroupService = await container.get(
                FeedbackGroupService
            )
            threshold_date = datetime.now(tz=UTC) - timedelta(days=365)
            input_dto = HardDeleteListParams(deleted_at=threshold_date)
            async with uow:
                await user_service.hard_delete_list(input_dto=input_dto)
                await product_service.hard_delete_list(input_dto=input_dto)
                await pickup_address_service.hard_delete_list(input_dto=input_dto)
                await cart_service.hard_delete_list(input_dto=input_dto)
                await order_service.hard_delete_list(input_dto=input_dto)
                await order_schedule_service.hard_delete_list(input_dto=input_dto)
                await admin_contact_service.hard_delete_list(input_dto=input_dto)
                await delivery_cost_service.hard_delete_list(input_dto=input_dto)
                await order_payment_service.hard_delete_list(input_dto=input_dto)
                await feedback_group_service.hard_delete_list(input_dto=input_dto)
        log.info("Database cleanup completed: %s", threshold_date)

    def __add_dependency_overrides(self) -> None:
        self.__container = make_async_container(
            DatabaseProvider(self.config.db),
            DomainProvider(),
            skip_validation=True,
        )
