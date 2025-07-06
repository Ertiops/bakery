from collections.abc import Callable
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsUUID

from bakery.adapters.database.tables import PickupAddressTable
from bakery.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from bakery.domains.entities.pickup_address import (
    CreatePickupAddress,
    PickupAddress,
    PickupAddressList,
    PickupAddressListParams,
    UpdatePickupAddress,
)
from bakery.domains.services.pickup_address import PickupAddressService


async def test__create(
    pickup_address_service: PickupAddressService,
) -> None:
    create_data = CreatePickupAddress(
        name="test_name",
    )
    pickup_address = await pickup_address_service.create(input_dto=create_data)
    assert pickup_address == PickupAddress(
        id=IsUUID,
        name=create_data.name,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__create__entity_already_exists_exception(
    pickup_address_service: PickupAddressService,
    create_pickup_address: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    create_data = CreatePickupAddress(
        name=db_pickup_address.name,
    )
    with pytest.raises(EntityAlreadyExistsException):
        await pickup_address_service.create(input_dto=create_data)


async def test__get_by_id(
    pickup_address_service: PickupAddressService,
    create_pickup_address: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    pickup_address = await pickup_address_service.get_by_id(
        input_id=db_pickup_address.id
    )
    assert pickup_address == PickupAddress(
        id=db_pickup_address.id,
        name=db_pickup_address.name,
        created_at=db_pickup_address.created_at,
        updated_at=db_pickup_address.updated_at,
    )


async def test__get_by_id__entity_not_found_exception(
    pickup_address_service: PickupAddressService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await pickup_address_service.get_by_id(input_id=uuid4())


async def test__get_list(
    pickup_address_service: PickupAddressService,
    create_pickup_address: Callable,
) -> None:
    db_addresses: list[PickupAddressTable] = [
        await create_pickup_address() for _ in range(2)
    ]
    pickup_addresses = await pickup_address_service.get_list(
        input_dto=PickupAddressListParams(limit=10, offset=0)
    )
    assert pickup_addresses == PickupAddressList(
        total=2,
        items=[
            PickupAddress(
                id=a.id,
                name=a.name,
                created_at=a.created_at,
                updated_at=a.updated_at,
            )
            for a in db_addresses
        ],
    )


async def test__get_list__validate_limit(
    pickup_address_service: PickupAddressService,
    create_pickup_address: Callable,
) -> None:
    db_pickup_addresses: list[PickupAddressTable] = [
        await create_pickup_address() for _ in range(2)
    ]
    pickup_addresses = await pickup_address_service.get_list(
        input_dto=PickupAddressListParams(limit=1, offset=0)
    )
    assert pickup_addresses == PickupAddressList(
        total=2,
        items=[
            PickupAddress(
                id=a.id,
                name=a.name,
                created_at=a.created_at,
                updated_at=a.updated_at,
            )
            for a in db_pickup_addresses
        ][:1],
    )


async def test__get_list__validate_offset(
    pickup_address_service: PickupAddressService,
    create_pickup_address: Callable,
) -> None:
    db_pickup_addresses: list[PickupAddressTable] = [
        await create_pickup_address() for _ in range(2)
    ]
    pickup_addresses = await pickup_address_service.get_list(
        input_dto=PickupAddressListParams(limit=2, offset=1)
    )
    assert pickup_addresses == PickupAddressList(
        total=2,
        items=[
            PickupAddress(
                id=a.id,
                name=a.name,
                created_at=a.created_at,
                updated_at=a.updated_at,
            )
            for a in db_pickup_addresses
        ][1:],
    )


async def test__get_list__empty_list(
    pickup_address_service: PickupAddressService,
) -> None:
    pickup_addresses = await pickup_address_service.get_list(
        input_dto=PickupAddressListParams(limit=10, offset=0)
    )
    assert pickup_addresses == PickupAddressList(total=0, items=[])


async def test__update_by_id(
    pickup_address_service: PickupAddressService,
    create_pickup_address: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    update_data = UpdatePickupAddress(
        id=db_pickup_address.id,
        name="test_name",
    )
    pickup_address = await pickup_address_service.update_by_id(input_dto=update_data)
    assert pickup_address == PickupAddress(
        id=db_pickup_address.id,
        name=update_data.name,
        created_at=db_pickup_address.created_at,
        updated_at=IsDatetime,
    )


async def test__update_by_id__entity_already_exists_exception(
    pickup_address_service: PickupAddressService,
    create_pickup_address: Callable,
) -> None:
    db_pickup_addresses: list[PickupAddressTable] = [
        await create_pickup_address() for _ in range(2)
    ]
    update_data = UpdatePickupAddress(
        id=db_pickup_addresses[0].id,
        name=db_pickup_addresses[1].name,
    )
    with pytest.raises(EntityAlreadyExistsException):
        await pickup_address_service.update_by_id(input_dto=update_data)


async def test__update_by_id__entity_not_found_exception(
    pickup_address_service: PickupAddressService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await pickup_address_service.update_by_id(
            input_dto=UpdatePickupAddress(
                id=uuid4(),
            )
        )


async def test__delete_by_id(
    pickup_address_service: PickupAddressService,
    create_pickup_address: Callable,
) -> None:
    db_pickup_address: PickupAddressTable = await create_pickup_address()
    await pickup_address_service.delete_by_id(input_id=db_pickup_address.id)
    assert db_pickup_address.deleted_at is not None


async def test__delete_by_id__entity_not_found_exception(
    pickup_address_service: PickupAddressService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await pickup_address_service.delete_by_id(input_id=uuid4())
