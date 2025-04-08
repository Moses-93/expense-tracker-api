import logging
from io import BytesIO
from typing import List
from openpyxl import Workbook
from openpyxl.styles import Font
from src.db.models import Expense
from .interfaces import ReportBase


logger = logging.getLogger(__name__)


class ExcelReport(ReportBase):
    """
    Generates an Excel report from a list of expenses.

    The report includes a table with detailed information for each expense:
    ID, name, date, amount in UAH and USD. At the end, it adds total sums for both currencies.
    """

    def generate_report(self, expenses: List[Expense]) -> BytesIO:
        """
        Create an Excel report from the given list of expenses.

        :param expenses: List of Expense objects
        :return: Excel file as a BytesIO stream
        """

        wb = Workbook()
        ws = wb.active
        ws.title = "Expenses"

        self._write_header(ws)
        self._write_expenses(ws, expenses)
        self._write_totals(ws, expenses)
        self._auto_adjust_column_widths(ws)

        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output

    def _write_header(self, ws):
        """
        Adds a header row to the worksheet and applies bold styling.
        """
        headers = ["ID", "Назва", "Дата", "Сума(UAH)", "Сума(USD)"]
        ws.append(headers)
        header_font = Font(bold=True)
        for cell in ws[1]:
            cell.font = header_font

    def _write_expenses(self, ws, expenses: List[Expense]):
        """
        Writes the list of expenses into the worksheet.
        """
        for exp in expenses:
            ws.append([exp.id, exp.name, exp.date, exp.uah_amount, exp.usd_amount])

    def _write_totals(self, ws, expenses: List[Expense]):
        """
        Appends total sums in UAH and USD at the end of the worksheet.
        """
        total_sum_uah = sum(exp.uah_amount for exp in expenses)
        total_sum_usd = sum(exp.usd_amount for exp in expenses)

        ws.append([])
        ws.append(["Сума UAH", total_sum_uah])
        ws.append(["Сума USD", total_sum_usd])

    def _auto_adjust_column_widths(self, ws):
        """
        Automatically adjusts column widths based on the maximum content length.
        """
        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[col_letter].width = max_length + 2
