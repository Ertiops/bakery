import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.storages.admin_contact import AdminContactStorage
from bakery.adapters.database.storages.cart import CartStorage
from bakery.adapters.database.storages.delivery_cost import DeliveryCostStorage
from bakery.adapters.database.storages.feedback_group import FeedbackGroupStorage
from bakery.adapters.database.storages.order import OrderStorage
from bakery.adapters.database.storages.order_payment import OrderPaymentStorage
from bakery.adapters.database.storages.order_schedule import OrderScheduleStorage
from bakery.adapters.database.storages.pickup_address import PickupAddressStorage
from bakery.adapters.database.storages.product import ProductStorage
from bakery.adapters.database.storages.user import UserStorage
from bakery.domains.interfaces.storages.admin_contact import IAdminContactStorage
from bakery.domains.interfaces.storages.cart import ICartStorage
from bakery.domains.interfaces.storages.delivery_cost import IDeliveryCostStorage
from bakery.domains.interfaces.storages.feedback_group import IFeedbackGroupStorage
from bakery.domains.interfaces.storages.order import IOrderStorage
from bakery.domains.interfaces.storages.order_payment import IOrderPaymentStorage
from bakery.domains.interfaces.storages.order_schedule import IOrderScheduleStorage
from bakery.domains.interfaces.storages.pickup_address import IPickupAddressStorage
from bakery.domains.interfaces.storages.product import IProductStorage
from bakery.domains.interfaces.storages.user import IUserStorage


@pytest.fixture
def user_storage(session: AsyncSession) -> IUserStorage:
    return UserStorage(session=session)


@pytest.fixture
def product_storage(session: AsyncSession) -> IProductStorage:
    return ProductStorage(session=session)


@pytest.fixture
def pickup_address_storage(session: AsyncSession) -> IPickupAddressStorage:
    return PickupAddressStorage(session=session)


@pytest.fixture
def cart_storage(session: AsyncSession) -> ICartStorage:
    return CartStorage(session=session)


@pytest.fixture
def order_storage(session: AsyncSession) -> IOrderStorage:
    return OrderStorage(session=session)


@pytest.fixture
def order_schedule_storage(session: AsyncSession) -> IOrderScheduleStorage:
    return OrderScheduleStorage(session=session)


@pytest.fixture
def admin_contact_storage(session: AsyncSession) -> IAdminContactStorage:
    return AdminContactStorage(session=session)


@pytest.fixture
def delivery_cost_storage(session: AsyncSession) -> IDeliveryCostStorage:
    return DeliveryCostStorage(session=session)


@pytest.fixture
def order_payment_storage(session: AsyncSession) -> IOrderPaymentStorage:
    return OrderPaymentStorage(session=session)


@pytest.fixture
def feedback_group_storage(session: AsyncSession) -> IFeedbackGroupStorage:
    return FeedbackGroupStorage(session=session)
