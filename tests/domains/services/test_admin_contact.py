from collections.abc import Awaitable, Callable
from datetime import timedelta
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsUUID

from bakery.adapters.database.tables import AdminContactTable
from bakery.application.exceptions import (
    EntityNotFoundException,
)
from bakery.domains.entities.admin_contact import (
    AdminContact,
    CreateAdminContact,
    UpdateAdminContact,
)
from bakery.domains.services.admin_contact import AdminContactService
from tests.utils import now_utc


async def test__create(
    admin_contact_service: AdminContactService,
) -> None:
    create_data = CreateAdminContact(
        name="test_name",
        tg_username="test_username",
    )
    admin_contact = await admin_contact_service.create(input_dto=create_data)
    assert admin_contact == AdminContact(
        id=IsUUID,
        name=create_data.name,
        tg_username=create_data.tg_username,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__get_last(
    admin_contact_service: AdminContactService,
    create_admin_contact: Callable,
) -> None:
    db_admin_contact: AdminContactTable = await create_admin_contact()
    await create_admin_contact(
        created_at=now_utc() - timedelta(days=1),
    )
    admin_contact = await admin_contact_service.get_last()
    assert admin_contact == AdminContact(
        id=db_admin_contact.id,
        name=db_admin_contact.name,
        tg_username=db_admin_contact.tg_username,
        created_at=db_admin_contact.created_at,
        updated_at=db_admin_contact.updated_at,
    )


async def test__get_last__entity_not_found_exception(
    admin_contact_service: AdminContactService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await admin_contact_service.get_last()


async def test__update_by_id(
    admin_contact_service: AdminContactService,
    create_admin_contact: Callable[..., Awaitable[AdminContactTable]],
) -> None:
    db_admin_contact = await create_admin_contact()
    update_data = UpdateAdminContact(
        id=db_admin_contact.id,
        name="test_name",
        tg_username="test_username",
    )
    admin_contact = await admin_contact_service.update_by_id(input_dto=update_data)
    assert admin_contact == AdminContact(
        id=db_admin_contact.id,
        name=update_data.name,
        tg_username=update_data.tg_username,
        created_at=db_admin_contact.created_at,
        updated_at=IsDatetime,
    )


async def test__update_by_id__entity_not_found_exception(
    admin_contact_service: AdminContactService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await admin_contact_service.update_by_id(
            input_dto=UpdateAdminContact(
                id=uuid4(),
            )
        )
