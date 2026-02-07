from collections.abc import Mapping, Sequence
from io import BytesIO
from pathlib import Path
from typing import Any, cast
from uuid import UUID

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from bakery.domains.entities.order import Order, OrderProduct
from bakery.domains.entities.user import User
from bakery.domains.interfaces.adapters.order_report_pdf import IOrderReportPdfAdapter
from bakery.presenters.bot.dialogs.utils.order import combine_order_number


class OrderReportPdfAdapter(IOrderReportPdfAdapter):
    def __init__(self) -> None:
        self._font_name = self._register_font()

    def build_order_report(self, *, title: str, orders: Sequence[Order]) -> bytes:
        products, free_products = self._build_order_pdf_data(orders)
        return self.build_order_pdf(
            title=title, products=products, free_products=free_products
        )

    def build_order_pdf(
        self, *, title: str, products: list[dict], free_products: list[dict]
    ) -> bytes:
        buf = BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=24,
            rightMargin=24,
            topMargin=24,
            bottomMargin=24,
        )
        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="TitleRu",
                parent=styles["Heading2"],
                fontName=self._font_name,
            )
        )
        styles.add(
            ParagraphStyle(
                name="BodyRu",
                parent=styles["BodyText"],
                fontName=self._font_name,
            )
        )

        elements: list[Any] = [Paragraph(title, styles["TitleRu"]), Spacer(1, 12)]

        data = [["Товар", "Кол-во"]]
        for item in products:
            data.append([item["name"], str(item["quantity"])])

        table = Table(data, colWidths=[360, 120])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, -1), self._font_name),
                    ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ]
            )
        )
        elements.append(table)

        if free_products:
            elements.append(Spacer(1, 12))
            elements.append(Paragraph("Свободные товары", styles["BodyRu"]))
            elements.append(Spacer(1, 6))
            free_data = [["Товар", "Кол-во"]]
            for item in free_products:
                free_data.append([item["name"], str(item["quantity"])])
            free_table = Table(free_data, colWidths=[360, 120])
            free_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        ("FONTNAME", (0, 0), (-1, -1), self._font_name),
                        ("ALIGN", (1, 1), (1, -1), "CENTER"),
                    ]
                )
            )
            elements.append(free_table)

        doc.build(elements)
        return buf.getvalue()

    def build_delivery_report(
        self,
        *,
        title: str,
        orders: Sequence[Order],
        users_by_id: Mapping[UUID, User],
    ) -> bytes:
        pickup_groups: dict[str, list[dict]] = {}
        individual_orders: list[dict] = []

        for order in orders:
            user = users_by_id.get(order.user_id)
            if not user:
                continue
            order_info = dict(
                number=combine_order_number(order.delivered_at, order.delivered_at_id),
                name=user.name,
                phone=user.phone,
                address=order.pickup_address_name,
                products=self._format_order_products_text(order.products),
            )
            if order.pickup_address_id:
                key = order.pickup_address_name or "Пункт выдачи"
                pickup_groups.setdefault(key, []).append(order_info)
            else:
                individual_orders.append(order_info)

        groups = []
        for name, items in pickup_groups.items():
            groups.append(dict(title=f"Точка развоза: {name}", orders=items))
        if individual_orders:
            groups.append(dict(title="Индивидуальный развоз", orders=individual_orders))

        return self.build_delivery_pdf(title=title, groups=groups)

    def build_delivery_pdf(self, *, title: str, groups: list[dict]) -> bytes:
        buf = BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=24,
            rightMargin=24,
            topMargin=24,
            bottomMargin=24,
        )
        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="TitleRu",
                parent=styles["Heading2"],
                fontName=self._font_name,
            )
        )
        styles.add(
            ParagraphStyle(
                name="BodyRu",
                parent=styles["BodyText"],
                fontName=self._font_name,
            )
        )

        cell_style = ParagraphStyle(
            name="TableCellRu",
            parent=styles["BodyRu"],
            fontName=self._font_name,
            fontSize=9,
            leading=11,
            wordWrap="CJK",
        )

        elements: list[Any] = [Paragraph(title, styles["TitleRu"]), Spacer(1, 12)]

        for group in groups:
            elements.append(Paragraph(group["title"], styles["BodyRu"]))
            elements.append(Spacer(1, 6))
            data = [["Заказ", "Клиент", "Телефон", "Адрес", "Состав"]]
            for order in group["orders"]:
                data.append(
                    [
                        order["number"],
                        order["name"],
                        order["phone"],
                        order["address"],
                        order["products"],
                    ]
                )
            data_wrapped = [
                [
                    Paragraph(str(value).replace("\n", "<br/>"), cell_style)
                    for value in row
                ]
                for row in data
            ]
            col_widths = self._calc_delivery_col_widths(
                data=data,
                available_width=A4[0] - 48,
            )
            table = Table(data_wrapped, colWidths=col_widths)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        ("FONTNAME", (0, 0), (-1, -1), self._font_name),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]
                )
            )
            elements.append(table)
            elements.append(Spacer(1, 12))

        doc.build(elements)
        return buf.getvalue()

    def _build_order_pdf_data(
        self, orders: Sequence[Order]
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        aggregated: dict[str, dict[str, Any]] = {}
        for order in orders:
            for item in order.products:
                if item.get("is_deleted", False):
                    continue
                key = item["id"]
                if key not in aggregated:
                    aggregated[key] = dict(name=item["name"], quantity=0)
                aggregated[key]["quantity"] += item["quantity"]

        products: list[dict[str, Any]] = []
        free_products: list[dict[str, Any]] = []
        for agg_item in aggregated.values():
            qty = agg_item["quantity"]
            if qty % 2 != 0:
                products.append(dict(name=agg_item["name"], quantity=qty + 1))
                free_products.append(dict(name=agg_item["name"], quantity=1))
            else:
                products.append(dict(name=agg_item["name"], quantity=qty))
        products.sort(key=lambda p: cast(str, p["name"]))
        free_products.sort(key=lambda p: cast(str, p["name"]))
        return products, free_products

    def _format_order_products_text(self, products: Sequence[OrderProduct]) -> str:
        return "\n".join(
            f"{item['name']} ×{item['quantity']}"
            for item in products
            if not item.get("is_deleted", False)
        )

    def _calc_delivery_col_widths(
        self, *, data: list[list[str]], available_width: float
    ) -> list[float]:
        min_widths: list[float] = [75, 110, 90, 140, 135]
        if not data:
            return min_widths

        max_lens = [0, 0, 0, 0, 0]
        for row in data:
            for idx, value in enumerate(row[:5]):
                text = str(value or "")
                max_lens[idx] = max(
                    max_lens[idx], max(len(line) for line in text.splitlines() or [""])
                )

        total_min = sum(min_widths)
        extra = max(0.0, available_width - total_min)
        total_len = sum(max_lens) or 1
        return [
            min_widths[idx] + extra * (max_lens[idx] / total_len) for idx in range(5)
        ]

    def _register_font(self) -> str:
        font_name = "DejaVuSans"
        if font_name in pdfmetrics.getRegisteredFontNames():
            return font_name

        font_paths = [
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/System/Library/Fonts/Supplemental/DejaVuSans.ttf"),
            Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
            Path("/Library/Fonts/DejaVuSans.ttf"),
        ]
        for path in font_paths:
            if path.exists():
                pdfmetrics.registerFont(TTFont(font_name, str(path)))
                return font_name
        return "Helvetica"
