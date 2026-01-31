from bakery.adapters.database.tables import OrderPaymentTable
from bakery.domains.entities.order_payment import OrderPayment


def convert_order_payment(
    *,
    result: OrderPaymentTable,
) -> OrderPayment:
    return OrderPayment(
        id=result.id,
        phone=result.phone,
        banks=result.banks,
        addressee=result.addressee,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
