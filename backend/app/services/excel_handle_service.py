import os
import traceback
from datetime import datetime
from typing import BinaryIO, Any
from uuid import UUID

import pandas as pd

from app.config import get_config
from app.db.models.excel_handle_logs import ExcelHandleLog
from app.enum.excel_handle_errors import ExcelHandleError
from app.enum.excel_handle_status import ExcelHandleStatus
from app.repositories.excel_handle_logs_repo import ExcelHandleLogRepo


class ExcelHandleService:
    EXCEL_CONTENT_TYPES = [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]
    EXPECTED_COLUMNS = [
        "Date",
        "Sales",
    ]

    def __init__(self, repo: ExcelHandleLogRepo):
        self._repo = repo
        self._config = get_config()

    def get_log(self, uuid: UUID | str) -> ExcelHandleLog | None:
        if isinstance(uuid, str):
            uuid = UUID(uuid)
        return self._repo.get(uuid=uuid)

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
        if isinstance(uuid, str):
            uuid = UUID(uuid)
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
        if isinstance(uuid, str):
            uuid = UUID(uuid)
        excel_handle_log = self.get_log(uuid=uuid)
        self._repo.delete(model=excel_handle_log)

    def validate_excel_file_and_get_dataframe(
        self,
        task_id: str,
        filename: str,
        content_type: str,
        file: BinaryIO,
    ) -> pd.DataFrame | None:
        # Catch error when uploaded file is not an Excel file and create log
        if content_type not in self.EXCEL_CONTENT_TYPES:
            self.create_log(
                uuid=task_id,
                filename=filename,
                status=ExcelHandleStatus.FAILED.value,
                log="The Excel file is empty",
                error_type=ExcelHandleError.UNSUPPORTED_TYPE.value,
            )
            return None
        try:
            dataframe = pd.read_excel(file)
            if dataframe.empty:
                # Catch error when empty Excel file has been uploaded and create log
                self.create_log(
                    uuid=task_id,
                    filename=filename,
                    status=ExcelHandleStatus.FAILED.value,
                    log="The Excel file is empty",
                    error_type=ExcelHandleError.EMPTY.value,
                )
                return None

        except Exception as e:
            # Catch other pandas-related errors (e.g., invalid file format)
            self.create_log(
                uuid=task_id,
                filename=filename,
                status=ExcelHandleStatus.FAILED.value,
                log=traceback.format_exc(),
                error_type=ExcelHandleError.PANDAS_RELATED.value,
            )
            return None

        return dataframe

    def is_valid_dataframe_columns(
        self,
        dataframe: pd.DataFrame,
        task_id: str,
        filename: str,
    ) -> bool:
        # Catch error when columns are not match with 'EXPECTED COLUMNS'
        if len(dataframe.columns) != len(self.EXPECTED_COLUMNS) or not all(
            dataframe.columns == self.EXPECTED_COLUMNS
        ):
            self.create_log(
                uuid=task_id,
                filename=filename,
                status=ExcelHandleStatus.FAILED.value,
                log=f"File's columns do not match with: {self.EXPECTED_COLUMNS}",
                error_type=ExcelHandleError.INVALID_COLUMNS.value,
            )
            return False

        return True

    def is_valid_date(
        self,
        date: Any,
        index: int,
        task_id: str,
        filename: str,
    ):
        try:
            # Catch error when data in Date column is not a valid type
            pd.to_datetime(date, format="%Y-%m-%d")
            return True
        except ValueError:
            self.create_log(
                uuid=task_id,
                filename=filename,
                status=ExcelHandleStatus.FAILED.value,
                log=f"Invalid date format in row: {index + 1}",
                error_type=ExcelHandleError.INVALID_DATA.value,
            )
            return False

    def is_valid_sales(
        self,
        sales: Any,
        index: int,
        task_id: str,
        filename: str,
    ):
        # Check if data in Date column is either None or float, int
        if pd.isna(sales) or isinstance(sales, (int, float)):
            return True

        self.create_log(
            uuid=task_id,
            filename=filename,
            status=ExcelHandleStatus.FAILED.value,
            log=f"Invalid sales format in row: {index + 1}",
            error_type=ExcelHandleError.INVALID_DATA.value,
        )
        return False

    def process_file(
        self,
        task_id: str,
        filename: str,
        content_type: str,
        file: BinaryIO,
    ) -> None:
        # Get dataframe and pass all validation functions
        dataframe = self.validate_excel_file_and_get_dataframe(
            task_id=task_id,
            filename=filename,
            content_type=content_type,
            file=file,
        )
        if not dataframe:
            return

        if not self.is_valid_dataframe_columns(
            dataframe=dataframe,
            task_id=task_id,
            filename=filename,
        ):
            return

        for index, row in dataframe.iterrows():
            if not self.is_valid_date(
                date=row[self.EXPECTED_COLUMNS[0]],
                index=int(index),
                task_id=task_id,
                filename=filename,
            ):
                return
            if not self.is_valid_sales(
                sales=row[self.EXPECTED_COLUMNS[1]],
                index=int(index),
                task_id=task_id,
                filename=filename,
            ):
                return

        try:
            # Convert the 'Date' column to a datetime format
            dataframe["Date"] = pd.to_datetime(dataframe["Date"])

            # Set the 'Date' column as the index of the dataframe
            dataframe.set_index("Date", inplace=True)

            # Interpolating missing values
            # Linear interpolation is used here, assuming that the values change uniformly between the known data points
            dataframe["Sales"] = dataframe["Sales"].interpolate(method="linear")

            processed_file_path = f"processed_{task_id}.xlsx"
            processed_files_folder = self._config.excel.folder_path

            # Save the updated data back to an Excel file
            dataframe.to_excel(
                os.path.join(processed_files_folder, processed_file_path), index=False
            )
            # Create log for success processing
            self.create_log(
                uuid=task_id,
                filename=filename,
                status=ExcelHandleStatus.SUCCESS.value,
                log="",
                error_type=ExcelHandleError.NONE.value,
            )

        except Exception as e:
            self.create_log(
                uuid=task_id,
                filename=filename,
                status=ExcelHandleStatus.FAILED.value,
                log=traceback.format_exc(),
                error_type=ExcelHandleError.OTHER.value,
            )
