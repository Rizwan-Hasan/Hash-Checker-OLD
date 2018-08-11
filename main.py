#!/usr/bin/python3

import os
import sys
import time
import platform
import resources
import pyperclip
from functools import partial
import tmpdir
import filesMD5
import versionInfo
from threadClass import Hashing
from HashChecker import checkHash
from about import AboutWindow

# PyQt5 Imports
import PyQt5
from PyQt5 import uic, sip
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QPushButton
from PyQt5.QtWidgets import QFileDialog, QDesktopWidget, QTextEdit
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

# PyInstaller requirements
import packaging
from packaging import specifiers
from packaging import requirements


# Application root location ↓
appFolder = os.path.dirname(os.path.realpath(sys.argv[0])) + '/'

# Application's Main Window Class ↓
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Loading Main UI Design Files ↓
        if(checkHash(appFolder + 'ui/MainWindow.ui', 'md5') == filesMD5.MainWindow_ui):
            uic.loadUi(appFolder + 'ui/MainWindow.ui', self)
        else:
            sys.exit('MainWindow.ui file is corrupted')

        # Loading custom styleSheet ↓
        if(checkHash(appFolder + 'ui/default.css', 'md5') == filesMD5.default_css):
            self.loadStyleSheet()
        else:
            sys.exit('default.css file is corrupted')

        # Other UI Design Variables
        if(checkHash(appFolder + 'ui/AboutWindow.ui', 'md5') == filesMD5.AboutWindow_ui):
            self.aboutUiVar = AboutWindow()
        else:
            sys.exit('AboutWindow.ui file is corrupted')

        # Loaded File Location Variable ↓
        self.currentFileLoc = None

        # Temp Variable
        self.temp486 = tmpdir.tmpLoc + 'temp486.temp'

        # Icons Variables ↓
        self.icon = QIcon(':icon/icon.png')
        self.doneIcon = QPixmap(':/done/done.png')
        self.matchedIcon = QPixmap(':/matched/matched.png')
        self.errorIcon = QPixmap(':/error/error.png')
        self.loading = QMovie(':loading/loading.gif')
        self.loadingBall = QMovie(':loadingBall/loadingBall.gif')
        self.folderOpenIcon = QPixmap(':folder_open/folder_open.png')

        # Software Version Variable
        self.labelVersionString.setText(versionInfo.Software_Version)

        # Main UI Calling ↓
        self.hashCheckerUI()

    def makeWindowCenter(self):
        # For launching windows in center
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def hashCheckerUI(self):
        # Making window centered ↓
        self.makeWindowCenter()

        # Window customizing ↓
        self.setWindowTitle('Hash Checker')
        self.setWindowIcon(self.icon)

        # Enabling Drag and Drop
        self.setAcceptDrops(True)

        # A Status
        self.statusBar().showMessage('You can drag and drop a file, not multiple file')

        # Buttons actions ↓
        self.openFileButton.clicked.connect(self.openFileDialog)
        self.removeFileButton.clicked.connect(self.removeFileButton_OnClick)
        self.clearButton.clicked.connect(self.clearButton_OnClick)
        self.clipboardButton.clicked.connect(self.clipboardText)
        self.checkButton.clicked.connect(self.checkButton_OnClick)
        self.aboutButton.clicked.connect(self.aboutUI)

        # Clipboard Buttons actions ↓
        self.clipboardMD5Button.clicked.connect(partial(self.clipboardButtonActions_OnClick, 'md5'))
        self.clipboardSHA256Button.clicked.connect(partial(self.clipboardButtonActions_OnClick, 'sha256'))
        self.clipboardSHA512Button.clicked.connect(partial(self.clipboardButtonActions_OnClick, 'sha512'))

        # Adding Place Holder Text ↓
        self.textBoxMD5.setPlaceholderText('...')
        self.textBoxSHA256.setPlaceholderText('...')
        self.textBoxSHA512.setPlaceholderText('...')
        self.textBoxCheck.setPlaceholderText('Paste your hash here to match with or leave empty\nOnly MD5 or SHA256 or SHA512 is allowed')

    @pyqtSlot()  # Qt Framework's Slot Decorator

    def closeEvent(self, event):
        try:
            # Closing All Opened Window
            self.aboutUiVar.close()
        except AttributeError:
            pass

    # Custom Style Sheet ↓
    def loadStyleSheet(self):
        with open(appFolder + 'ui/default.css', 'r') as css:
            self.styleSheet = css.read()

        # Label font size customizing using CSS ↓
        self.labelMD5.setStyleSheet(self.styleSheet)
        self.labelSHA256.setStyleSheet(self.styleSheet)
        self.labelSHA512.setStyleSheet(self.styleSheet)
        self.labelHashBox.setStyleSheet(self.styleSheet)

        # Button customizing using CSS ↓
        self.aboutButton.setStyleSheet(self.styleSheet)

        # Textbox font size customizing using CSS ↓
        self.textBoxMD5.setStyleSheet(self.styleSheet)
        self.textBoxSHA256.setStyleSheet(self.styleSheet)
        self.textBoxSHA512.setStyleSheet(self.styleSheet)
        self.textBoxCheck.setStyleSheet(self.styleSheet)

    # Other User Interface Function ↓
    def aboutUI(self):
        # About Window
        try:
            self.aboutButton.clicked.disconnect()
        except:
            pass
        self.aboutUiVar.show()
        self.aboutButton.clicked.connect(self.aboutUI)

    # Drag and Drop Functions ↓
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().text():
            self.currentFileLoc = e.mimeData().text()
            if(platform.system() == 'Windows'):  # For Windows OS
                # Removing 'file:///' # Example: 'file:///Rizwan Hasan' -> 'Rizwan Hasan'
                self.currentFileLoc = self.currentFileLoc.replace('file:///', '')
                print(self.currentFileLoc)
            else:
                # Removing 'file://' # Example: 'file:///Rizwan Hasan' -> '/Rizwan Hasan'
                self.currentFileLoc = self.currentFileLoc.replace('file://', '')
                # Removing '\n' # Example: 'Rizwan Hasan\n' -> 'Rizwan Hasan'
                self.currentFileLoc = self.currentFileLoc[:len(self.currentFileLoc) - 2]
                # Replacing '%20' with ' ' # Example: 'Rizwan%20Hasan' -> 'Rizwan Hasan'
                self.currentFileLoc = self.currentFileLoc.replace('%20', ' ')
            self.labelFile.setPixmap(self.doneIcon)
            self.openFileButton.setText("'" + os.path.basename(self.currentFileLoc) + "' is loaded")
            with open(self.temp486, 'w') as temp:
                temp.write(self.currentFileLoc)
            self.start_Hash_Calculation()

    # Open With Function ↓
    def openWith(self, argFile):
        self.currentFileLoc = argFile
        self.labelFile.setPixmap(self.doneIcon)
        self.openFileButton.setText("'" + os.path.basename(self.currentFileLoc) + "' is loaded")
        with open(self.temp486, 'w') as temp:
            temp.write(self.currentFileLoc)
        self.start_Hash_Calculation()
        print(argFile)

    # Clipboard Buttons Action Functions ↓
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

    # Clipboard Text ↓
    def clipboardText(self):
        try:
            self.clipboardButton.clicked.disconnect()
        except:
            pass
        clipText = QApplication.clipboard().text()
        clipText = clipText.strip()
        self.textBoxCheck.setText(clipText)
        self.loadingBallAnimation('start')
        self.clipboardButton.clicked.connect(self.clipboardText)

    # Clear Button's Action ↓
    def clearButton_OnClick(self):
        self.loadingBallAnimation('stop')
        self.labelLoadingBall.clear()

    # Loading Ball Animation ↓
    def loadingBallAnimation(self, decider):
        self.loadingBall.setSpeed(150)
        self.labelLoadingBall.setMovie(self.loadingBall)
        if(decider == 'start'):
            self.loadingBall.start()
        elif(decider == 'stop'):
            self.loadingBall.stop()

    # Check Button's Action Function ↓
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

    # Check Buttons Action Dialogue ↓
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

    # File Dialogs ↓
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
            with open(self.temp486, 'w') as temp:
                temp.write(self.currentFileLoc)
            self.start_Hash_Calculation()
        self.openFileButton.clicked.connect(self.openFileDialog)

    # Buttons Actions Function ↓
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

    # Loading Circle Initialize ↓
    def loadingCircle(self, x):
        if(x == 'start'):
            self.loading.setSpeed(280)
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

    # Remove Button's Action Function ↓
    def removeFileButton_OnClick(self):
        try:
            self.removeFileButton.clicked.disconnect()
        except:
            pass
        self.currentFileLoc = None
        self.openFileButton.setText('Click to open a file')
        self.textBoxMD5.clear()
        self.textBoxSHA256.clear()
        self.textBoxSHA512.clear()
        self.textBoxCheck.clear()
        self.labelDoneMD5.clear()
        self.labelDoneSHA256.clear()
        self.labelDoneSHA512.clear()
        self.clearButton_OnClick()
        self.labelFile.setPixmap(self.folderOpenIcon)
        self.statusBar().showMessage('Cleared...')
        time.sleep(1.0)
        self.statusBar().showMessage('You can drag and drop a file, not multiple file')
        self.removeFileButton.clicked.connect(self.removeFileButton_OnClick)


# Main Function ↓
def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    try:
        mainWindow.openWith(sys.argv[1])
    except IndexError:
        pass
    mainWindow.show()
    sys.exit(app.exec_())


# Start Application ↓
if __name__ == '__main__':
    main()
