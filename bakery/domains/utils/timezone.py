from datetime import UTC, datetime, time
from zoneinfo import ZoneInfo

MOSCOW_TZ = ZoneInfo("Europe/Moscow")


def time_msk_to_utc_time(value: time) -> time:
    local_dt = datetime(
        2000,
        1,
        1,
        value.hour,
        value.minute,
        value.second,
        value.microsecond,
        tzinfo=MOSCOW_TZ,
    )
    return local_dt.astimezone(UTC).time().replace(tzinfo=None)


def time_utc_to_msk_time(value: time) -> time:
    utc_dt = datetime(
        2000,
        1,
        1,
        value.hour,
        value.minute,
        value.second,
        value.microsecond,
        tzinfo=UTC,
    )
    return utc_dt.astimezone(MOSCOW_TZ).time().replace(tzinfo=None)


def format_hhmm(value: time) -> str:
    return value.strftime("%H:%M")


def parse_hhmm(value: str) -> time:
    return datetime.strptime(value, "%H:%M").time()
