from typing import Any


class BakeryException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class EntityNotFoundException(BakeryException):
    def __init__(self, entity: type, entity_id: Any) -> None:
        super().__init__(f"{entity.__name__} with id {entity_id} not found")


class EmptyPayloadException(BakeryException): ...


class EntityAlreadyExistsException(BakeryException): ...


class StorageException(BakeryException):
    def __init__(self, storage_name: str) -> None:
        super().__init__(f"{storage_name} has failed to execute query")
