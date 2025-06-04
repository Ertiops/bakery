from dataclasses import dataclass, field

from bakery.adapters.database.config import DatabaseConfig, RedisConfig
from bakery.application.config import (
    AppConfig,
)
from bakery.presenters.bot.config import TgConfig


@dataclass(frozen=True, kw_only=True, slots=True)
class MainConfig:
    db: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())
    redis: RedisConfig = field(default_factory=lambda: RedisConfig())
    app: AppConfig = field(default_factory=lambda: AppConfig())
    bot: TgConfig = field(default_factory=lambda: TgConfig())
