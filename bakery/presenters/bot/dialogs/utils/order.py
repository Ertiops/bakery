from datetime import date


def combine_order_number(delivered_at: date, delivered_at_id: int) -> str:
    return f"{delivered_at:%Y-%m-%d}-{delivered_at_id}"
