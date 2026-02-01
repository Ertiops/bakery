from bakery.adapters.database.tables import ProductTable
from bakery.domains.entities.product import Product


def convert_product(
    *,
    result: ProductTable,
) -> Product:
    return Product(
        id=result.id,
        name=result.name,
        description=result.description,
        category=result.category,
        price=result.price,
        photo_file_id=result.photo_file_id,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
