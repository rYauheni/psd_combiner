from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QFileDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextBrowser
)

from PyQt5.QtGui import QFont, QMovie, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from utils.combine_tools import combine_data

from static.style_sheet import style_sheets

from parse_templates.parse_templates_list import TEMPLATES_TITLES


class WorkerThread(QThread):
    result_ready = pyqtSignal(object)

    def __init__(self, selected_files):
        super().__init__()
        self.selected_files = selected_files

    def run(self):
        result = combine_data(self.selected_files)
        self.result_ready.emit(result)


class HeaderWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QLabel for text
        self.header_main = QLabel(self)
        self.header_main.setText("PSD Combiner")

        font = QFont("Roboto", 24, QFont.Bold)
        self.header_main.setFont(font)
        self.header_main.setStyleSheet("color: white;")
        self.setStyleSheet("background: transparent;")

        # Create a QLabel for image
        self.header_image = QLabel(self)
        pixmap = QPixmap("static/img/cards.png")
        scaled_pixmap = pixmap.scaled(192, 142, Qt.KeepAspectRatio)
        self.header_image.setPixmap(scaled_pixmap)

        # Align the text and image centered along the horizontal axis
        self.header_main.setAlignment(Qt.AlignCenter)
        self.header_image.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.header_image)
        self.layout.addWidget(self.header_main)
        self.setLayout(self.layout)


class FileSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a button to select files
        self.select_files_button = QPushButton(self)
        self.select_files_button.setText("Select")
        self.select_files_button.setMaximumWidth(100)
        self.select_files_button.setStyleSheet(style_sheets.BUTTON_EXEC_SS)

        # Create a label to display the number of selected files
        self.selected_files_label = QLabel(self)
        self.selected_files_label.setStyleSheet(style_sheets.SUBSIDIARY_TEXT_SS)
        self.selected_files = []

        # Connect the select button click processing function
        self.select_files_button.clicked.connect(self.select_files)

        # Create a horizontal layout for select_files_button and selected_files_label
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.select_files_button)
        self.layout.addWidget(self.selected_files_label)
        self.setLayout(self.layout)

        self.setStyleSheet("background: transparent;")

    def select_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.ExistingFiles
        file_dialog = QFileDialog(self, options=options)
        file_dialog.setNameFilter("Text files (*.txt)")

        self.selected_files, _ = file_dialog.getOpenFileNames()

        if self.selected_files:
            self.selected_files_label.setText(f"Files selected: {len(self.selected_files)}")
        else:
            self.selected_files_label.setText("No files selected")


