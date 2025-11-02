from collections.abc import Callable, Mapping
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsUUID

from bakery.adapters.database.tables import UserTable
from bakery.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from bakery.domains.entities.user import (
    CreateUser,
    UpdateUser,
    User,
    UserList,
    UserListParams,
    UserRole,
)
from bakery.domains.services.user import UserService
from tests.utils import now_utc


async def test__create(
    user_service: UserService,
) -> None:
    create_data = CreateUser(
        name="test_name",
        tg_id=1,
        phone="+79999999999",
        role=UserRole.USER,
    )
    user = await user_service.create(input_dto=create_data)
    assert user == User(
        id=IsUUID,
        name=create_data.name,
        tg_id=create_data.tg_id,
        phone=create_data.phone,
        role=create_data.role,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


@pytest.mark.parametrize(
    "unique_data",
    (
        dict(tg_id=1),
        dict(phone="+79999999999"),
    ),
)
async def test__create__entity_already_exists_exception__username(
    user_service: UserService,
    create_user: Callable,
    unique_data: Mapping[str, int | str],
) -> None:
    db_user: UserTable = await create_user(**unique_data)
    with pytest.raises(EntityAlreadyExistsException):
        await user_service.create(
            input_dto=CreateUser(
                name="test_name",
                tg_id=db_user.tg_id,
                phone=db_user.phone,
                role=UserRole.USER,
            )
        )


async def test__get_by_id(
    user_service: UserService,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    user = await user_service.get_by_id(input_id=db_user.id)
    assert user == User(
        id=db_user.id,
        name=db_user.name,
        tg_id=db_user.tg_id,
        phone=db_user.phone,
        role=db_user.role,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
    )


async def test__get_by_id__entity_not_found_exception(
    user_service: UserService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await user_service.get_by_id(input_id=uuid4())


async def test__get_by_id__entity_not_found_exception__deleted(
    user_service: UserService,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user(deleted_at=now_utc())
    with pytest.raises(EntityNotFoundException):
        await user_service.get_by_id(input_id=db_user.id)


async def test__get_by_tg_id(
    user_service: UserService,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    user = await user_service.get_by_tg_id(input_id=db_user.tg_id)
    assert user == User(
        id=db_user.id,
        name=db_user.name,
        tg_id=db_user.tg_id,
        phone=db_user.phone,
        role=db_user.role,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
    )


async def test__get_by_tg_id__entity_not_found(user_service: UserService) -> None:
    with pytest.raises(EntityNotFoundException):
        await user_service.get_by_tg_id(input_id=1)


async def test__get_by_tg_id__deleted(
    user_service: UserService,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user(deleted_at=now_utc())
    with pytest.raises(EntityNotFoundException):
        await user_service.get_by_tg_id(input_id=db_user.tg_id)


async def test__get_admin(
    user_service: UserService,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user(role=UserRole.ADMIN)
    user = await user_service.get_admin()
    assert user == User(
        id=db_user.id,
        name=db_user.name,
        tg_id=db_user.tg_id,
        phone=db_user.phone,
        role=db_user.role,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
    )


async def test__get_admin__none(
    user_service: UserService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await user_service.get_admin()


async def test__get_admin__deleted(
    user_service: UserService,
    create_user: Callable,
) -> None:
    await create_user(role=UserRole.ADMIN, deleted_at=now_utc())
    with pytest.raises(EntityNotFoundException):
        await user_service.get_admin()


async def test__get_list(
    user_service: UserService,
    create_user: Callable,
) -> None:
    db_users: list[UserTable] = [await create_user() for _ in range(2)]
    users = await user_service.get_list(input_dto=UserListParams(limit=10, offset=0))
    assert users == UserList(
        total=len(db_users),
        items=[
            User(
                id=db_user.id,
                name=db_user.name,
                tg_id=db_user.tg_id,
                phone=db_user.phone,
                role=db_user.role,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at,
            )
            for db_user in db_users
        ],
    )


async def test__get_list__validate_limit(
    user_service: UserService,
    create_user: Callable,
) -> None:
    db_users: list[UserTable] = [await create_user() for _ in range(2)]
    users = await user_service.get_list(input_dto=UserListParams(limit=1, offset=0))
    assert users == UserList(
        total=len(db_users),
        items=[
            User(
                id=db_user.id,
                name=db_user.name,
                tg_id=db_user.tg_id,
                phone=db_user.phone,
                role=db_user.role,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at,
            )
            for db_user in db_users
        ][:1],
    )


async def test__get_list__validate_offset(
    user_service: UserService,
    create_user: Callable,
) -> None:
    db_users: list[UserTable] = [await create_user() for _ in range(2)]
    users = await user_service.get_list(input_dto=UserListParams(limit=1, offset=1))
    assert users == UserList(
        total=len(db_users),
        items=[
            User(
                id=db_user.id,
                name=db_user.name,
                tg_id=db_user.tg_id,
                phone=db_user.phone,
                role=db_user.role,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at,
            )
            for db_user in db_users
        ][1:],
    )


async def test__get_list__empty_list(
    user_service: UserService,
) -> None:
    users = await user_service.get_list(input_dto=UserListParams(limit=10, offset=0))
    assert users == UserList(total=0, items=[])


async def test__update_by_id(
    user_service: UserService,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    update_data = UpdateUser(
        id=db_user.id,
        name="test_name",
        tg_id=1,
        phone="+79999999999",
        role=UserRole.ADMIN,
    )
    user = await user_service.update_by_id(input_dto=update_data)
    assert user == User(
        id=db_user.id,
        name=update_data.name,
        tg_id=update_data.tg_id,
        phone=update_data.phone,
        role=update_data.role,
        created_at=db_user.created_at,
        updated_at=IsDatetime,
    )


async def test__update_by_id__entity_not_found_exception(
    user_service: UserService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await user_service.update_by_id(
            input_dto=UpdateUser(
                id=uuid4(),
                name="test_name",
                tg_id=1,
                phone="+79999999999",
                role=UserRole.ADMIN,
            )
        )


async def test__delete_by_id(
    user_service: UserService,
    create_user: Callable,
) -> None:
    db_user: UserTable = await create_user()
    await user_service.delete_by_id(input_id=db_user.id)
    assert db_user.deleted_at is not None


async def test__delete_by_id__entity_not_found_exception(
    user_service: UserService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await user_service.delete_by_id(input_id=uuid4())
