from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QWidget, QVBoxLayout, \
    QHBoxLayout
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

import sys

from utils.combine_tools import combine_data


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

        # Создаем метку для отображения результата обработки файлов
        self.result_label = QLabel(self)
        self.result_label.setText("Result:")

        # Создаем метку для отображения ошибок при обработке файлов
        self.error_log_label = QLabel(self)
        self.error_log_label.setText("Error Log:")

        # Подключаем функцию обработки нажатия на кнопку
        self.process_files_button.clicked.connect(self.process_files)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.process_files_button)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.error_log_label)
        self.setLayout(self.layout)

    def process_files(self):
        selected_files = self.file_selection_widget.selected_files  # Получаем выбранные файлы из FileSelectionWidget
        if selected_files:
            self.result_label.setText("Result:")
            self.error_log_label.setText("Error Log:")

            print(combine_data(selected_files))
        else:
            self.result_label.setText("Result: No files selected")


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
