from bakery.adapters.database.tables import PickupAddressTable
from bakery.domains.entities.pickup_address import PickupAddress


def convert_pickup_address(
    *,
    result: PickupAddressTable,
) -> PickupAddress:
    return PickupAddress(
        id=result.id,
        name=result.name,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
