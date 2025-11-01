from bakery.adapters.database.converters.product import convert_product
from bakery.adapters.database.tables import CartTable, ProductTable
from bakery.domains.entities.cart import Cart, CartWProduct


def convert_cart(
    *,
    result: CartTable,
) -> Cart:
    return Cart(
        user_id=result.user_id,
        product_id=result.product_id,
        quantity=result.quantity,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )


def convert_cart_w_product(
    *,
    result: tuple[CartTable, ProductTable],
) -> CartWProduct:
    cart, product = result
    return CartWProduct(
        user_id=cart.user_id,
        quantity=cart.quantity,
        product=convert_product(result=product),
        created_at=cart.created_at,
        updated_at=cart.updated_at,
    )
