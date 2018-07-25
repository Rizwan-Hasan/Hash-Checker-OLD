#!/usr/bin/env python3


def checkHash(fileLoc, option):
    # Hash calculator
    import hashlib
    with open(fileLoc, 'rb') as file:
        fileData = file.read()
    if(option == 'md5'):
        return hashlib.md5(fileData).hexdigest()
    elif(option == 'sha256'):
        return hashlib.sha256(fileData).hexdigest()
    elif(option == 'sha512'):
        return hashlib.sha512(fileData).hexdigest()
    else:
        return -1


if __name__ == '__main__':
    print('Hello World')
