#!/usr/bin/env python3

import os
import sys
import resources
from HashChecker import checkHash
import PyQt5
from PyQt5 import uic, sip
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QFileDialog, QDesktopWidget, QTextEdit
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

appFolder = os.path.dirname(sys.argv[0]) + '/'  # Application root location


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(appFolder + 'ui/MainWindow.ui', self)
        self.currentFileLoc = None
        self.doneIcon = QPixmap(':/done/done.png')
        self.loading = QMovie(':loading/loading.gif')
        self.hashCalcUI()

    def makeWindowCenter(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def hashCalcUI(self):
        # Making window centered
        self.makeWindowCenter()
        # Window customizing
        self.setWindowTitle('Hash Calculator')
        self.setWindowIcon(QIcon(':icon/icon.png'))
        # Textbox customizing
        self.textBoxMD5.setStyleSheet("""QTextEdit { font-size: 15px; }""")
        self.textBoxSHA256.setStyleSheet("""QTextEdit { font-size: 15px; }""")
        self.textBoxSHA512.setStyleSheet("""QTextEdit { font-size: 15px; }""")
        # Buttons actions
        self.openFileButton.clicked.connect(self.openFileDialog)
        self.removeFileButton.clicked.connect(self.removeFileButton_OnClick)

    @pyqtSlot()
    # Close event
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?\nAll changes will be lost.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.statusBar().showMessage('Exited.')
            event.accept()
        else:
            self.statusBar().showMessage('Welcome back.')
            event.ignore()

    # File Dialogs

    def openFileDialog(self):
        try:
            self.openFileButton.clicked.disconnect()
        except:
            pass
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog # Qt's builtin File Dialogue
        fileName, _= QFileDialog.getOpenFileName(self, "Open", "", "All Files (*.*)", options=options)
        if fileName:
            self.currentFileLoc = fileName
            self.labelFile.setPixmap(self.doneIcon)
            self.openFileButton.setText("'" + os.path.basename(self.currentFileLoc) + "' is loaded")
            with open('temp486.temp', 'w') as temp:
                temp.write(self.currentFileLoc)
            self.start_Hash_Calculation()
        self.openFileButton.clicked.connect(self.openFileDialog)

    # Buttons Actions Function

    def start_Hash_Calculation(self):
        self.loadingCircle('start')
        self.textBoxMD5.setText("Computing...")
        self.textBoxSHA256.setText("Computing...")
        self.textBoxSHA512.setText("Computing...")
        self.hashing = Hashing()
        self.hashing.signalMD5.connect(self.textBoxMD5.setText)
        self.hashing.signalSHA256.connect(self.textBoxSHA256.setText)
        self.hashing.signalSHA512.connect(self.textBoxSHA512.setText)
        self.hashing.signalStopLoading.connect(self.loadingCircle)
        self.hashing.start()

    def loadingCircle(self, x):
        if(x == 'start'):
            self.loading.setSpeed(250)
            self.labelDoneMD5.setMovie(self.loading)
            self.labelDoneSHA256.setMovie(self.loading)
            self.labelDoneSHA512.setMovie(self.loading)
            self.loading.start()
        elif(x == 'stop_MD5'):
            self.labelDoneMD5.setPixmap(self.doneIcon)
        elif(x == 'stop_SHA256'):
            self.labelDoneSHA256.setPixmap(self.doneIcon)
        elif(x == 'stop_SHA512'):
            self.labelDoneSHA512.setPixmap(self.doneIcon)

    def removeFileButton_OnClick(self):
        try:
            self.removeFileButton.clicked.disconnect()
        except:
            pass
        self.currentFileLoc = None
        self.openFileButton.setText('Click here to open a file')
        self.textBoxMD5.setText("")
        self.textBoxSHA256.setText("")
        self.textBoxSHA512.setText("")
        self.labelDoneMD5.setText(" ")
        self.labelDoneSHA256.setText(" ")
        self.labelDoneSHA512.setText(" ")
        self.labelFile.setPixmap(QPixmap(appFolder + 'icons/folder_open.png'))
        self.removeFileButton.clicked.connect(self.removeFileButton_OnClick)


class Hashing(QThread):

    signalMD5 = pyqtSignal(str)
    signalSHA256 = pyqtSignal(str)
    signalSHA512 = pyqtSignal(str)
    signalStopLoading = pyqtSignal(str)

    def run(self):
        with open('temp486.temp', 'r') as temp:
            fileLoc = temp.read()
        os.remove('temp486.temp')
        for i in range(1):
            self.signalMD5.emit(checkHash(fileLoc, 'md5'))
            self.signalStopLoading.emit('stop_MD5')
        for i in range(1):
            self.signalSHA256.emit(checkHash(fileLoc, 'sha256'))
            self.signalStopLoading.emit('stop_SHA256')
        for i in range(1):
            self.signalSHA512.emit(checkHash(fileLoc, 'sha512'))
            self.signalStopLoading.emit('stop_SHA512')


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
