from __future__ import annotations

from datetime import date as date_type
from datetime import datetime, time as time_type, timezone
from pathlib import Path
from typing import Optional, TypeVar

from PySide6.QtCore import QFile, QDate, QTime
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QDateEdit,
    QTimeEdit,
)

from List7.log_data import LogRecord, LogStore, record_display_text
from List7.main_window import Ui_MainWindow



class LogBrowserController:
    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self.store = LogStore()
        self.current_index: Optional[int] = None

        self.file_path_line = self._require(QLineEdit, "filePathLine")
        self.open_button = self._require(QPushButton, "openButton")
        self.apply_button = self._require(QPushButton, "applyButton")
        self.clear_button = self._require(QPushButton, "clearButton")
        self.prev_button = self._require(QPushButton, "prevButton")
        self.next_button = self._require(QPushButton, "nextButton")

        self.log_list = self._require(QListWidget, "logList")

        self.from_date_edit = self._require(QDateEdit, "fromDateEdit")
        self.from_time_edit = self._require(QTimeEdit, "fromTimeEdit")
        self.to_date_edit = self._require(QDateEdit, "toDateEdit")
        self.to_time_edit = self._require(QTimeEdit, "toTimeEdit")

        self.detail_fields = {
            "remote_host": self._require(QLineEdit, "remoteHostEdit"),
            "host": self._require(QLineEdit, "hostEdit"),
            "date": self._require(QLineEdit, "dateEdit"),
            "time": self._require(QLineEdit, "timeEdit"),
            "timezone": self._require(QLineEdit, "timezoneEdit"),
            "method": self._require(QLineEdit, "methodEdit"),
            "status_code": self._require(QLineEdit, "statusCodeEdit"),
            "status_text": self._require(QLineEdit, "statusTextEdit"),
            "resource": self._require(QLineEdit, "resourceEdit"),
            "orig_port": self._require(QLineEdit, "origPortEdit"),
            "resp_host": self._require(QLineEdit, "respHostEdit"),
            "resp_port": self._require(QLineEdit, "respPortEdit"),
        }

        self._connect_signals()
        self._update_nav_buttons()

    def _require[T](self, widget_type: type[T], name: str) -> T:
        widget = self.window.findChild(widget_type, name)
        if widget is None:
            raise RuntimeError(f"Blad: Brak widgetu '{name}' w pliku UI")
        return widget

    def _connect_signals(self) -> None:
        self.open_button.clicked.connect(self._on_open)
        self.apply_button.clicked.connect(self._on_apply_filter)
        self.clear_button.clicked.connect(self._on_clear_filter)
        self.prev_button.clicked.connect(self._on_prev)
        self.next_button.clicked.connect(self._on_next)
        self.log_list.currentRowChanged.connect(self._on_row_changed)

    def _on_open(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self.window, "Open log file")
        print(file_path)
        if not file_path:
            return

        try:
            self.store.load(Path(file_path))
        except OSError as exc:
            QMessageBox.critical(self.window, "Error", f"Failed to read file: {exc}")
            return

        self.file_path_line.setText(file_path)
        self._seed_filter_range()
        self._refresh_list()

    def _seed_filter_range(self) -> None:
        if not self.store.records:
            return

        timestamps = [record.entry.ts for record in self.store.records]
        start_ts = min(timestamps)
        end_ts = max(timestamps)

        self.from_date_edit.setDate(self._to_qdate(start_ts.date()))
        self.from_time_edit.setTime(self._to_qtime(start_ts.time()))
        self.to_date_edit.setDate(self._to_qdate(end_ts.date()))
        self.to_time_edit.setTime(self._to_qtime(end_ts.time()))

    def _on_apply_filter(self) -> None:
        if not self.store.records:
            return

        start_dt = self._combine_datetime(self.from_date_edit.date(), self.from_time_edit.time())
        end_dt = self._combine_datetime(self.to_date_edit.date(), self.to_time_edit.time())

        if start_dt and end_dt and start_dt > end_dt:
            QMessageBox.warning(self.window, "Error", "Start must be before end.")
            return

        self.store.apply_filter(start_dt, end_dt)
        self._refresh_list()

    def _on_clear_filter(self) -> None:
        if not self.store.records:
            return

        self.store.apply_filter(None, None)
        self._seed_filter_range()
        self._refresh_list()

    def _refresh_list(self) -> None:
        self.log_list.clear()
        for record in self.store.filtered:
            item = QListWidgetItem(record_display_text(record))
            self.log_list.addItem(item)

        if self.store.filtered:
            self.log_list.setCurrentRow(0)
        else:
            self.current_index = None
            self._clear_details()
            self._update_nav_buttons()

    def _on_row_changed(self, row: int) -> None:
        if row < 0 or row >= len(self.store.filtered):
            return

        self.current_index = row
        self._update_details(self.store.filtered[row])
        self._update_nav_buttons()

    def _update_details(self, record: LogRecord) -> None:
        entry = record.entry
        ts = entry.ts
        tz_name = ts.tzname() or "UTC"

        self.detail_fields["remote_host"].setText(entry.id_orig_h)
        self.detail_fields["host"].setText(entry.host)
        self.detail_fields["date"].setText(ts.strftime("%Y-%m-%d"))
        self.detail_fields["time"].setText(ts.strftime("%H:%M:%S"))
        self.detail_fields["timezone"].setText(tz_name)
        self.detail_fields["method"].setText(entry.method)
        self.detail_fields["status_code"].setText("" if entry.status_code is None else str(entry.status_code))
        self.detail_fields["status_text"].setText(entry.status_text or "")
        self.detail_fields["resource"].setText(entry.uri)
        self.detail_fields["orig_port"].setText(str(entry.id_orig_p))
        self.detail_fields["resp_host"].setText(entry.id_resp_h)
        self.detail_fields["resp_port"].setText(str(entry.id_resp_p))

    def _clear_details(self) -> None:
        for field in self.detail_fields.values():
            field.setText("")

    def _update_nav_buttons(self) -> None:
        if self.current_index is None or not self.store.filtered:
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return

        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.store.filtered) - 1)

    def _on_prev(self) -> None:
        if self.current_index is None:
            return
        next_index = self.current_index - 1
        if next_index >= 0:
            self.log_list.setCurrentRow(next_index)

    def _on_next(self) -> None:
        if self.current_index is None:
            return
        next_index = self.current_index + 1
        if next_index < len(self.store.filtered):
            self.log_list.setCurrentRow(next_index)

    def _combine_datetime(self, date_value: QDate, time_value: QTime) -> Optional[datetime]:
        if not date_value.isValid() or not time_value.isValid():
            return None

        py_date = self._qdate_to_py(date_value)
        py_time = self._qtime_to_py(time_value)
        return datetime.combine(py_date, py_time).replace(tzinfo=timezone.utc)

    def _qdate_to_py(self, date_value: QDate) -> date_type:
        try:
            return date_value.toPython()
        except AttributeError:
            return date_type(date_value.year(), date_value.month(), date_value.day())

    def _qtime_to_py(self, time_value: QTime) -> time_type:
        try:
            return time_value.toPython()
        except AttributeError:
            return time_type(time_value.hour(), time_value.minute(), time_value.second())

    def _to_qdate(self, value: date_type) -> QDate:
        return QDate(value.year, value.month, value.day)

    def _to_qtime(self, value: time_type) -> QTime:
        return QTime(value.hour, value.minute, value.second)


# def load_ui(ui_path: Path) -> QMainWindow:
#     loader = QUiLoader()
#     ui_file = QFile(str(ui_path))
#     if not ui_file.open(QFile.ReadOnly):
#         raise RuntimeError(f"Blad: Nie można otworzyć pliku UI: {ui_path}")
#
#     window = loader.load(ui_file, None)
#     ui_file.close()
#
#     if not isinstance(window, QMainWindow):
#         raise RuntimeError("Blad: Nie udało się wczytać pliku UI")
#
#     return window


# def run_app(ui_path: Path) -> int:
#     app = QApplication()
#     window = load_ui(ui_path)
#     window._controller = LogBrowserController(window)
#     window.show()
#     return app.exec()


def run_app() -> int:
    app = QApplication()
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    
    window._controller = LogBrowserController(window)
    window.show()
    return app.exec()
