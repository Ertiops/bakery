from bakery_bot.adapters.database.tables import UserTable
from bakery_bot.domains.entities.user import User


def convert_user_table_to_dto(
    *,
    result: UserTable,
) -> User:
    return User(
        id=result.id,
        name=result.name,
        tg_id=result.tg_id,
        phone=result.phone,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
