from bakery.adapters.database.tables import OrderTable
from bakery.domains.entities.order import Order


def convert_order_to_dto(
    *,
    result: OrderTable,
) -> Order:
    return Order(
        id=result.id,
        user_id=result.user_id,
        pickup_address_name=result.pickup_address_name,
        status=result.status,
        products=result.products,
        delivered_at=result.delivered_at,
        total_price=result.total_price,
        delivery_price=result.delivery_price,
        delivered_at_id=result.delivered_at_id,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
