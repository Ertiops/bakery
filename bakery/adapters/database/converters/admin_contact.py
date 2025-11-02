from bakery.adapters.database.tables import AdminContactTable
from bakery.domains.entities.admin_contact import AdminContact


def convert_admin_contact(
    *,
    result: AdminContactTable,
) -> AdminContact:
    return AdminContact(
        id=result.id,
        name=result.name,
        tg_username=result.tg_username,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
