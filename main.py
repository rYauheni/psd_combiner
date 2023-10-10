from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QWidget, QVBoxLayout, \
    QHBoxLayout, QScrollArea, QSizePolicy, QTextBrowser
from PyQt5.QtGui import QFont, QColor, QMovie
from PyQt5.QtCore import Qt

import sys
import time

from utils.combine_tools import combine_data

from static.style_sheet import style_sheets


class HeaderWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем QLabel для текста
        self.header_main = QLabel(self)
        self.header_main.setText("PSD Combiner")

        # Устанавливаем шрифт и цвет текста
        font = QFont("Roboto", 24, QFont.Bold)
        self.header_main.setFont(font)
        self.header_main.setStyleSheet("color: white;")

        # Устанавливаем фон
        self.setStyleSheet("background-color: #627F7A;")

        # Выравниваем текст по центру по горизонтальной оси
        self.header_main.setAlignment(Qt.AlignCenter)

    def resizeEvent(self, event):
        # Вызываем метод при изменении размера виджета
        self.update_positions()
        super().resizeEvent(event)

    def update_positions(self):
        label_width = self.width()  # Ширина текста равна ширине виджета
        label_height = 40  # Высота текста
        label_x = 0  # X-координата текста начинается с нуля
        label_y = 0  # Округляем до целого числа
        self.header_main.setGeometry(label_x, label_y, label_width, label_height)


class FileSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем кнопку для выбора файлов
        self.select_files_button = QPushButton(self)
        self.select_files_button.setText("SELECT")
        self.select_files_button.setMaximumWidth(100)

        # Создаем метку для отображения количества выбранных файлов
        self.selected_files_label = QLabel(self)

        self.selected_files = []

        # Подключаем функцию обработки нажатия на кнопку
        self.select_files_button.clicked.connect(self.select_files)

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

        # Создаем кнопку для запуска обработки файлов
        self.process_files_button = QPushButton(self)
        self.process_files_button.setText("PROCESS FILES")
        self.process_files_button.setMaximumWidth(100)

        # Подключаем функцию обработки нажатия на кнопку
        self.process_files_button.clicked.connect(self.process_files)

        # Создаем QLabel для анимации и скрываем его
        self.animation_label = QLabel(self)
        self.movie = QMovie('static/gif/processing.gif')  # Укажите путь к вашей анимации
        self.animation_label.setMovie(self.movie)
        self.animation_label.hide()

        # Создаем метку для отображения результата обработки файлов
        self.result_text = QTextBrowser(self)
        self.result_text.setPlainText("Result:")
        self.result_text.setStyleSheet(style_sheets.RESULT_SS)
        self.result_text.setFixedHeight(200)

        # Создаем кнопку "Copy" для копирования результата
        self.copy_button = QPushButton(self)
        self.copy_button.setText("Copy")
        self.copy_button.setMaximumWidth(100)
        self.copy_button.clicked.connect(self.copy_result_to_clipboard)

        # Создаем метку для отображения ошибок при обработке файлов
        self.error_log_text = QTextBrowser(self)
        self.error_log_text.setPlainText("Error Log:")
        self.error_log_text.setStyleSheet(style_sheets.ERRORS_LOG_SS)

        # Создаем область с прокруткой для error_log_label
        self.error_log_scroll_area = QScrollArea(self)
        self.error_log_scroll_area.setWidgetResizable(True)
        self.error_log_scroll_area.setMaximumHeight(160)
        self.error_log_scroll_area.setWidget(self.error_log_text)


        # Создаем кнопку "Copy2" для копирования errors
        self.copy_2_button = QPushButton(self)
        self.copy_2_button.setText("Copy2")
        self.copy_2_button.setMaximumWidth(100)
        self.copy_2_button.clicked.connect(self.copy_errors_to_clipboard)


        # Создаем горизонтальный макет для result_label и copy_button
        result_layout = QHBoxLayout()
        result_layout.addWidget(self.result_text)
        result_layout.addWidget(self.copy_button)

        # Создаем горизонтальный макет для errors
        errors_layout = QHBoxLayout()
        errors_layout.addWidget(self.error_log_scroll_area)
        errors_layout.addWidget(self.copy_2_button)

        # Основной вертикальный макет
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.process_files_button)
        self.layout.addWidget(self.animation_label)
        self.layout.addLayout(result_layout)
        self.layout.addLayout(errors_layout)

        self.setLayout(self.layout)

    def process_files(self):
        selected_files = self.file_selection_widget.selected_files  # Получаем выбранные файлы из FileSelectionWidget

        # Показываем анимацию перед началом обработки
        self.animation_label.show()
        self.movie.start()

        if selected_files:
            self.result_text.setText("Result:")
            self.error_log_text.setText("Error Log:")
            self.result_text.setPlainText("Tournaments: ___\n"
                                          "Total entries: ___ (re-entries: ___)\n"
                                          "Buy-in (total): USD ___ (USD: ___, EUR ___, CNY ___)\n"
                                          "Buy-in (first entries): USD ___ (USD: ___, EUR ___, CNY ___)\n"
                                          "Buy-in (reentries): USD ___ (USD: ___, EUR ___, CNY ___)\n"
                                          "Total received: USD ___ (USD: ___, EUR ___, CNY ___)\n"
                                          "Profit: ___")

            t1 = time.time()
            combine_data(selected_files)
            t2 = time.time()
            print(t2-t1)


        else:
            self.result_text.setText("No files selected")

        # По завершению обработки скрываем анимацию
        # self.movie.stop()
        # self.animation_label.hide()



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
        self.setGeometry(240, 180, 800, 600)

        # Устанавливаем фон для главного окна
        self.setStyleSheet("background-color: #627F7A;")

        # Создаем главный виджет
        main_widget = QWidget(self)
        layout = QVBoxLayout()

        # Устанавливаем минимальный размер между виджетами (отступ)
        layout.setSpacing(0)

        main_widget.setLayout(layout)

        # Устанавливаем главный виджет в окно
        self.setCentralWidget(main_widget)

        # Создаем виджеты для заголовка и выбора файлов
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
