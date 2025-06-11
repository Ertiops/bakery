import pytest

from bakery.domains.interfaces.storages.product import IProductStorage
from bakery.domains.interfaces.storages.user import IUserStorage
from bakery.domains.services.product import ProductService
from bakery.domains.services.user import UserService


@pytest.fixture
def user_service(user_storage: IUserStorage) -> UserService:
    return UserService(user_storage=user_storage)


@pytest.fixture
def product_service(product_storage: IProductStorage) -> ProductService:
    return ProductService(product_storage=product_storage)
