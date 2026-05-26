import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QPushButton, QLabel,
                               QListWidget, QDateEdit, QGridLayout, QFileDialog,
                               QMessageBox)
from PySide6.QtCore import Qt, QDate

# Import funkcji do czytania logów z Twojej poprzedniej listy
from List2.readLog import read_log


class LogBrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log browser")
        self.resize(850, 500)

        # Zmienne przechowujące stan aplikacji
        self.full_log = []
        self.filtered_log = []

        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # ================= Górny pasek =================
        top_layout = QHBoxLayout()
        self.file_path_input = QLineEdit()
        self.file_path_input.setReadOnly(True)
        self.file_path_input.setPlaceholderText("Wybierz plik z logami...")
        
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.load_file)
        
        top_layout.addWidget(self.file_path_input)
        top_layout.addWidget(self.open_button)
        main_layout.addLayout(top_layout)

        # ================= Główny obszar (Master-Detail) =================
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # --- Lewa strona (Master) ---
        left_layout = QVBoxLayout()
        content_layout.addLayout(left_layout, stretch=1)

        # Filtrowanie dat
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
        
        left_layout.addLayout(dates_layout)

        # Lista logów
        self.log_list = QListWidget()
        self.log_list.currentRowChanged.connect(self.display_details)
        left_layout.addWidget(self.log_list)

        # Przycisk "Previous"
        self.prev_button = QPushButton("Previous")
        self.prev_button.setEnabled(False)
        self.prev_button.clicked.connect(self.go_previous)
        left_layout.addWidget(self.prev_button, alignment=Qt.AlignLeft)

        # --- Prawa strona (Detail) ---
        right_layout = QVBoxLayout()
        content_layout.addLayout(right_layout, stretch=1)

        detail_grid = QGridLayout()
        right_layout.addLayout(detail_grid)

        # Inicjalizacja pól szczegółów
        detail_grid.addWidget(QLabel("Remote host:"), 0, 0)
        self.detail_host = QLineEdit()
        self.detail_host.setReadOnly(True)
        detail_grid.addWidget(self.detail_host, 0, 1, 1, 3)

        detail_grid.addWidget(QLabel("Date:"), 1, 0)
        self.detail_date = QLineEdit()
        self.detail_date.setReadOnly(True)
        detail_grid.addWidget(self.detail_date, 1, 1, 1, 3)

        detail_grid.addWidget(QLabel("Time:"), 2, 0)
        self.detail_time = QLineEdit()
        self.detail_time.setReadOnly(True)
        detail_grid.addWidget(self.detail_time, 2, 1)

        detail_grid.addWidget(QLabel("Timezone:"), 2, 2)
        self.detail_tz = QLineEdit()
        self.detail_tz.setReadOnly(True)
        detail_grid.addWidget(self.detail_tz, 2, 3)

        detail_grid.addWidget(QLabel("Status code:"), 3, 0)
        self.detail_status = QLabel("")
        self.detail_status.setFixedSize(35, 35)
        self.detail_status.setAlignment(Qt.AlignCenter)
        self.detail_status.setStyleSheet("background-color: lightgray; border-radius: 17px; font-weight: bold;")
        detail_grid.addWidget(self.detail_status, 3, 1)

        detail_grid.addWidget(QLabel("Method:"), 3, 2)
        self.detail_method = QLabel("")
        detail_grid.addWidget(self.detail_method, 3, 3)

        detail_grid.addWidget(QLabel("Resource:"), 4, 0)
        self.detail_resource = QLineEdit()
        self.detail_resource.setReadOnly(True)
        detail_grid.addWidget(self.detail_resource, 4, 1, 1, 3)

        detail_grid.addWidget(QLabel("UID:"), 5, 0)
        self.detail_uid = QLineEdit()
        self.detail_uid.setReadOnly(True)
        detail_grid.addWidget(self.detail_uid, 5, 1, 1, 3)

        right_layout.addStretch()

        # Przycisk "Next"
        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.go_next)
        right_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

    # ================= Logika aplikacji =================

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik logu", "", "Log Files (*.log);;All Files (*)")
        if not file_path:
            return

        self.file_path_input.setText(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.full_log = read_log(f)
            
            if not self.full_log:
                QMessageBox.warning(self, "Ostrzeżenie", "Plik jest pusty lub ma nieprawidłowy format.")
                return

            # Ustawienie kalendarzy na skrajne daty z pliku
            min_date = min(entry.ts.date() for entry in self.full_log)
            max_date = max(entry.ts.date() for entry in self.full_log)

            # Blokada sygnałów na moment konfiguracji kalendarza (żeby nie filtrować podwójnie)
            self.date_from.blockSignals(True)
            self.date_to.blockSignals(True)

            self.date_from.setDate(QDate(min_date.year, min_date.month, min_date.day))
            self.date_to.setDate(QDate(max_date.year, max_date.month, max_date.day))

            self.date_from.blockSignals(False)
            self.date_to.blockSignals(False)

            self.filter_logs()

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas wczytywania pliku:\n{e}")

    def filter_logs(self):
        if not self.full_log:
            return

        start_date = self.date_from.date().toPython()
        end_date = self.date_to.date().toPython()

        # Filtrowanie i zachowanie tylko logów z odpowiedniego przedziału
        self.filtered_log = [
            entry for entry in self.full_log
            if start_date <= entry.ts.date() <= end_date
        ]

        self.populate_list()

    def populate_list(self):
        self.log_list.clear()
        
        for entry in self.filtered_log:
            # Ucinanie URI do ok. 30 znaków zgodnie z instrukcją
            short_uri = entry.uri[:30] + "..." if len(entry.uri) > 30 else entry.uri
            formatted_ts = entry.ts.strftime("%d/%b/%Y:%H:%M:%S %z")
            
            list_item_text = f'{entry.id_orig_h} - [{formatted_ts}] "{entry.method} {short_uri}"'
            self.log_list.addItem(list_item_text)

        if self.filtered_log:
            self.log_list.setCurrentRow(0)
        else:
            self.clear_details()

    def display_details(self, index):
        if index < 0 or index >= len(self.filtered_log):
            self.clear_details()
            return

        entry = self.filtered_log[index]

        # Wypełnianie pól formularza Detail
        self.detail_host.setText(entry.id_orig_h)
        self.detail_date.setText(entry.ts.strftime("%Y-%m-%d"))
        self.detail_time.setText(entry.ts.strftime("%H:%M:%S"))
        self.detail_tz.setText(entry.ts.strftime("%Z") or "UTC")
        self.detail_method.setText(entry.method)
        self.detail_resource.setText(entry.uri)
        self.detail_uid.setText(entry.uid)

        # Okrągły wskaźnik Status Code
        code = entry.status_code
        if code:
            self.detail_status.setText(str(code))
            if 200 <= code < 300:
                color = "#4CAF50" # Zielony dla 2xx
            elif 300 <= code < 400:
                color = "#2196F3" # Niebieski dla 3xx
            elif 400 <= code < 600:
                color = "#F44336" # Czerwony dla błędów
            else:
                color = "#FF9800" # Pomarańczowy dla innych
                
            self.detail_status.setStyleSheet(f"background-color: {color}; color: white; border-radius: 17px; font-weight: bold;")
        else:
            self.detail_status.setText("-")
            self.detail_status.setStyleSheet("background-color: lightgray; border-radius: 17px;")

        # Uaktualnienie stanu przycisków Prev/Next
        self.prev_button.setEnabled(index > 0)
        self.next_button.setEnabled(index < len(self.filtered_log) - 1)

    def clear_details(self):
        self.detail_host.clear()
        self.detail_date.clear()
        self.detail_time.clear()
        self.detail_tz.clear()
        self.detail_method.clear()
        self.detail_resource.clear()
        self.detail_uid.clear()
        self.detail_status.setText("")
        self.detail_status.setStyleSheet("background-color: lightgray; border-radius: 17px;")
        
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)

    def go_previous(self):
        current_row = self.log_list.currentRow()
        if current_row > 0:
            self.log_list.setCurrentRow(current_row - 1)

    def go_next(self):
        current_row = self.log_list.currentRow()
        if current_row < self.log_list.count() - 1:
            self.log_list.setCurrentRow(current_row + 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogBrowserApp()
    window.show()
    sys.exit(app.exec())
