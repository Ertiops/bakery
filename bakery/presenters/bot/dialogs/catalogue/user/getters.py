import logging
from collections.abc import Sequence
from typing import Any
from uuid import UUID

from aiogram.types import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.api.protocols import DialogManager

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.cart import GetCartByUserProductIds
from bakery.domains.entities.product import Product, ProductCategory, ProductListParams
from bakery.domains.entities.user import User
from bakery.domains.services.cart import CartService
from bakery.domains.services.order import OrderService
from bakery.domains.services.product import ProductService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.utils.order_edit import get_order_edit_id

log = logging.getLogger(__name__)


async def get_products_data(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Sequence[Product]]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await dialog_manager.middleware_data["dishka_container"].get(
        AbstractUow
    )
    service: ProductService = await container.get(ProductService)
    category: str = dialog_manager.dialog_data.get(  # type: ignore
        "category"
    ) or dialog_manager.start_data.get("category")  # type: ignore[union-attr]
    if category:
        dialog_manager.dialog_data["category"] = category
    order_edit_id = get_order_edit_id(dialog_manager)
    if order_edit_id:
        dialog_manager.dialog_data["order_edit_id"] = order_edit_id
    log.info("Fetching products for category: %s", category)
    async with uow:
        product_list = await service.get_list(
            input_dto=ProductListParams(
                category=ProductCategory(category), limit=50, offset=0
            )
        )
    return dict(products=product_list.items)


async def get_selected_product(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    product_service: ProductService = await container.get(ProductService)
    cart_service: CartService = await container.get(CartService)
    order_service: OrderService = await container.get(OrderService)
    user: User = dialog_manager.middleware_data["current_user"]
    product_id: UUID = dialog_manager.start_data.get(  # type: ignore
        "product_id"
    ) or dialog_manager.dialog_data.get("product_id")
    log.info("Fetching product with ID: %s", product_id)
    order_edit_id = get_order_edit_id(dialog_manager)
    async with uow:
        product = await product_service.get_by_id(input_id=UUID(product_id))  # type: ignore[arg-type]
        quantity = 0
        if order_edit_id:
            try:
                order = await order_service.get_by_id(input_id=UUID(order_edit_id))
                for item in order.products:
                    if item["id"] == str(product.id):
                        quantity = item["quantity"]
                        break
            except (EntityNotFoundException, ValueError):
                quantity = 0
        else:
            try:
                cart = await cart_service.get_w_product_by_user_product_ids(
                    input_dto=GetCartByUserProductIds(
                        user_id=user.id,
                        product_id=product_id,
                    )
                )
                quantity = cart.quantity
            except EntityNotFoundException:
                quantity = 0
    if quantity is None:
        quantity = 0
    dialog_manager.dialog_data.update(
        dict(
            product_id=str(product.id),
            original_name=product.name,
            original_description=product.description,
            original_price=product.price,
            quantity=quantity,
        )
    )
    photo_attachment = (
        MediaAttachment(
            type=ContentType.PHOTO,
            file_id=MediaId(product.photo_file_id),
        )
        if product.photo_file_id
        else None
    )
    return dict(
        product=product,
        quantity=quantity,
        product_photo_attachment=photo_attachment,
        has_order_edit=bool(order_edit_id),
    )
