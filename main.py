from PyQt5.QtWidgets import QApplication

import sys

from gui.main_window import MainWindow


def start_app():
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_app()
