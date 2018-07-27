#!/usr/bin/env python3


def checkHash(fileLoc, option):

    # Hash calculator
    from hashlib import md5, sha256, sha512

    # Specifing how many bytes of the file to open at a time
    BLOCKSIZE = 128000
    # 128000 Byte = 128 KiloByte


    # Variables
    md5Hasher = md5()
    sha256Hasher = sha256()
    sha512Hasher = sha512()

    with open(fileLoc, 'rb') as file:
        fileData = file.read(BLOCKSIZE)

        # Conditions for desired hashing

        if(option == 'md5'): # MD5sum
            while(len(fileData) > 0):
                md5Hasher.update(fileData)
                fileData = file.read(BLOCKSIZE)
            return md5Hasher.hexdigest()

        elif(option == 'sha256'): # SHA256sum
            while(len(fileData) > 0):
                sha256Hasher.update(fileData)
                fileData = file.read(BLOCKSIZE)
            return sha256Hasher.hexdigest()

        elif(option == 'sha512'): # SHA512sum
            while(len(fileData) > 0):
                sha512Hasher.update(fileData)
                fileData = file.read(BLOCKSIZE)
            return sha512Hasher.hexdigest()

        else:
            return -1



if __name__ == '__main__':
    print('Hello World')