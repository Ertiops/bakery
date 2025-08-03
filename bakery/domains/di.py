from dishka import Provider, Scope, provide

from bakery.domains.interfaces.storages.cart import ICartStorage
from bakery.domains.interfaces.storages.pickup_address import IPickupAddressStorage
from bakery.domains.interfaces.storages.product import IProductStorage
from bakery.domains.interfaces.storages.user import IUserStorage
from bakery.domains.services.cart import CartService
from bakery.domains.services.pickup_address import PickupAddressService
from bakery.domains.services.product import ProductService
from bakery.domains.services.user import UserService


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_service(self, user_storage: IUserStorage) -> UserService:
        return UserService(user_storage=user_storage)

    @provide(scope=Scope.REQUEST)
    def product_service(self, product_storage: IProductStorage) -> ProductService:
        return ProductService(product_storage=product_storage)

    @provide(scope=Scope.REQUEST)
    def pickup_address_service(
        self, pickup_address_storage: IPickupAddressStorage
    ) -> PickupAddressService:
        return PickupAddressService(pickup_address_storage=pickup_address_storage)

    @provide(scope=Scope.REQUEST)
    def cart_service(self, cart_storage: ICartStorage) -> CartService:
        return CartService(cart_storage=cart_storage)
