from collections.abc import Sequence
from typing import Any
from uuid import UUID

from aiogram_dialog.api.protocols import DialogManager

from bakery.domains.entities.product import Product, ProductCategory, ProductListParams
from bakery.domains.services.product import ProductService
from bakery.domains.uow import AbstractUow


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
) -> dict[str, str]:
    return dict(
        name=dialog_manager.dialog_data.get("name", "<нет>"),
        description=dialog_manager.dialog_data.get("description", "<нет>"),
        price=dialog_manager.dialog_data.get("price", "?"),
    )


async def get_selected_product(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Product]:
    uow: AbstractUow = await dialog_manager.middleware_data["dishka_container"].get(
        AbstractUow
    )
    service: ProductService = await dialog_manager.middleware_data[
        "dishka_container"
    ].get(ProductService)
    product_id = dialog_manager.start_data.get(  # type: ignore
        "product_id"
    ) or dialog_manager.dialog_data.get("product_id")
    async with uow:
        product = await service.get_by_id(input_id=UUID(product_id))

    dialog_manager.dialog_data.update(
        dict(
            product_id=str(product.id),
            original_name=product.name,
            original_description=product.description,
            original_price=product.price,
        )
    )
    return dict(product=product)
