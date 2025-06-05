import pytest

from bakery.domains.interfaces.storages.user import IUserStorage
from bakery.domains.services.user import UserService


@pytest.fixture
def user_service(user_storage: IUserStorage) -> UserService:
    return UserService(user_storage=user_storage)
