from collections.abc import AsyncIterator

from dishka import AnyOf, BaseScope, Component, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from bakery.adapters.database.config import DatabaseConfig
from bakery.adapters.database.storages.admin_contact import AdminContactStorage
from bakery.adapters.database.storages.cart import CartStorage
from bakery.adapters.database.storages.delivery_cost import DeliveryCostStorage
from bakery.adapters.database.storages.order import OrderStorage
from bakery.adapters.database.storages.order_schedule import OrderScheduleStorage
from bakery.adapters.database.storages.pickup_address import PickupAddressStorage
from bakery.adapters.database.storages.product import ProductStorage
from bakery.adapters.database.storages.user import UserStorage
from bakery.adapters.database.uow import SqlalchemyUow
from bakery.adapters.database.utils import create_engine, create_sessionmaker
from bakery.domains.interfaces.storages.admin_contact import IAdminContactStorage
from bakery.domains.interfaces.storages.cart import ICartStorage
from bakery.domains.interfaces.storages.delivery_cost import IDeliveryCostStorage
from bakery.domains.interfaces.storages.order import IOrderStorage
from bakery.domains.interfaces.storages.order_schedule import IOrderScheduleStorage
from bakery.domains.interfaces.storages.pickup_address import IPickupAddressStorage
from bakery.domains.interfaces.storages.product import IProductStorage
from bakery.domains.interfaces.storages.user import IUserStorage
from bakery.domains.uow import AbstractUow


class DatabaseProvider(Provider):
    def __init__(
        self,
        config: DatabaseConfig,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ) -> None:
        self.dsn = config.dsn
        self.debug = config.debug
        super().__init__(scope=scope, component=component)

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        async with create_engine(dsn=self.dsn, debug=self.debug) as engine:
            yield engine

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_sessionmaker(engine=engine)

    @provide(scope=Scope.REQUEST)
    def uow(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AnyOf[SqlalchemyUow, AbstractUow]:
        return SqlalchemyUow(session=session_factory())

    @provide(scope=Scope.REQUEST)
    def user_storage(self, uow: SqlalchemyUow) -> IUserStorage:
        return UserStorage(session=uow.session)

    @provide(scope=Scope.REQUEST)
    def product_storage(self, uow: SqlalchemyUow) -> IProductStorage:
        return ProductStorage(session=uow.session)

    @provide(scope=Scope.REQUEST)
    def pickup_address_storage(self, uow: SqlalchemyUow) -> IPickupAddressStorage:
        return PickupAddressStorage(session=uow.session)

    @provide(scope=Scope.REQUEST)
    def cart_storage(self, uow: SqlalchemyUow) -> ICartStorage:
        return CartStorage(session=uow.session)

    @provide(scope=Scope.REQUEST)
    def order_storage(self, uow: SqlalchemyUow) -> IOrderStorage:
        return OrderStorage(session=uow.session)

    @provide(scope=Scope.REQUEST)
    def order_schedule_storage(self, uow: SqlalchemyUow) -> IOrderScheduleStorage:
        return OrderScheduleStorage(session=uow.session)

    @provide(scope=Scope.REQUEST)
    def admin_contact_storage(self, uow: SqlalchemyUow) -> IAdminContactStorage:
        return AdminContactStorage(session=uow.session)

    @provide(scope=Scope.REQUEST)
    def delivery_cost_storage(self, uow: SqlalchemyUow) -> IDeliveryCostStorage:
        return DeliveryCostStorage(session=uow.session)
