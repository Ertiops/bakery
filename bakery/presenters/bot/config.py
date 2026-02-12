from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, kw_only=True, slots=True)
class TgConfig:
    token: str = field(default_factory=lambda: environ.get("APP_TG_BOT_TOKEN", "token"))
    fsm_state_ttl: int = field(
        default_factory=lambda: int(environ.get("APP_TG_FSM_STATE_TTL", 86400))
    )
    fsm_data_ttl: int = field(
        default_factory=lambda: int(environ.get("APP_TG_FSM_DATA_TTL", 86400))
    )
