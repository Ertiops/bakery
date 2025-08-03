from typing import Final

CART_ITEM: Final = (
    "• {cart.product.name} - {cart.quantity} × {cart.product.price}₽ = {subtotal}₽"
)
CART_EMPTY: Final = "🧺 Ваша корзина пуста."
CART_TOTAL: Final = "Итого: {total}₽"
