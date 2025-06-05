import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.storages.user import UserStorage
from bakery.domains.interfaces.storages.user import IUserStorage


@pytest.fixture
def user_storage(session: AsyncSession) -> IUserStorage:
    return UserStorage(session=session)
