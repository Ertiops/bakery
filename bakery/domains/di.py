from dishka import Provider, Scope, provide

from bakery.domains.interfaces.storages.product import IProductStorage
from bakery.domains.interfaces.storages.user import IUserStorage
from bakery.domains.services.product import ProductService
from bakery.domains.services.user import UserService


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_service(self, user_storage: IUserStorage) -> UserService:
        return UserService(user_storage=user_storage)

    @provide(scope=Scope.REQUEST)
    def product_service(self, product_storage: IProductStorage) -> ProductService:
        return ProductService(product_storage=product_storage)