class FileProcessingWidget(QWidget):
    def __init__(self, file_selection_widget):
        super().__init__()

        self.metrics_data = None

        self.file_selection_widget = file_selection_widget

        # Create a button to start file processing
        self.process_files_button = QPushButton(self)
        self.process_files_button.setText("Process")
        self.process_files_button.setMaximumWidth(100)
        self.process_files_button.setStyleSheet(style_sheets.BUTTON_EXEC_SS)

        # Connecting the processing button click processing function
        self.process_files_button.clicked.connect(self.process_files)

        # Create a QLabel for animation and hide it
        self.animation_label = QLabel(self)
        self.movie = QMovie('static/gif/processing.gif')  # Укажите путь к вашей анимации
        self.animation_label.setMovie(self.movie)
        self.animation_label.setStyleSheet("background: transparent;")
        self.animation_label.hide()

        # Create a text area to display the result of file processing
        self.result_text = QTextBrowser(self)
        self.result_text.setPlainText("Result:")
        self.result_text.setStyleSheet(style_sheets.RESULT_SS)
        self.result_text.setFixedHeight(170)

        # Create a button to copy the result
        self.copy_button = QPushButton(self)
        self.copy_button.setText("Copy")
        self.copy_button.setMaximumWidth(100)
        self.copy_button.clicked.connect(self.copy_result_to_clipboard)
        self.copy_button.setStyleSheet(style_sheets.BUTTON_COPY_SS)

        # Create a button to export the result
        self.export_button = QPushButton(self)
        self.export_button.setText("Export")
        self.export_button.setMaximumWidth(100)
        self.export_button.clicked.connect(self.export_result)
        self.export_button.setStyleSheet(style_sheets.BUTTON_COPY_SS)

        # Create a text area to display errors when processing files
        self.error_log_text = QTextBrowser(self)
        self.error_log_text.setPlainText("Error Log:")
        self.error_log_text.setStyleSheet(style_sheets.ERRORS_LOG_BASE_SS)
        self.error_log_text.setFixedHeight(100)

        # Create a button to copy the error_log
        self.copy_2_button = QPushButton(self)
        self.copy_2_button.setText("Copy")
        self.copy_2_button.setMaximumWidth(100)
        self.copy_2_button.clicked.connect(self.copy_errors_to_clipboard)
        self.copy_2_button.setStyleSheet(style_sheets.BUTTON_COPY_SS)

        # Create layouts

        # Create a horizontal layout for process_files_button and animation_label
        process_layout = QHBoxLayout()
        process_layout.addWidget(self.process_files_button)
        process_layout.addWidget(self.animation_label)
        process_layout.setAlignment(Qt.AlignLeft)

        # Create a vertical layout for copy_button and export_button
        copy_export_layout = QVBoxLayout()
        copy_export_layout.addWidget(self.copy_button)
        copy_export_layout.addWidget(self.export_button)

        # Create a horizontal layout for result_label and copy_export_layout
        result_layout = QHBoxLayout()
        result_layout.addWidget(self.result_text)
        result_layout.addLayout(copy_export_layout)

        # Create a horizontal layout for error_log and copy_errors_button
        errors_layout = QHBoxLayout()
        errors_layout.addWidget(self.error_log_text)
        errors_layout.addWidget(self.copy_2_button)

        # Create a basic vertical layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(process_layout)
        self.layout.addSpacing(16)
        self.layout.addLayout(result_layout)
        self.layout.addLayout(errors_layout)

        self.setLayout(self.layout)

    def process_files(self):
        selected_files = self.file_selection_widget.selected_files

        if selected_files:

            # Showing the animation before processing begins
            self.animation_label.show()
            self.movie.start()

            self.result_text.setText("Result:")
            self.error_log_text.setText("Error Log:")

            # Create a background thread to execute combine_data
            self.worker_thread = WorkerThread(selected_files)
            self.worker_thread.result_ready.connect(self.handle_worker_thread_result)
            self.worker_thread.start()

        else:
            self.result_text.setText("No files selected")
            self.error_log_text.setText("No files selected")

    def handle_worker_thread_result(self, result):
        # Processing the result of executing combine_data and hide the animation
        self.movie.stop()
        self.animation_label.hide()

        metrics = result[0]
        errors = result[1]

        self.metrics_data = metrics

        bi = metrics[f'{TEMPLATES_TITLES["buy_in"]}']
        tr = metrics[f'{TEMPLATES_TITLES["total_received"]}']
        er = metrics['exchange_rate']

        if metrics['tournaments_n'] > 0:
            self.result_text.setPlainText(f"Tournaments: {metrics['tournaments_n']}\n"
                                          f"Total entries: {metrics['total_entries_n']} "
                                          f"(re-entries: {metrics['re_entries_n']})\n"
                                          f"Buy-in (total): USD {bi['total']['convert']} (USD: {bi['total']['USD']}, "
                                          f"EUR {bi['total']['EUR']}, CNY {bi['total']['CNY']})\n"
                                          f"Buy-in (first entries): USD {bi['first_entries']['convert']} "
                                          f"(USD: {bi['first_entries']['USD']}, EUR {bi['first_entries']['EUR']}, "
                                          f"CNY {bi['first_entries']['CNY']})\n"
                                          f"Buy-in (re-entries): USD {bi['re_entries']['convert']} "
                                          f"(USD: {bi['re_entries']['USD']}, EUR {bi['re_entries']['EUR']}, "
                                          f"CNY {bi['re_entries']['CNY']})\n"
                                          f"Total received: USD {tr['convert']} (USD: {tr['USD']}, "
                                          f"Cash_USD: {tr['CASH_USD']}, EUR {tr['EUR']}, CNY {tr['CNY']})\n"
                                          f"Profit: USD {metrics['profit']}\n"
                                          f"Exchange rates: 1 EUR = {er['EUR']} USD; 1 CNY = {er['CNY']} USD")
        else:
            self.result_text.setPlainText("No appropriate files found")

        errors_check = sum([0] + [1 for value in errors.values() if value])

        if errors_check:
            self.error_log_text.setStyleSheet(style_sheets.ERRORS_LOG_1_SS)
            self.error_log_text.verticalScrollBar().setStyleSheet(style_sheets.SCROLLBAR_SS)

            errors_log_message = ''
            end = '_' * 60 + '\n\n'

            ge = errors['general_errors']
            if ge:
                ers = '\n'.join(e for e in ge)
                errors_log_message += f"General errors:\n{ers}\n"
                errors_log_message += end

            d = errors['duplicates']
            if d:
                errors_log_message += f"Duplicates detected: {d}\n"
                errors_log_message += end

            nt = errors['no_txt']
            if nt:
                errors_log_message += f"Inappropriate files detected: {nt}\n"
                errors_log_message += end

            fe = errors['file_errors']
            if fe:
                errors_log_message += "File errors:\n"
                part_end = '_' * 20 + '\n'
                for e in fe:
                    ers = '\n'.join(er for er in e['errors'])
                    errors_log_message += f"File: {e['file']}\n" \
                                          f"Content:\n{e['content']}\n" \
                                          f"Errors:\n{ers}\n"
                    errors_log_message += part_end
                errors_log_message += end

            self.error_log_text.setPlainText(errors_log_message)

        else:
            self.error_log_text.setStyleSheet(style_sheets.ERRORS_LOG_0_SS)
            self.error_log_text.setPlainText("No errors found")

    def copy_result_to_clipboard(self):
        text = self.result_text.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def export_result(self):
        result = self.metrics_data

        bi = result[f'{TEMPLATES_TITLES["buy_in"]}']
        tr = result[f'{TEMPLATES_TITLES["total_received"]}']

        text = f"Tournaments\t{result['tournaments_n']}\n" \
               f"Total entries\t{result['total_entries_n']}\n" \
               f"Re-entries\t{result['re_entries_n']}\n" \
               f"Buy-in, $\t{str(bi['total']['convert']).replace('.', ',')}\n" \
               f"Buy-in (first entries), $\t{str(bi['first_entries']['convert']).replace('.', ',')}\n" \
               f"Buy-in (re-entries), $\t{str(bi['re_entries']['convert']).replace('.', ',')}\n" \
               f"Total received, $\t{str(tr['convert']).replace('.', ',')}\n" \
               f"Profit, $\t{str(result['profit']).replace('.', ',')}\n"

        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def copy_errors_to_clipboard(self):
        text = self.error_log_text.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
