from bakery.adapters.database.converters.pickup_address import (
    convert_pickup_address_to_dto,
)
from bakery.adapters.database.tables import OrderTable
from bakery.domains.entities.order import Order


def convert_order_to_dto(
    *,
    result: OrderTable,
) -> Order:
    return Order(
        id=result.id,
        user_id=result.user_id,
        pickup_address_id=result.pickup_address_id,
        status=result.status,
        products=result.products,
        delivered_at=result.delivered_at,
        price=result.price,
        address=result.address,
        pickup_address=convert_pickup_address_to_dto(result=result.pickup_address)
        if result.pickup_address
        else None,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
