from bakery.adapters.database.tables import UserTable
from bakery.domains.entities.user import User


def convert_user_table_to_dto(
    *,
    result: UserTable,
) -> User:
    return User(
        id=result.id,
        name=result.name,
        tg_id=result.tg_id,
        phone=result.phone,
        role=result.role,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
