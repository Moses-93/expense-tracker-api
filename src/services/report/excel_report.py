from io import BytesIO
from typing import List
from openpyxl import Workbook
from openpyxl.styles import Font
from src.db.models import Expense
from .interfaces import ReportBase


class ExcelReport(ReportBase):

    def generate_report(self, expenses: List[Expense]) -> BytesIO:
        """
        Generate an Excel report from a list of expenses.
        """
        wb = Workbook()
        ws = wb.active
        ws.title = "Витрати"

        headers = ["ID", "Назва", "Дата", "Сума(UAH)", "Сума(USD)"]
        ws.append(headers)

        header_font = Font(bold=True)
        for cell in ws[1]:  
            cell.font = header_font

        for exp in expenses:
            ws.append([exp.id, exp.name, exp.date, exp.uah_amount, exp.usd_amount])

        total_sum_uah = sum(exp.uah_amount for exp in expenses)
        total_sum_usd = sum(exp.usd_amount for exp in expenses)

        ws.append(["Загальна сума у гривнях", total_sum_uah])
        ws.append(["Загальна сума у доларах", total_sum_usd])

        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[col_letter].width = max_length + 2

        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output
