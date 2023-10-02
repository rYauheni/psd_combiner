from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

import sys


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

        # Устанавливаем начальное положение текста
        self.update_header_size()

    def resizeEvent(self, event):
        # Вызываем метод при изменении размера виджета
        self.update_header_size()
        super().resizeEvent(event)

    def update_header_size(self):
        label_width = self.width()  # Ширина текста равна ширине виджета
        label_height = 40  # Высота текста
        label_x = 0  # X-координата текста начинается с нуля
        label_y = int(self.height() * 0.2)  # Округляем до целого числа
        self.header_main.setGeometry(label_x, label_y, label_width, label_height)


class FileSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем кнопку для выбора файлов
        self.select_files_button = QPushButton(self)
        self.select_files_button.setText("SELECT")

        # Создаем метку для отображения количества выбранных файлов
        self.selected_files_label = QLabel(self)

        # Подключаем функцию обработки нажатия на кнопку
        self.select_files_button.clicked.connect(self.select_files)

    def update_positions(self):
        label_y = int(self.parent().parent().height() * 0.3)  # 30% ниже верхней границы окна

        self.select_files_button.setGeometry(20, label_y, 200, 40)
        self.selected_files_label.setGeometry(240, label_y, 200, 40)

    def select_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.ExistingFiles
        file_dialog = QFileDialog(self, options=options)
        file_dialog.setNameFilter("Text files (*.txt)")

        selected_files, _ = file_dialog.getOpenFileNames()

        if selected_files:
            self.selected_files_label.setText(f"Files selected: {len(selected_files)}")
        else:
            self.selected_files_label.setText("No files selected")


class FileProcessingWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем кнопку для запуска обработки файлов
        self.process_files_button = QPushButton(self)
        self.process_files_button.setText("PROCESS FILES")

        # Создаем метку для отображения результата обработки файлов
        self.result_label = QLabel(self)
        self.result_label.setText("Result:")

        # Создаем метку для отображения ошибок при обработке файлов
        self.error_log_label = QLabel(self)
        self.error_log_label.setText("Error Log:")

        # Подключаем функцию обработки нажатия на кнопку
        self.process_files_button.clicked.connect(self.process_files)

    def update_positions(self):
        label_y = int(self.parent().parent().height())
        print(label_y)

        self.process_files_button.setGeometry(20, round(label_y * 0.01), 200, 40)
        self.result_label.setGeometry(200, round(label_y * 0.8), 200, 40)
        self.error_log_label.setGeometry(420, round(label_y * 2), 200, 40)

    def process_files(self):
        # Здесь вы можете добавить код для обработки выбранных файлов и вывода результатов
        # Ваш функционал обработки информации в файлах должен быть реализован здесь
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('PSD Combiner')
        self.setGeometry(240, 180, 800, 600)

        # Устанавливаем фон для главного окна
        self.setStyleSheet("background-color: #627F7A;")

        # Создаем виджеты для заголовка и выбора файлов
        self.header_widget = HeaderWidget()
        self.file_selection_widget = FileSelectionWidget()

        # Создаем главный виджет и размещаем в нем виджеты
        main_widget = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(self.header_widget)
        layout.addWidget(self.file_selection_widget)

        # Создаем и добавляем FileProcessingWidget
        self.file_processing_widget = FileProcessingWidget()
        layout.addWidget(self.file_processing_widget)

        main_widget.setLayout(layout)

        # Устанавливаем главный виджет в окно
        self.setCentralWidget(main_widget)

        # Вызываем update_positions для виджетов
        self.file_selection_widget.update_positions()
        self.file_processing_widget.update_positions()


def start_app():
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_app()
