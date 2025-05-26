from dataclasses import dataclass, field
from os import environ


@dataclass
class Config:
    tg_bot_token: str = field(
        default_factory=lambda: environ.get("APP_TG_BOT_TOKEN", "tg_token")
    )
    tg_fontan_id: int = field(
        default_factory=lambda: int(environ.get("APP_TG_FONTAN_ID", 1))
    )
    tg_fort_dialog_id: int = field(
        default_factory=lambda: int(environ.get("APP_TG_FORT_DIALOG_ID", 1))
    )
    tg_test_id: int = field(
        default_factory=lambda: int(environ.get("APP_TG_TEST_ID", 1))
    )
    tg_api_base_url: str = field(
        default_factory=lambda: environ.get(
            "APP_TG_API_BASE_URL", "https://api.telegram.org"
        )
    )
    vk_token: str = field(
        default_factory=lambda: environ.get("APP_VK_TOKEN", "vk_token")
    )
    vk_group_id: int = field(
        default_factory=lambda: int(environ.get("APP_VK_GROUP_ID", 1))
    )
    vk_base_url: str = field(
        default_factory=lambda: environ.get("APP_VK_BASE_URL", "https://api.vk.com")
    )
