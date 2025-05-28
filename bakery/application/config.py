from dataclasses import dataclass, field
from os import environ


@dataclass
class AppConfig:
    tg_bot_token: str = field(
        default_factory=lambda: environ.get("APP_TG_BOT_TOKEN", "tg_token")
    )
