import os
import platform

# Operating System Temporary Directory ↓

if (platform.system() == 'Windows'):
    # tmpLoc = "C:\\users\\{}\\AppData\\Local\\Temp".format(os.getlogin())
    tmpLoc = "C:\\users\\" + os.getlogin() + "\\AppData\\Local\\Temp\\"  # Windows
else:
    tmpLoc = ''  # Linux


if __name__ == '__main__':
    print('Hello World')
