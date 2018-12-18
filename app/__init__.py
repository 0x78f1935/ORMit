from app.gui import ORMit
from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget
import sys

def create_app():
    app = QApplication(sys.argv) # Initialize app
    SI = ORMit()
    SI.show()  # Show application
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass