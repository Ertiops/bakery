import logging

from aiomisc import Service, entrypoint
from aiomisc_log import LogFormat, LogLevel, basic_config

from bakery.config import MainConfig
from bakery.presenters.bot.service import TelegramBotService

log = logging.getLogger(__name__)


def main() -> None:
    config = MainConfig()

    basic_config()

    services: list[Service] = [
        TelegramBotService(config=config),
        # UserQuestionCronService(config=config),
        # EventReportCronService(config=config),
        # WorkingOffReportCronService(config=config),
        # AbsenceReportService(config=config),
        # CleanReportCronService(config=config),
        # SendingMessageCronService(config=config),
        # PracticeFeedbackCronService(config=config),
    ]

    with entrypoint(
        *services,
        log_level=LogLevel.info,
        log_format=LogFormat.color,
        pool_size=4,
        debug=True,
    ) as loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
