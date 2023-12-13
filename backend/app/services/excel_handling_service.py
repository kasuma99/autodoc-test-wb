from typing import BinaryIO
from uuid import UUID

import pandas as pd

from app.db.models.excel_handling_logs import ExcelHandlingLog
from app.exceptions.content_type_exception import FileReadException
from app.repositories.excel_handling_logs_repo import ExcelHandlingLogRepo


class ExcelHandlingService:
    EXCEL_CONTENT_TYPES = (
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    def __init__(self, repo: ExcelHandlingLogRepo):
        self._repo = repo

    def get_log(self, uuid: UUID | str) -> ExcelHandlingLog:
        pass

    def get_logs(self) -> list[ExcelHandlingLog]:
        pass

    def create_log(
        self,
        uuid: UUID | str,
        filename: str,
        status: str,
        log: str,
        error_type: str,
    ) -> ExcelHandlingLog:
        pass

    def delete_log(self, uuid: UUID | str) -> None:
        pass

    def validate_excel_file_and_get_dataframe(
        self,
        file: BinaryIO,
        content_type,
    ) -> pd.DataFrame:
        # Catch error when uploaded file is not an Excel file
        if content_type not in self.EXCEL_CONTENT_TYPES:
            raise FileReadException(
                message="Unsupported file type. Please upload an Excel file with '.xls' or '.xlsx' extension."
            )
        try:
            dataframe = pd.read_excel(file)
            if dataframe.empty:
                # Catch error when empty Excel file has been uploaded
                self.create_log()
                raise FileReadException(message="The Excel file is empty")

        except Exception:
            # Catch other pandas-related errors (e.g., invalid file format)

            raise FileReadException(
                message="An error occurred while reading the Excel file"
            )

    def process_file(self, file: BinaryIO, content_type: str):
        pass
