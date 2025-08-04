import logging
from collections.abc import Sequence
from typing import Any
from uuid import UUID

from aiogram_dialog.api.protocols import DialogManager

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.cart import GetCartByUserProductIds
from bakery.domains.entities.product import Product, ProductCategory, ProductListParams
from bakery.domains.entities.user import User
from bakery.domains.services.cart import CartService
from bakery.domains.services.product import ProductService
from bakery.domains.uow import AbstractUow

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
    user: User = dialog_manager.middleware_data["current_user"]
    product_id: UUID = dialog_manager.start_data.get(  # type: ignore
        "product_id"
    ) or dialog_manager.dialog_data.get("product_id")
    log.info("Fetching product with ID: %s", product_id)
    async with uow:
        product = await product_service.get_by_id(input_id=UUID(product_id))  # type: ignore[arg-type]
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
    dialog_manager.dialog_data.update(
        dict(
            product_id=str(product.id),
            original_name=product.name,
            original_description=product.description,
            original_price=product.price,
            quantity=quantity,
        )
    )
    return dict(product=product, quantity=quantity)
