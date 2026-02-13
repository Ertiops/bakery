from typing import Any

from aiogram_dialog.api.protocols import DialogManager

from bakery.domains.entities.cart import CartListParams
from bakery.domains.services.cart import CartService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.content.messages.cart import user as user_cart_msg
from bakery.presenters.bot.dialogs.utils.order_for_user import get_order_for_user_id


async def get_cart_data(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    cart_service: CartService = await container.get(CartService)
    uow: AbstractUow = await container.get(AbstractUow)
    user_id = get_order_for_user_id(dialog_manager)
    async with uow:
        carts = await cart_service.get_list(
            input_dto=CartListParams(
                user_id=user_id,
                has_non_zero_quantity=True,
            )
        )
        if not carts:
            dialog_manager.dialog_data["cart_item_index"] = {}
            return dict(cart_text=user_cart_msg.CART_EMPTY)
    lines = []
    total = 0
    cart_items = []
    cart_item_index: dict[str, str] = {}
    for idx, cart in enumerate(carts, start=1):
        subtotal = cart.product.price * cart.quantity
        lines.append(user_cart_msg.CART_ITEM.format(cart=cart, subtotal=subtotal))
        total += subtotal
        idx_str = str(idx)
        cart_items.append(
            dict(
                idx=idx_str,
                product_id=str(cart.product.id),
                name=cart.product.name,
                quantity=cart.quantity,
            )
        )
        cart_item_index[idx_str] = str(cart.product.id)
    dialog_manager.dialog_data["cart_item_index"] = cart_item_index

    return dict(
        cart_text="\n".join(lines)
        + "\n\n"
        + user_cart_msg.CART_TOTAL.format(total=total),
        carts=cart_items,
    )
