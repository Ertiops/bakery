import pytest

from bakery.domains.interfaces.storages.cart import ICartStorage
from bakery.domains.interfaces.storages.pickup_address import IPickupAddressStorage
from bakery.domains.interfaces.storages.product import IProductStorage
from bakery.domains.interfaces.storages.user import IUserStorage
from bakery.domains.services.cart import CartService
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
