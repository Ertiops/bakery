from dishka import Provider, Scope, provide

from bakery_bot.adapters.http.tg_client.tg_client import TGClient
from bakery_bot.adapters.http.vk_client.vk_client import VKClient
from bakery_bot.common.config import Config
from bakery_bot.domains.file_service import FileService


class DomainProvider(Provider):
    __config: Config

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.__config = config

    @provide(scope=Scope.REQUEST)
    def file_service(
        self,
        vk_client: VKClient,
        tg_client: TGClient,
    ) -> FileService:
        return FileService(
            config=self.__config,
            vk_client=vk_client,
            tg_client=tg_client,
        )
