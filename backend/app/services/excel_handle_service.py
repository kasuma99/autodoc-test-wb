from typing import BinaryIO
from uuid import UUID

import pandas as pd

from app.db.models.excel_handle_logs import ExcelHandleLog
from app.exceptions.content_type_exception import FileReadException
from app.repositories.excel_handle_logs_repo import ExcelHandleLogRepo


class ExcelHandleService:
    EXCEL_CONTENT_TYPES = (
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    def __init__(self, repo: ExcelHandleLogRepo):
        self._repo = repo

    def get_log(self, uuid: UUID | str) -> ExcelHandleLog:
        pass

    def get_logs(self) -> list[ExcelHandleLog]:
        pass

    def create_log(
        self,
        uuid: UUID | str,
        filename: str,
        status: str,
        log: str,
        error_type: str,
    ) -> ExcelHandleLog:
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
