#!/usr/bin/env python3

import os
import sys
import resources
import pyperclip
from functools import partial
from HashChecker import checkHash
import PyQt5
from PyQt5 import uic, sip
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QFileDialog, QDesktopWidget, QTextEdit
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

appFolder = os.path.dirname(os.path.realpath(sys.argv[0])) + '/'  # Application root location


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(appFolder + 'ui/MainWindow.ui', self)
        # Loaded File Location Variable
        self.currentFileLoc = None
        # Icons Variables
        self.icon = QIcon(':icon/icon.png')
        self.doneIcon = QPixmap(':/done/done.png')
        self.matchedIcon = QPixmap(':/matched/matched.png')
        self.errorIcon = QPixmap(':/error/error.png')
        self.loading = QMovie(':loading/loading.gif')
        # Main UI Calling
        self.hashCheckerUI()

    def makeWindowCenter(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def hashCheckerUI(self):
        # Making window centered
        self.makeWindowCenter()
        # Window customizing
        self.setWindowTitle('Hash Checker')
        self.setWindowIcon(self.icon)
        # Textbox customizing
        self.textBoxMD5.setStyleSheet("""QTextEdit { font-size: 15px; }""")
        self.textBoxSHA256.setStyleSheet("""QTextEdit { font-size: 15px; }""")
        self.textBoxSHA512.setStyleSheet("""QTextEdit { font-size: 15px; }""")
        # Buttons actions
        self.openFileButton.clicked.connect(self.openFileDialog)
        self.removeFileButton.clicked.connect(self.removeFileButton_OnClick)
        self.clipboardButton.clicked.connect(self.clipboardText)
        self.checkButton.clicked.connect(self.checkButton_OnClick)
        # Clipboard Buttons actions
        self.clipboardMD5Button.clicked.connect(partial(self.clipboardButtonActions_OnClick, 'md5'))
        self.clipboardSHA256Button.clicked.connect(partial(self.clipboardButtonActions_OnClick, 'sha256'))
        self.clipboardSHA512Button.clicked.connect(partial(self.clipboardButtonActions_OnClick, 'sha512'))
        # Adding Place Holder Text
        self.textBoxMD5.setPlaceholderText('...')
        self.textBoxSHA256.setPlaceholderText('...')
        self.textBoxSHA512.setPlaceholderText('...')
        self.textBoxCheck.setPlaceholderText('Paste your hash here to match with or leave empty\nOnly MD5 or SHA256 or SHA512 is allowed')

    @pyqtSlot()
    # Open With Function
    def openWith(self, argFile):
        self.currentFileLoc = argFile
        self.labelFile.setPixmap(self.doneIcon)
        self.openFileButton.setText("'" + os.path.basename(self.currentFileLoc) + "' is loaded")
        with open('temp486.temp', 'w') as temp:
            temp.write(self.currentFileLoc)
        self.start_Hash_Calculation()
        print(argFile)

    # Clipboard Buttons Action Functions

    def clipboardButtonActions_OnClick(self, hashName):
        try:
            self.clipboardMD5Button.clicked.disconnect()
            self.clipboardSHA256Button.clicked.disconnect()
            self.clipboardSHA512Button.clicked.disconnect()
        except:
            pass
        if(self.currentFileLoc != None):
            if(hashName == 'md5'):
                clipText = self.textBoxMD5.toPlainText()
                pyperclip.copy(clipText.strip())
                self.statusBar().showMessage('MD5sum has been copied to clipboard')
            elif(hashName == 'sha256'):
                clipText = self.textBoxSHA256.toPlainText()
                pyperclip.copy(clipText.strip())
                self.statusBar().showMessage('SHA256sum has been copied to clipboard')
            elif(hashName == 'sha512'):
                clipText = self.textBoxSHA512.toPlainText()
                pyperclip.copy(clipText.strip())
                self.statusBar().showMessage('SHA512sum has been copied to clipboard')
        else:
            pass
        self.clipboardMD5Button.clicked.connect(partial(self.clipboardButtonActions_OnClick, 'md5'))
        self.clipboardSHA256Button.clicked.connect(partial(self.clipboardButtonActions_OnClick, 'sha256'))
        self.clipboardSHA512Button.clicked.connect(partial(self.clipboardButtonActions_OnClick, 'sha512'))

    # Clipboard Text

    def clipboardText(self):
        try:
            self.clipboardButton.clicked.disconnect()
        except:
            pass
        clipText = QApplication.clipboard().text()
        clipText = clipText.strip()
        self.textBoxCheck.setText(clipText)
        self.clipboardButton.clicked.connect(self.clipboardText)

    def checkButton_OnClick(self):
        try:
            self.checkButton.clicked.disconnect()
        except:
            pass
        clipText = self.textBoxCheck.toPlainText()
        clipText = clipText.strip()

        if(len(clipText) == 32):
            if(self.textBoxMD5.toPlainText() == clipText):
                self.checkButtonDialogue('Congrats 😄😄😄\nMD5sum has matched')
            else:
                self.checkButtonDialogue('Sorry 😢😢😢\nMD5sum doesn\'t matched', -1)
        elif(len(clipText) == 64):
            if(self.textBoxSHA256.toPlainText() == clipText):
                self.checkButtonDialogue('Congrats 😄😄😄\nSHA256sum has matched')
            else:
                self.checkButtonDialogue('Sorry 😢😢😢\nSHA256sum doesn\'t matched', -1)
        elif(len(clipText) == 128):
            if(self.textBoxSHA512.toPlainText() == clipText):
                self.checkButtonDialogue('Congrats 😄😄😄\nSHA512sum has matched')
            else:
                self.checkButtonDialogue('Sorry 😢😢😢\nSHA512sum doesn\'t matched', -1)
        elif(len(clipText) == 0):
            self.checkButtonDialogue('Error 😠😠😠\nNo hash found', -1)
        else:
            self.checkButtonDialogue('Error 😤😤😤\nWrong Hashtype', -1)

        self.checkButton.clicked.connect(self.checkButton_OnClick)

    def checkButtonDialogue(self, message, checkResult=0):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Result')
        if checkResult is 0:
            msgBox.setIconPixmap(self.matchedIcon)
        else:
            msgBox.setIconPixmap(self.errorIcon)
        msgBox.setWindowIcon(QIcon(':icon/icon.png'))
        msgBox.setText(str(message))
        msgBox.exec_()

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
        self.openFileButton.setText('Click to open a file')
        self.textBoxMD5.setText("")
        self.textBoxSHA256.setText("")
        self.textBoxSHA512.setText("")
        self.labelDoneMD5.setText(" ")
        self.labelDoneSHA256.setText(" ")
        self.labelDoneSHA512.setText(" ")
        self.labelFile.setPixmap(QPixmap(appFolder + 'icons/folder_open.png'))
        self.removeFileButton.clicked.connect(self.removeFileButton_OnClick)


class Hashing(QThread):
    # Hash Calculation Background Process
    signalMD5 = pyqtSignal(str)
    signalSHA256 = pyqtSignal(str)
    signalSHA512 = pyqtSignal(str)
    signalStopLoading = pyqtSignal(str)

    def run(self):
        with open('temp486.temp', 'r') as temp:
            fileLoc = temp.read()
        os.remove('temp486.temp')
        # Calculating MD5sum
        self.signalMD5.emit(checkHash(fileLoc, 'md5'))
        self.signalStopLoading.emit('stop_MD5')
        # Calculating SHA256sum
        self.signalSHA256.emit(checkHash(fileLoc, 'sha256'))
        self.signalStopLoading.emit('stop_SHA256')
        # Calculating SHA512sum
        self.signalSHA512.emit(checkHash(fileLoc, 'sha512'))
        self.signalStopLoading.emit('stop_SHA512')


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    try:
        mainWindow.openWith(sys.argv[1])
    except IndexError:
        pass
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
