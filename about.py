# About Window User Intarface

import sys
import os
import resources
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

# Application root location ↓
appFolder = os.path.dirname(os.path.realpath(sys.argv[0])) + '/'

class AboutWindow(QMainWindow):
    def __init__(self):
        super(AboutWindow, self).__init__()
        uic.loadUi(appFolder + 'ui/AboutWindow.ui', self)
        self.aboutIcon = QIcon(':about/about.png')
        self.aboutUI()

    def makeWindowCenter(self):
        from PyQt5.QtWidgets import QDesktopWidget
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def aboutUI(self):
        # Making Window centered
        self.makeWindowCenter()

        # Window customizing
        self.setWindowTitle('About')
        self.setWindowIcon(self.aboutIcon)


def main():
    import sys
    app = QApplication(sys.argv)
    aboutWindow = AboutWindow()
    aboutWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
