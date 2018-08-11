
''' All QThread classes are here '''

import os
import tmpdir
from HashChecker import checkHash
import PyQt5
from PyQt5.QtCore import pyqtSignal, QThread

# Hash Calculation Background Process Class ↓
class Hashing(QThread):

    signalMD5 = pyqtSignal(str)
    signalSHA256 = pyqtSignal(str)
    signalSHA512 = pyqtSignal(str)
    signalStopLoading = pyqtSignal(str)

    # Temporary Location Variable
    temp486 = tmpdir.tmpLoc + 'temp486.temp'

    def run(self):
        with open(self.temp486, 'r') as temp:
            fileLoc = temp.read()
        os.remove(self.temp486)
        # Calculating MD5sum ↓
        self.signalMD5.emit(checkHash(fileLoc, 'md5'))
        self.signalStopLoading.emit('stop_MD5')
        # Calculating SHA256sum ↓
        self.signalSHA256.emit(checkHash(fileLoc, 'sha256'))
        self.signalStopLoading.emit('stop_SHA256')
        # Calculating SHA512sum ↓
        self.signalSHA512.emit(checkHash(fileLoc, 'sha512'))
        self.signalStopLoading.emit('stop_SHA512')

# Start Application ↓
if __name__ == '__main__':
    print('Hello World')
