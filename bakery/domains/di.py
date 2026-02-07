from dishka import Provider, Scope, provide

from bakery.domains.interfaces.storages.admin_contact import IAdminContactStorage
from bakery.domains.interfaces.storages.cart import ICartStorage
from bakery.domains.interfaces.storages.delivery_cost import IDeliveryCostStorage
from bakery.domains.interfaces.storages.feedback_group import IFeedbackGroupStorage
from bakery.domains.interfaces.storages.order import IOrderStorage
from bakery.domains.interfaces.storages.order_payment import IOrderPaymentStorage
from bakery.domains.interfaces.storages.order_schedule import IOrderScheduleStorage
from bakery.domains.interfaces.storages.pickup_address import IPickupAddressStorage
from bakery.domains.interfaces.storages.product import IProductStorage
from bakery.domains.interfaces.storages.user import IUserStorage
from bakery.domains.services.admin_contact import AdminContactService
from bakery.domains.services.cart import CartService
from bakery.domains.services.delivery_cost import DeliveryCostService
from bakery.domains.services.feedback_group import FeedbackGroupService
from bakery.domains.services.order import OrderService
from bakery.domains.services.order_payment import OrderPaymentService
from bakery.domains.services.order_schedule import OrderScheduleService
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

    @provide(scope=Scope.REQUEST)
    def order_service(
        self,
        order_storage: IOrderStorage,
        order_schedule_storage: IOrderScheduleStorage,
        cart_storage: ICartStorage,
        delivery_cost_storage: IDeliveryCostStorage,
        pickup_address_storage: IPickupAddressStorage,
        user_storage: IUserStorage,
    ) -> OrderService:
        return OrderService(
            order_storage=order_storage,
            order_schedule_storage=order_schedule_storage,
            cart_storage=cart_storage,
            delivery_cost_storage=delivery_cost_storage,
            pickup_address_storage=pickup_address_storage,
            user_storage=user_storage,
        )

    @provide(scope=Scope.REQUEST)
    def order_schedule_service(
        self, order_schedule_storage: IOrderScheduleStorage
    ) -> OrderScheduleService:
        return OrderScheduleService(order_schedule_storage=order_schedule_storage)

    @provide(scope=Scope.REQUEST)
    def admin_contact_service(
        self, admin_contact_storage: IAdminContactStorage
    ) -> AdminContactService:
        return AdminContactService(admin_contact_storage=admin_contact_storage)

    @provide(scope=Scope.REQUEST)
    def delivery_cost_service(
        self, delivery_cost_storage: IDeliveryCostStorage
    ) -> DeliveryCostService:
        return DeliveryCostService(delivery_cost_storage=delivery_cost_storage)

    @provide(scope=Scope.REQUEST)
    def order_payment_service(
        self, order_payment_storage: IOrderPaymentStorage
    ) -> OrderPaymentService:
        return OrderPaymentService(order_payment_storage=order_payment_storage)

    @provide(scope=Scope.REQUEST)
    def feedback_group_service(
        self, feedback_group_storage: IFeedbackGroupStorage
    ) -> FeedbackGroupService:
        return FeedbackGroupService(feedback_group_storage=feedback_group_storage)
