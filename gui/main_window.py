from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon

from gui.widgets import HeaderWidget, FileSelectionWidget, FileProcessingWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('PSD Combiner')
        self.setGeometry(240, 180, 900, 680)
        self.setMinimumSize(600, 660)

        app_icon = QIcon("static/img/favicon.ico")
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
