from bakery.domains.entities.user import UserRole
from bakery.presenters.bot.middlewares.user import (
    UserRoleMiddleware,
)

dialog_roles = (
    UserRole.USER,
    UserRole.ADMIN,
)
dialog_middlewares = (UserRoleMiddleware(dialog_roles),)
