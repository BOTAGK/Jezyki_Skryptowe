from __future__ import annotations

import sys
from pathlib import Path

try:
    from PySide6.QtCore import Qt, QDate
    from PySide6.QtWidgets import (
        QApplication,
        QFileDialog,
        QGridLayout,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QListWidget,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QVBoxLayout,
        QWidget,
        QDateEdit,
    )
except ModuleNotFoundError as error:
    raise SystemExit("Brak PySide6. Zainstaluj pakiet poleceniem: pip install PySide6") from error

try:
    from .log_logic import LogService
except ImportError:
    from log_logic import LogService


class LogBrowserApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.service = LogService()
        self.full_log = []
        self.filtered_log = []

        self.setWindowTitle("Log browser")
        self.resize(900, 520)
        self.setup_ui()

    def setup_ui(self) -> None:
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        top_layout = QHBoxLayout()
        self.file_path_input = QLineEdit()
        self.file_path_input.setReadOnly(True)
        self.file_path_input.setPlaceholderText("Wybierz plik z logami...")

        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.load_file)

        top_layout.addWidget(self.file_path_input)
        top_layout.addWidget(self.open_button)
        main_layout.addLayout(top_layout)

        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        left_layout = QVBoxLayout()
        content_layout.addLayout(left_layout, stretch=1)
        left_layout.addLayout(self._build_dates_layout())

        self.log_list = QListWidget()
        self.log_list.currentRowChanged.connect(self.display_details)
        left_layout.addWidget(self.log_list)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.go_previous)
        left_layout.addWidget(self.prev_button, alignment=Qt.AlignmentFlag.AlignLeft)

        right_layout = QVBoxLayout()
        content_layout.addLayout(right_layout, stretch=1)
        self._build_details(right_layout)

        right_layout.addStretch()
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.go_next)
        right_layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignRight)

        self._set_styles()
        self.clear_details()

    def _build_dates_layout(self) -> QHBoxLayout:
        dates_layout = QHBoxLayout()
        dates_layout.addWidget(QLabel("From"))

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.dateChanged.connect(self.filter_logs)
        dates_layout.addWidget(self.date_from)

        dates_layout.addWidget(QLabel("To"))
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.dateChanged.connect(self.filter_logs)
        dates_layout.addWidget(self.date_to)

        return dates_layout

    def _build_details(self, parent_layout: QVBoxLayout) -> None:
        detail_grid = QGridLayout()
        parent_layout.addLayout(detail_grid)

        self.detail_host = self._add_line_detail(detail_grid, "Remote host:", 0)
        self.detail_date = self._add_line_detail(detail_grid, "Date:", 1)

        detail_grid.addWidget(QLabel("Time:"), 2, 0)
        self.detail_time = self._readonly_line()
        detail_grid.addWidget(self.detail_time, 2, 1)

        detail_grid.addWidget(QLabel("Timezone:"), 2, 2)
        self.detail_tz = self._readonly_line()
        detail_grid.addWidget(self.detail_tz, 2, 3)

        detail_grid.addWidget(QLabel("Status code:"), 3, 0)
        self.detail_status = QLabel("-")
        self.detail_status.setFixedSize(45, 45)
        self.detail_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        detail_grid.addWidget(self.detail_status, 3, 1)

        detail_grid.addWidget(QLabel("Method:"), 3, 2)
        self.detail_method = QLabel("-")
        detail_grid.addWidget(self.detail_method, 3, 3)

        self.detail_resource = self._add_line_detail(detail_grid, "Resource:", 4)
        self.detail_size = self._add_line_detail(detail_grid, "Size:", 5)

    def _add_line_detail(self, grid: QGridLayout, label: str, row: int) -> QLineEdit:
        grid.addWidget(QLabel(label), row, 0)
        line_edit = self._readonly_line()
        grid.addWidget(line_edit, row, 1, 1, 3)
        return line_edit

    def _readonly_line(self) -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setReadOnly(True)
        return line_edit

    def _set_styles(self) -> None:
        self.setStyleSheet(
            """
            QWidget {
                font-family: "Comic Sans MS";
                font-size: 13px;
                color: #111;
                background: #f7f7f7;
            }
            QLabel {
                color: #111;
                background: transparent;
            }
            QLineEdit, QDateEdit, QListWidget {
                border: 2px solid #111;
                background: white;
                color: #111;
                padding: 4px;
            }
            QLineEdit:read-only {
                background: white;
                color: #111;
            }
            QPushButton {
                background: #d0d0d0;
                border: 2px solid #111;
                color: #111;
                padding: 7px 22px;
                font-weight: bold;
            }
            QListWidget::item {
                color: #111;
                background: white;
            }
            QListWidget::item:selected {
                color: #111;
                background: #dce8ff;
            }
            QDateEdit::drop-down {
                background: #d0d0d0;
                border-left: 1px solid #111;
            }
            QPushButton:disabled {
                color: #aaa;
                background: #eee;
            }
            """
        )

    def load_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz plik logu",
            self._initial_directory(),
            "Log Files (*.log *.txt);;All Files (*)",
        )

        if file_path:
            self.open_log_file(file_path)

    def open_log_file(self, file_path: str | Path) -> None:
        try:
            loaded_log = self.service.load_file(file_path)
        except Exception as error:
            QMessageBox.critical(self, "Blad", f"Nie mozna wczytac pliku:\n{error}")
            return

        self.file_path_input.setText(str(loaded_log.path))
        self.full_log = loaded_log.entries

        if not self.full_log:
            QMessageBox.warning(self, "Ostrzezenie", "Plik jest pusty lub ma nieprawidlowy format.")
            self.clear_details()
            return

        self._set_date_range()
        self.filter_logs()

    def _set_date_range(self) -> None:
        start_date, end_date = self.service.get_date_range(self.full_log)

        self.date_from.blockSignals(True)
        self.date_to.blockSignals(True)
        self.date_from.setDate(QDate(start_date.year, start_date.month, start_date.day))
        self.date_to.setDate(QDate(end_date.year, end_date.month, end_date.day))
        self.date_from.blockSignals(False)
        self.date_to.blockSignals(False)

    def filter_logs(self) -> None:
        if not self.full_log:
            return

        try:
            self.filtered_log = self.service.filter_by_date(
                self.full_log,
                self.date_from.date().toPython(),
                self.date_to.date().toPython(),
            )
        except ValueError as error:
            QMessageBox.warning(self, "Blad filtrowania", str(error))
            return

        self.populate_list()

    def populate_list(self) -> None:
        self.log_list.clear()

        for entry in self.filtered_log:
            self.log_list.addItem(self.service.make_list_text(entry))

        if self.filtered_log:
            self.log_list.setCurrentRow(0)
        else:
            self.clear_details()

    def display_details(self, index: int) -> None:
        if index < 0 or index >= len(self.filtered_log):
            self.clear_details()
            return

        entry = self.filtered_log[index]
        self.detail_host.setText(entry.id_orig_h)
        self.detail_date.setText(entry.ts.strftime("%Y-%m-%d"))
        self.detail_time.setText(entry.ts.strftime("%H:%M:%S"))
        self.detail_tz.setText(self.service.get_timezone(entry))
        self.detail_method.setText(entry.method)
        self.detail_resource.setText(entry.uri)
        self.detail_size.setText(self.service.get_size(entry))
        self._set_status(entry.status_code)
        self._update_buttons(index)

    def _set_status(self, status_code: int | None) -> None:
        text = "-" if status_code is None else str(status_code)
        color = self.service.get_status_color(status_code)
        self.detail_status.setText(text)
        self.detail_status.setStyleSheet(
            f"background-color: {color}; border-radius: 22px; font-weight: bold;"
        )

    def clear_details(self) -> None:
        for widget in [
            self.detail_host,
            self.detail_date,
            self.detail_time,
            self.detail_tz,
            self.detail_resource,
            self.detail_size,
        ]:
            widget.clear()

        self.detail_method.setText("-")
        self._set_status(None)
        self._update_buttons(-1)

    def _update_buttons(self, index: int) -> None:
        self.prev_button.setEnabled(index > 0)
        self.next_button.setEnabled(0 <= index < len(self.filtered_log) - 1)

    def go_previous(self) -> None:
        current_row = self.log_list.currentRow()
        if current_row > 0:
            self.log_list.setCurrentRow(current_row - 1)

    def go_next(self) -> None:
        current_row = self.log_list.currentRow()
        if current_row < self.log_list.count() - 1:
            self.log_list.setCurrentRow(current_row + 1)

    def _initial_directory(self) -> str:
        log_dir = Path(__file__).resolve().parents[1] / "List2" / "utils"
        return str(log_dir if log_dir.exists() else Path(__file__).resolve().parent)


def main() -> None:
    app = QApplication(sys.argv)
    window = LogBrowserApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
