import os
import traceback
from datetime import datetime
from typing import BinaryIO, Any
from uuid import UUID

import pandas as pd  # type: ignore

from app.config import get_config
from app.db.models.excel_handle_logs import ExcelHandleLog
from app.enum.excel_handle_errors import ExcelHandleError
from app.enum.excel_handle_status import ExcelHandleStatus
from app.exceptions.not_found_exception import NotFoundException
from app.repositories.excel_handle_logs_repo import ExcelHandleLogRepo
from app.utils.excel_handle_log_dataclass import LogMinor
from app.utils.validate_uuid_format import validate_uuid_format


class ExcelHandleService:
    def __init__(self, repo: ExcelHandleLogRepo):
        self._repo = repo
        self._config = get_config().excel
        self._status = ExcelHandleStatus
        self._error = ExcelHandleError

    def get_log(self, uuid: UUID | str) -> ExcelHandleLog:
        uuid = validate_uuid_format(string=uuid)

        excel_handle_log = self._repo.get(uuid=uuid)
        if excel_handle_log is None:
            raise NotFoundException(
                message=f"ExcelHandleLog record with uuid={uuid} not found"
            )
        return excel_handle_log

    def get_logs(self) -> list[ExcelHandleLog]:
        return self._repo.get_all()

    def create_log(
        self,
        uuid: UUID | str,
        filename: str,
        status: str,
        log: str,
        error_type: str,
    ) -> ExcelHandleLog:
        uuid = validate_uuid_format(string=uuid)
        excel_handle_log = self._repo.create(
            model=ExcelHandleLog(
                uuid=uuid,
                created_date=datetime.utcnow(),
                filename=filename,
                status=status,
                log=log,
                error_type=error_type,
            )
        )
        return excel_handle_log

    def delete_log(self, uuid: UUID | str) -> None:
        uuid = validate_uuid_format(string=uuid)
        excel_handle_log = self._repo.get(uuid=uuid)
        self._repo.delete(model=excel_handle_log)

    # Validation methods:

    def get_log_invalid_content_type(self, content_type: str) -> LogMinor | None:
        # Catch error when uploaded file is not an Excel file
        if content_type not in [self._config.mime_xls, self._config.mime_xlsx]:
            log = LogMinor(
                status=self._status.FAILED.value,
                log=f"Unsupported file extension: {content_type}",
                error_type=self._error.UNSUPPORTED_TYPE.value,
            )
            return log
        return None

    def get_log_unreadable(self, file: BinaryIO) -> LogMinor | None:
        try:
            dataframe = pd.read_excel(file)
            # Catch error when uploaded file is not an Excel file
            if dataframe.empty:
                log = LogMinor(
                    status=self._status.FAILED.value,
                    log="The Excel file is empty",
                    error_type=self._error.UNSUPPORTED_TYPE.value,
                )
                return log

        # Catch other pandas-related errors
        except Exception:
            log = LogMinor(
                status=ExcelHandleStatus.FAILED.value,
                log=traceback.format_exc(),
                error_type=ExcelHandleError.PANDAS_RELATED.value,
            )
            return log

        return None

    def get_log_invalid_columns(self, columns: list) -> LogMinor | None:
        # Catch error when columns are not match with EXPECTED COLUMNS
        if not columns == [self._config.column_date, self._config.column_sales]:
            log = LogMinor(
                status=ExcelHandleStatus.FAILED.value,
                log=f"File's columns do not match with: {self._config.column_date}, {self._config.column_sales}",
                error_type=ExcelHandleError.INVALID_COLUMNS.value,
            )
            return log
        return None

    def get_log_invalid_date(self, date: Any, index: int) -> LogMinor | None:
        try:
            # Catch error when data in Date column is not a valid type
            pd.to_datetime(date, format="%Y-%m-%d")

        except ValueError:
            log = LogMinor(
                status=self._status.FAILED.value,
                log=f"Invalid date format in row: {index + 1}: {date}",
                error_type=self._error.INVALID_DATA.value,
            )
            return log

        return None

    def get_log_invalid_sales(self, sales: Any, index: int) -> LogMinor | None:
        # Check if data in Date column is either None or float | int
        if not pd.isna(sales) and not isinstance(sales, (int, float)):
            log = LogMinor(
                status=self._status.FAILED.value,
                log=f"Invalid sales format in row: {index + 1}",
                error_type=self._error.INVALID_DATA.value,
            )
            return log
        return None

    def validate_and_get_log(
        self, content_type: str, file: BinaryIO
    ) -> LogMinor | None:
        # Pass all validation functions
        log = self.get_log_invalid_content_type(content_type=content_type)
        if log:
            return log

        log = self.get_log_unreadable(file=file)
        if log:
            return log

        dataframe = pd.read_excel(file)
        log = self.get_log_invalid_columns(columns=list(dataframe.columns))
        if log:
            return log

        for index, row in dataframe.iterrows():
            log = self.get_log_invalid_date(
                date=row[self._config.column_date], index=int(index)
            )
            if log:
                return log

            log = self.get_log_invalid_sales(
                sales=row[self._config.column_sales], index=int(index)
            )
            if log:
                return log

        return None

    def process_file(
        self,
        task_id: str,
        filename: str,
        content_type: str,
        file: BinaryIO,
    ) -> None:
        # validate Excel file by all validators
        log = self.validate_and_get_log(content_type=content_type, file=file)
        if log:
            self.create_log(
                uuid=task_id,
                filename=filename,
                status=log.status,
                log=log.log,
                error_type=log.error_type,
            )
            return

        try:
            dataframe = pd.read_excel(file)
            # Convert the 'Date' column to a datetime format
            dataframe["Date"] = pd.to_datetime(dataframe["Date"])

            # Set the 'Date' column as the index of the dataframe
            dataframe.set_index("Date", inplace=True)

            # Interpolating missing values
            # Linear interpolation is used here, assuming that the values change uniformly between the known data points
            dataframe["Sales"] = dataframe["Sales"].interpolate(method="linear")

            processed_file_path = f"{task_id}.xlsx"
            processed_files_folder = self._config.folder_path
            # Create the directory if it does not exist
            os.makedirs(processed_files_folder, exist_ok=True)
            # Save the updated data back to an Excel file
            dataframe.to_excel(
                os.path.join(processed_files_folder, processed_file_path)
            )
            # Create log for success processing Excel file
            self.create_log(
                uuid=task_id,
                filename=filename,
                status=ExcelHandleStatus.SUCCESS.value,
                log="",
                error_type=ExcelHandleError.NONE.value,
            )

        except Exception:
            self.create_log(
                uuid=task_id,
                filename=filename,
                status=ExcelHandleStatus.FAILED.value,
                log=traceback.format_exc(),
                error_type=ExcelHandleError.OTHER.value,
            )
