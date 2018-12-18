from app.layouts.gui import Ui_MainWindow as GUI
from app.version import VersionCheck
from app.settings import *
from PyQt5.QtGui import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os, sys, binascii, subprocess
from app.parser import convert as CONVERT


class ORMit(QMainWindow, GUI, VersionCheck):
    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        super(GUI, self).__init__(*args, **kwargs)
        VersionCheck.__init__(self)

        initialRun = True
        if initialRun:
            self.setupUi(self)
            self.setWindowIcon(QIcon(os.path.join(os.path.join(os.path.join(os.getcwd(), 'app'), 'layouts'), 'app.png')))  # Set icon along the title

            initialRun = False
            self.timer = QTimer(self)

            # Check version
            update = VersionCheck.check(self)
            self.version.setText(self.y.decode())
            if update:
                QMessageBox().warning(self, "Update available", "You know where to ask", QMessageBox.Ok)

            # Preferences
            self.pushFont.clicked.connect(self.font_choice)
            # Fetch style options
            style_keys = QStyleFactory.keys()
            for i in style_keys:
                self.pushStyle.addItem(i)
            self.pushStyle.activated[str].connect(self.style_choice)

            # Header bar
            self.actionSave.triggered.connect(self.file_save)
            self.actionOpen.triggered.connect(self.file_open)
            self.actionAbout.triggered.connect(self.about)
            self.actionCheck_for_updates.triggered.connect(self.check_new_version)
            self.actionExit.triggered.connect(self.close_application)

            # Actions
            self.pushButton.clicked.connect(self.copy_results)
            self.pushButton_2.clicked.connect(self.convert_sql)

    def font_choice(self):
        """Changes font of the application"""
        font, valid = QFontDialog.getFont()
        if valid:
            self.setFont(font)
    
    def style_choice(self, text):
        """Changes window style of the application"""
        QApplication.setStyle(QStyleFactory.create(text))

    def close_application(self):
        """Closes application"""
        choice = QMessageBox.question(
            self,
            "Quit!?", "Are you sure?",
            QMessageBox.Yes | QMessageBox.No
        )
        if choice == QMessageBox.Yes: sys.exit()
        else: pass

    def file_open(self):
        """Tries to open the file into the text editor"""
        self.tabWidget.setCurrentIndex(0)
        name = QFileDialog.getOpenFileName(self, 'Open File', filter='*.sql')
        try:
            data = open(name[0], 'r')
            with data:
                text = data.read().encode('latin1').decode('cp1251')
                self.textEdit.setText(str(text))
        except FileNotFoundError as e:
            self.textBrowser.setText(str(e))

    def file_save(self):
        """Saves plain text from the editor to a file format"""
        self.tabWidget.setCurrentIndex(0)
        name = QFileDialog.getSaveFileName(self, 'Save File', filter='*.sql')
        try:
            data = open(name[0], 'w')
            text = self.textBrowser.toPlainText()
            data.write(text)
            data.close()
        except (FileExistsError, FileNotFoundError):
            pass

    def about(self):
        QMessageBox().information(self,  "Placeholder", binascii.unhexlify(MAPI).decode(), QMessageBox.Ok)
    
    def check_new_version(self):
        # Check version
        update = VersionCheck.check(self)
        if update:
            QMessageBox().information(self, "Update available", "You know where to ask", QMessageBox.Ok)
        else:
            QMessageBox().information(self, "Update not available", "Currently no update available", QMessageBox.Ok)
    
    def convert_sql(self):
        text = []
        s = ' '.join(str(self.textEdit.toPlainText()).split('\n'))
        if ';' in s:
            text = s.split(';')
        else:
            text.append(s)

        text = [i for i in text if i != '']

        results = []
        for query in text:      
            try:
                q = str(CONVERT.to_sqla(query))
                result = str(self.lineEdit.text()) + " = " + q
            except IndexError:
                result = "Please insert a SQL query first!"
            except Exception as e:
                if e.args: result = "ERROR {} ON QUERY: {}".format(query, str(e.args[0]))
                else: result = "UNEXPECTED ERROR {} ON QUERY: {}".format(e, query)
            finally:
                results.append(result)
        self.textBrowser.setText('\n\n'.join(results))

    def copy_results(self):
        text = str(self.textBrowser.toPlainText())
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)
        QMessageBox().information(self, "Code copied", "You have copied the PYTHON code.", QMessageBox.Ok)