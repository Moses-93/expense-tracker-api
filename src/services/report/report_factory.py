from src.services.report.interfaces import ReportBase
from src.services.report.excel_report import ExcelReport


class ReportFactory:
    _instances = {}

    @classmethod
    def get_report_generator(cls, format_report: str) -> ReportBase:
        """
        Returns a report generator instance based on the format.
        Uses caching to avoid unnecessary instantiations.
        """
        if format_report not in cls._instances:
            if format_report == "excel":
                cls._instances[format_report] = ExcelReport()
            else:
                raise ValueError("Unsupported report format")

        return cls._instances[format_report]
