from abc import abstractmethod
from collections.abc import Mapping, Sequence
from typing import Protocol
from uuid import UUID

from bakery.domains.entities.order import Order
from bakery.domains.entities.user import User


class IOrderReportPdfAdapter(Protocol):
    @abstractmethod
    def build_order_report(self, *, title: str, orders: Sequence[Order]) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def build_order_pdf(
        self, *, title: str, products: list[dict], free_products: list[dict]
    ) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def build_delivery_report(
        self,
        *,
        title: str,
        orders: Sequence[Order],
        users_by_id: Mapping[UUID, User],
    ) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def build_delivery_pdf(self, *, title: str, groups: list[dict]) -> bytes:
        raise NotImplementedError
