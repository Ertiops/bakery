from bakery.adapters.database.tables import ProductTable
from bakery.domains.entities.product import Product


def convert_product_table_to_dto(
    *,
    result: ProductTable,
) -> Product:
    return Product(
        id=result.id,
        name=result.name,
        description=result.description,
        category=result.category,
        weight=result.weight,
        volume=result.volume,
        protein=result.protein,
        fat=result.fat,
        carbohydrate=result.carbohydrate,
        price=result.price,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
