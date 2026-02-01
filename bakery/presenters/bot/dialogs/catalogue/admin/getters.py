import logging
from collections.abc import Sequence
from typing import Any
from uuid import UUID

from aiogram.types import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.api.protocols import DialogManager

from bakery.domains.entities.product import Product, ProductCategory, ProductListParams
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


async def get_product_preview_data(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    photo_file_id = dialog_manager.dialog_data.get("photo_file_id")
    original_photo_file_id = dialog_manager.dialog_data.get("original_photo_file_id")
    if photo_file_id is None:
        photo_file_id = original_photo_file_id
    photo_attachment = (
        MediaAttachment(
            type=ContentType.PHOTO,
            file_id=MediaId(photo_file_id),
        )
        if photo_file_id
        else None
    )
    return dict(
        name=dialog_manager.dialog_data.get("name", "<нет>"),
        description=dialog_manager.dialog_data.get("description", "<нет>"),
        price=dialog_manager.dialog_data.get("price", "?"),
        product_preview_attachment=photo_attachment,
    )


async def get_selected_product(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    uow: AbstractUow = await dialog_manager.middleware_data["dishka_container"].get(
        AbstractUow
    )
    service: ProductService = await dialog_manager.middleware_data[
        "dishka_container"
    ].get(ProductService)
    product_id = dialog_manager.start_data.get(  # type: ignore
        "product_id"
    ) or dialog_manager.dialog_data.get("product_id")
    log.info("Fetching product with ID: %s", product_id)
    async with uow:
        product = await service.get_by_id(input_id=UUID(product_id))

    dialog_manager.dialog_data.update(
        {
            "product_id": str(product.id),
            "original_name": product.name,
            "original_description": product.description,
            "original_price": product.price,
            "original_photo_file_id": product.photo_file_id,
        }
    )
    photo_attachment = (
        MediaAttachment(
            type=ContentType.PHOTO,
            file_id=MediaId(product.photo_file_id),
        )
        if product.photo_file_id
        else None
    )
    return dict(product=product, product_photo_attachment=photo_attachment)
