from typing import Any

from aiogram_dialog.api.protocols import DialogManager

from bakery.domains.entities.cart import CartListParams
from bakery.domains.entities.user import User
from bakery.domains.services.cart import CartService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.content.messages.cart import user as user_cart_msg


async def get_cart_data(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, str]:
    container = dialog_manager.middleware_data["dishka_container"]
    cart_service: CartService = await container.get(CartService)
    uow: AbstractUow = await container.get(AbstractUow)
    user: User = dialog_manager.middleware_data["current_user"]
    async with uow:
        carts = await cart_service.get_list(
            input_dto=CartListParams(
                user_id=user.id,
                has_non_zero_quantity=True,
            )
        )
        if not carts:
            return dict(cart_text=user_cart_msg.CART_EMPTY)
    lines = []
    total = 0
    for cart in carts:
        subtotal = cart.product.price * cart.quantity
        lines.append(user_cart_msg.CART_ITEM.format(cart=cart, subtotal=subtotal))
        total += subtotal

    return dict(
        cart_text="\n".join(lines)
        + "\n\n"
        + user_cart_msg.CART_TOTAL.format(total=total)
    )
