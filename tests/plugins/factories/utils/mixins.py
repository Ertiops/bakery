from datetime import UTC, datetime
from uuid import UUID

from tests.plugins.factories.utils.iteruse import IterUse


class TimestampedFactoryMixin:
    @classmethod
    def created_at(cls) -> datetime:
        return datetime.now(tz=UTC)

    @classmethod
    def updated_at(cls) -> datetime:
        return datetime.now(tz=UTC)

    @classmethod
    def deleted_at(cls) -> None:
        return None


class IdentifableFactoryMixin:
    _id_iter = IterUse(lambda i: UUID(int=i))

    @classmethod
    def id(cls) -> UUID:
        return cls._id_iter.next()
