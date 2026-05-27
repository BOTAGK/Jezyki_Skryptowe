from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from threading import Event, Thread
from typing import Optional

from PySide6.QtCore import (
    QAbstractListModel,
    QFile,
    QDate,
    QDateTime,
    QModelIndex,
    QObject,
    Qt,
    QTime,
    Signal,
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QDateTimeEdit,
    QFileDialog,
    QLineEdit,
    QListView,
    QMainWindow,
    QMessageBox,
    QPushButton,
)

from List7.log_data import LogRecord, LogStore, record_display_text
from List7.main_window import Ui_MainWindow


class LogBrowserController:
    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self.store = LogStore()
        self.log_model = LogListModel(self.store)
        self.current_index: Optional[int] = None
        self.is_loading = False
        self._stop_loading = Event()
        self._load_worker: Optional[Thread] = None

        self.worker_signals = WorkerSignal()
        self.worker_signals.finished.connect(self._on_load_finished)
        self.worker_signals.chunk_ready.connect(self._on_chunk_loaded)
        self.worker_signals.failed.connect(self._on_load_failed)

        self.file_path_line = self._require(QLineEdit, "filePathLine")
        self.open_button = self._require(QPushButton, "openButton")
        self.apply_button = self._require(QPushButton, "applyButton")
        self.clear_button = self._require(QPushButton, "clearButton")
        self.prev_button = self._require(QPushButton, "prevButton")
        self.next_button = self._require(QPushButton, "nextButton")

        self.log_list = self._require(QListView, "logList")
        self.log_list.setModel(self.log_model)
        self.log_list.setUniformItemSizes(True)

        self.from_datetime_edit = self._require(QDateTimeEdit, "fromDateTimeEdit")
        self.to_datetime_edit = self._require(QDateTimeEdit, "toDateTimeEdit")

        self.detail_fields = {
            "uid": self._require(QLineEdit, "uidEdit"),
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
        self.log_list.selectionModel().currentChanged.connect(self._on_current_changed)

    def _on_open(self) -> None:
        if self.is_loading:
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Open log file",
            self._initial_directory(),
            "Log files (*.log)",
        )
        if not file_path:
            return

        self.file_path_line.setText(file_path)
        self._start_loading(Path(file_path))

    def _start_loading(self, file_path: Path, chunk_size: int = 1000) -> None:
        self.current_index = None
        self._clear_details()
        self.log_model.clear()
        self._set_loading(True)
        self._stop_loading = Event()

        def worker() -> None:
            try:
                chunk: list[LogRecord] = []

                for record in stream_log_file(file_path):
                    if self._stop_loading.is_set():
                        break

                    chunk.append(record)
                    if len(chunk) >= chunk_size:
                        self.worker_signals.chunk_ready.emit(chunk)
                        chunk = []

                if chunk and not self._stop_loading.is_set():
                    self.worker_signals.chunk_ready.emit(chunk)
            except OSError as exc:
                self.worker_signals.failed.emit(str(exc))
            finally:
                self.worker_signals.finished.emit()

        self._load_worker = Thread(target=worker, daemon=True)
        self._load_worker.start()

    def _on_chunk_loaded(self, chunk: list[LogRecord]) -> None:
        should_select_first = self.current_index is None
        self.log_model.append_records(chunk)

        if should_select_first and self.log_model.rowCount() > 0:
            self._select_row(0)

        self._update_nav_buttons()

    def _on_load_finished(self) -> None:
        self._set_loading(False)
        self._load_worker = None

        self._seed_filter_range()
        if self.current_index is None and self.log_model.rowCount() > 0:
            self._select_row(0)
        self._update_nav_buttons()

    def _on_load_failed(self, message: str) -> None:
        QMessageBox.critical(self.window, "Error", f"Failed to read file: {message}")

    def _initial_directory(self) -> str:
        log_dir = Path(__file__).resolve().parents[1] / "List2" / "utils"
        return str(log_dir if log_dir.exists() else Path(__file__).resolve().parent)

    def _seed_filter_range(self) -> None:
        if not self.store.records:
            return

        timestamps = [record.entry.ts for record in self.store.records]
        start_ts = min(timestamps)
        end_ts = max(timestamps)

        self.from_datetime_edit.setDateTime(self._to_qdatetime(start_ts))
        self.to_datetime_edit.setDateTime(self._to_qdatetime(end_ts))

    def _on_apply_filter(self) -> None:
        if self.is_loading or not self.store.records:
            return

        start_dt = self._qdatetime_to_py(self.from_datetime_edit.dateTime())
        end_dt = self._qdatetime_to_py(self.to_datetime_edit.dateTime())

        if start_dt and end_dt and start_dt > end_dt:
            QMessageBox.warning(self.window, "Error", "Start must be before end.")
            return

        self.log_model.apply_filter(start_dt, end_dt)
        self._select_first_or_clear()

    def _on_clear_filter(self) -> None:
        if self.is_loading or not self.store.records:
            return

        self.log_model.apply_filter(None, None)
        self._seed_filter_range()
        self._select_first_or_clear()

    def _on_current_changed(self, current: QModelIndex, previous: QModelIndex) -> None:
        row = current.row()
        if not current.isValid() or row < 0 or row >= self.log_model.rowCount():
            self.current_index = None
            self._clear_details()
            self._update_nav_buttons()
            return

        self.current_index = row
        self._update_details(self.store.record_at(row))
        self._update_nav_buttons()

    def _update_details(self, record: LogRecord) -> None:
        entry = record.entry
        ts = entry.ts
        tz_name = ts.tzname() or "UTC"

        self.detail_fields["uid"].setText(entry.uid)
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

    def _select_first_or_clear(self) -> None:
        if self.log_model.rowCount() > 0:
            self._select_row(0)
            return

        self.current_index = None
        self._clear_details()
        self._update_nav_buttons()

    def _select_row(self, row: int) -> None:
        index = self.log_model.index(row, 0)
        if not index.isValid():
            return

        self.log_list.setCurrentIndex(index)
        self.log_list.scrollTo(index)

    def _set_loading(self, is_loading: bool) -> None:
        self.is_loading = is_loading
        self.open_button.setEnabled(not is_loading)
        self.apply_button.setEnabled(not is_loading)
        self.clear_button.setEnabled(not is_loading)

    def _update_nav_buttons(self) -> None:
        row_count = self.log_model.rowCount()
        if self.current_index is None or row_count == 0:
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return

        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < row_count - 1)

    def _on_prev(self) -> None:
        if self.current_index is None:
            return
        next_index = self.current_index - 1
        if next_index >= 0:
            self._select_row(next_index)

    def _on_next(self) -> None:
        if self.current_index is None:
            return
        next_index = self.current_index + 1
        if next_index < self.log_model.rowCount():
            self._select_row(next_index)

    def _qdatetime_to_py(self, value: QDateTime) -> Optional[datetime]:
        if not value.isValid():
            return None

        try:
            py_datetime = value.toPython()
        except AttributeError:
            py_datetime = datetime(
                value.date().year(),
                value.date().month(),
                value.date().day(),
                value.time().hour(),
                value.time().minute(),
                value.time().second(),
            )

        return py_datetime.replace(tzinfo=timezone.utc)

    def _to_qdatetime(self, value: datetime) -> QDateTime:
        return QDateTime(
            QDate(value.year, value.month, value.day),
            QTime(value.hour, value.minute, value.second),
        )


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

def run_app(ui_path: Path) -> int:
    app = QApplication()
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    window._controller = LogBrowserController(window)
    window.show()
    return app.exec()

