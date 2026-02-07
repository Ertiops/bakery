from collections.abc import Sequence
from datetime import date

from bakery.domains.entities.order import OrderProduct


def combine_order_number(delivered_at: date, delivered_at_id: int) -> str:
    return f"{delivered_at:%Y-%m-%d}-{delivered_at_id}"


def format_order_products(products: Sequence[OrderProduct]) -> str:
    if not products:
        return "—"
    lines: list[str] = []
    for p in products:
        name = p.get("name") or "—"
        price = int(p.get("price") or 0)
        qty = int(p.get("quantity") or 0)
        text = f"• {name} — {qty} × {price}₽"
        if p.get("is_deleted", False):
            text = f"• <s>{name} — {qty} × {price}₽</s>"
        lines.append(text)
    return "\n".join(lines)
