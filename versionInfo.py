import os
import platform

# Hash Checker Software Version ↓

version = 'Version: 2.1'

if (platform.system() == 'Windows'):
    Software_Version = """
        <font style="font-size: 8pt;
                     font-weight: 496;
                     color: #3e3e3e;">
            <b>""" + version + """</b>
        <font>
    """
else:
    Software_Version = """
        <font style="font-size: 10pt;
                     font-weight: 496;
                     color: #3e3e3e;">
            <b>""" + version + """</b>
        <font>
    """

if __name__ == '__main__':
    print(version)
