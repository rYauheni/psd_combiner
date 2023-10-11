from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QWidget, QVBoxLayout, \
    QHBoxLayout, QScrollArea, QSizePolicy, QTextBrowser, QSpacerItem
from PyQt5.QtGui import QFont, QColor, QMovie, QPixmap, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal

import sys
import time

from utils.combine_tools import combine_data

from static.style_sheet import style_sheets


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

    # def resizeEvent(self, event):
    #     # Вызываем метод при изменении размера виджета
    #     self.update_positions()
    #     super().resizeEvent(event)
    #
    # def update_positions(self):
    #     label_width = self.width()  # Ширина текста равна ширине виджета
    #     label_height = 40  # Высота текста
    #     label_x = 0  # X-координата текста начинается с нуля
    #     label_y = 0  # Округляем до целого числа
    #     self.header_main.setGeometry(label_x, label_y, label_width, label_height)


class FileSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a button to select files
        self.select_files_button = QPushButton(self)
        self.select_files_button.setText("Select")
        self.select_files_button.setMaximumWidth(100)
        self.select_files_button.setStyleSheet(style_sheets.BUTTON_SS)

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

        self.file_selection_widget = file_selection_widget

        # Create a button to start file processing
        self.process_files_button = QPushButton(self)
        self.process_files_button.setText("Process")
        self.process_files_button.setMaximumWidth(100)
        self.process_files_button.setStyleSheet(style_sheets.BUTTON_SS)

        # Connecting the processing button click processing function
        self.process_files_button.clicked.connect(self.process_files)

        # Create a QLabel for animation and hide it
        self.animation_label = QLabel(self)
        self.movie = QMovie('static/gif/processing.gif')  # Укажите путь к вашей анимации
        self.animation_label.setMovie(self.movie)
        self.animation_label.hide()

        # Create a text area to display the result of file processing
        self.result_text = QTextBrowser(self)
        self.result_text.setPlainText("Result:")
        self.result_text.setStyleSheet(style_sheets.RESULT_SS)
        self.result_text.setFixedHeight(200)

        # Create a copy button to copy the result
        self.copy_button = QPushButton(self)
        self.copy_button.setText("Copy")
        self.copy_button.setMaximumWidth(100)
        self.copy_button.clicked.connect(self.copy_result_to_clipboard)
        self.copy_button.setStyleSheet(style_sheets.BUTTON_SS)

        # Create a text area to display errors when processing files
        self.error_log_text = QTextBrowser(self)
        self.error_log_text.setPlainText("Error Log:")
        self.error_log_text.setStyleSheet(style_sheets.ERRORS_LOG_SS)

        # Create a scroll area for error_log_label
        self.error_log_scroll_area = QScrollArea(self)
        self.error_log_scroll_area.setWidgetResizable(True)
        self.error_log_scroll_area.setMaximumHeight(160)
        self.error_log_scroll_area.setWidget(self.error_log_text)

        # Create a copy button to copy the error_log
        self.copy_2_button = QPushButton(self)
        self.copy_2_button.setText("Copy")
        self.copy_2_button.setMaximumWidth(100)
        self.copy_2_button.clicked.connect(self.copy_errors_to_clipboard)
        self.copy_2_button.setStyleSheet(style_sheets.BUTTON_SS)

        # Create layouts

        # Create a horizontal layout for process_files_button and animation_label
        process_layout = QHBoxLayout()
        process_layout.addWidget(self.process_files_button)
        process_layout.addWidget(self.animation_label)
        process_layout.setAlignment(Qt.AlignLeft)

        # Create a horizontal layout for result_label and copy_button
        result_layout = QHBoxLayout()
        result_layout.addWidget(self.result_text)
        result_layout.addWidget(self.copy_button)

        # Create a horizontal layout for error_log and copy_errors_button
        errors_layout = QHBoxLayout()
        errors_layout.addWidget(self.error_log_scroll_area)
        errors_layout.addWidget(self.copy_2_button)

        # Create a basic vertical layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(process_layout)
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


            t1 = time.time()
            # Create a background thread to execute combine_data
            self.worker_thread = WorkerThread(selected_files)
            self.worker_thread.result_ready.connect(self.handle_worker_thread_result)
            self.worker_thread.start()
            t2 = time.time()
            print(t2-t1)

        else:
            self.result_text.setText("No files selected")

    def handle_worker_thread_result(self, result):
        # Here we process the result of executing combine_data and hide the animation
        self.movie.stop()
        self.animation_label.hide()
        self.result_text.setPlainText("Tournaments: ___\n"
                                      "Total entries: ___ (re-entries: ___)\n"
                                      "Buy-in (total): USD ___ (USD: ___, EUR ___, CNY ___)\n"
                                      "Buy-in (first entries): USD ___ (USD: ___, EUR ___, CNY ___)\n"
                                      "Buy-in (reentries): USD ___ (USD: ___, EUR ___, CNY ___)\n"
                                      "Total received: USD ___ (USD: ___, EUR ___, CNY ___)\n"
                                      "Profit: ___")
        print(result)

    def copy_result_to_clipboard(self):
        text = self.result_text.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def copy_errors_to_clipboard(self):
        text = self.error_log_text.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('PSD Combiner')
        self.setGeometry(240, 180, 800, 680)
        self.setMinimumSize(600, 640)

        app_icon = QIcon("static/img/2222.ico")
        self.setWindowIcon(app_icon)

        self.setStyleSheet("background-color: #627F7A;")

        main_widget = QWidget(self)
        layout = QVBoxLayout()

        layout.setSpacing(0)

        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)

        self.header_widget = HeaderWidget()
        self.file_selection_widget = FileSelectionWidget()
        self.file_processing_widget = FileProcessingWidget(self.file_selection_widget)

        layout.addWidget(self.header_widget)
        layout.addWidget(self.file_selection_widget)
        layout.addWidget(self.file_processing_widget)


def start_app():
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_app()
