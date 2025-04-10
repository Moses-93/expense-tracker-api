from src.services.report.interfaces import ReportBase
from src.services.report.excel_report import ExcelReport


class ReportFactory:
    """
    A factory class for creating report generator instances based on the specified format.
    """

    def get_report_generator(self, format_report: str) -> ReportBase:
        """Creates and returns a report generator instance based on the provided format.

        Args:
            format_report (str): format_report (str): The format of the report (e.g., "excel").

        Raises:
            ValueError: ValueError: If the provided format is not supported.

        Returns:
            ReportBase: ReportBase: An instance of a report generator.
        """
        if format_report == "excel":
            return ExcelReport()
        else:
            raise ValueError(f"Unsupported report format: {format_report}")
