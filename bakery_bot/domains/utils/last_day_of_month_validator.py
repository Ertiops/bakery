from datetime import datetime, timedelta


def is_yesterday_last_month(current_date: datetime) -> bool:
    yesterday_date = current_date - timedelta(days=1)
    if yesterday_date.month != current_date.month:
        return True
    return False
