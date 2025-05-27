from dishka import Provider, Scope, provide

from bakery_bot.domains.interfaces.storages.user import IUserStorage
from bakery_bot.domains.services.user import UserService


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_service(self, user_storage: IUserStorage) -> UserService:
        return UserService(user_storage=user_storage)
