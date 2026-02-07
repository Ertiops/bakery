from dishka import Provider, Scope, provide

from bakery.adapters.pdf.order_report import OrderReportPdfAdapter
from bakery.domains.interfaces.adapters.order_report_pdf import IOrderReportPdfAdapter


class PdfProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def order_report_pdf_adapter(self) -> IOrderReportPdfAdapter:
        return OrderReportPdfAdapter()
