import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.storages.pickup_address import PickupAddressStorage
from bakery.adapters.database.storages.product import ProductStorage
from bakery.adapters.database.storages.user import UserStorage
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
