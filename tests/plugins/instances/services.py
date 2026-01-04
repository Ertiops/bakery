import pytest

from bakery.domains.interfaces.storages.admin_contact import IAdminContactStorage
from bakery.domains.interfaces.storages.cart import ICartStorage
from bakery.domains.interfaces.storages.order import IOrderStorage
from bakery.domains.interfaces.storages.order_schedule import IOrderScheduleStorage
from bakery.domains.interfaces.storages.pickup_address import IPickupAddressStorage
from bakery.domains.interfaces.storages.product import IProductStorage
from bakery.domains.interfaces.storages.user import IUserStorage
from bakery.domains.services.admin_contact import AdminContactService
from bakery.domains.services.cart import CartService
from bakery.domains.services.order import OrderService
from bakery.domains.services.order_schedule import OrderScheduleService
from bakery.domains.services.pickup_address import PickupAddressService
from bakery.domains.services.product import ProductService
from bakery.domains.services.user import UserService


@pytest.fixture
def user_service(user_storage: IUserStorage) -> UserService:
    return UserService(user_storage=user_storage)


@pytest.fixture
def product_service(product_storage: IProductStorage) -> ProductService:
    return ProductService(product_storage=product_storage)


@pytest.fixture
def pickup_address_service(
    pickup_address_storage: IPickupAddressStorage,
) -> PickupAddressService:
    return PickupAddressService(pickup_address_storage=pickup_address_storage)


@pytest.fixture
def cart_service(cart_storage: ICartStorage) -> CartService:
    return CartService(cart_storage=cart_storage)


@pytest.fixture
def order_service(
    order_storage: IOrderStorage,
    order_schedule_storage: IOrderScheduleStorage,
) -> OrderService:
    return OrderService(
        order_storage=order_storage,
        order_schedule_storage=order_schedule_storage,
    )


@pytest.fixture
def order_schedule_service(
    order_schedule_storage: IOrderScheduleStorage,
) -> OrderScheduleService:
    return OrderScheduleService(order_schedule_storage=order_schedule_storage)


@pytest.fixture
def admin_contact_service(
    admin_contact_storage: IAdminContactStorage,
) -> AdminContactService:
    return AdminContactService(admin_contact_storage=admin_contact_storage)
