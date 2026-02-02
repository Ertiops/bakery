from bakery.adapters.database.tables import DeliveryCostTable
from bakery.domains.entities.delivery_cost import DeliveryCost


def convert_delivery_cost(
    *,
    result: DeliveryCostTable,
) -> DeliveryCost:
    return DeliveryCost(
        id=result.id,
        price=result.price,
        free_delivery_amount=result.free_delivery_amount,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
