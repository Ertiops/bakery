from bakery.domains.entities.user import UserRole
from bakery.presenters.bot.dialogs.utils.inline_query import (
    router as inline_query_router,
)
from bakery.presenters.bot.middlewares.user import (
    UserRoleMiddleware,
)

dialog_roles = (
    UserRole.USER,
    UserRole.ADMIN,
)
dialog_middlewares = (UserRoleMiddleware(dialog_roles),)
for m in dialog_middlewares:
    inline_query_router.inline_query.middleware(m)
