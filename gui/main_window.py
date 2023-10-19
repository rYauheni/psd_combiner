from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QBrush, QPalette

from gui.widgets import HeaderWidget, FileSelectionWidget, FileProcessingWidget
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('PSD Combiner')
        self.setGeometry(240, 180, 900, 680)
        self.setMinimumSize(600, 660)

        app_icon = QIcon("static/img/favicon.ico")
        self.setWindowIcon(app_icon)

        # self.setStyleSheet("background: #627F7A;")
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2f4d48, stop:1 #86ccbd);")

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
