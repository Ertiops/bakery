from uuid import UUID

from bakery.domains.entities.delivery_cost import DeliveryCost


def calculate_delivery_price(
    *,
    delivery_cost: DeliveryCost,
    pickup_names: set[str],
    pickup_address_id: UUID | None,
    pickup_address_name: str,
    cart_total: int,
) -> int:
    if cart_total <= 0:
        return 0
    if pickup_address_id is not None:
        return 0
    if pickup_address_name in pickup_names:
        return 0
    if (
        delivery_cost.free_delivery_amount is not None
        and cart_total >= delivery_cost.free_delivery_amount
    ):
        return 0
    return delivery_cost.price
