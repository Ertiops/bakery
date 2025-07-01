from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, kw_only=True, slots=True)
class DatabaseConfig:
    user: str = field(default_factory=lambda: environ.get("APP_DB_USER", "bakery"))
    password: str = field(
        default_factory=lambda: environ.get("APP_DB_PASSWORD", "bakery")
    )
    name: str = field(default_factory=lambda: environ.get("APP_DB_NAME", "bakery"))
    host: str = field(default_factory=lambda: environ.get("APP_DB_HOST", "127.0.0.1"))
    port: int = field(default_factory=lambda: int(environ.get("APP_DB_PORT", 5432)))
    pool_size: int = field(
        default_factory=lambda: int(environ.get("APP_DB_POOL_SIZE", 10))
    )
    pool_timeout: int = field(
        default_factory=lambda: int(environ.get("APP_DB_POOL_TIMEOUT", 10))
    )
    debug: bool = field(default_factory=lambda: bool(environ.get("APP_DB_DEBUG", True)))

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


@dataclass(frozen=True, slots=True, kw_only=True)
class RedisConfig:
    host: str = field(
        default_factory=lambda: environ.get("APP_REDIS_HOST", "127.0.0.1")
    )
    port: str = field(default_factory=lambda: environ.get("APP_REDIS_PORT", "6379"))
    password: str = field(
        default_factory=lambda: environ.get("APP_REDIS_PASSWORD", "bakery")
    )

    @property
    def dsn(self) -> str:
        return f"redis://:{self.password}@{self.host}:{self.port}"
