# D3.py - Message Encryption/Decryption Program
#
# Develop and test a Python program that reads messages contained in a text 
# file, and encodes the messages saved in a new file. For encoding messages, 
# a simple substitution key should be used as shown below,
#
#   (TABLE DELETED)
#
# Each letter in the left column is substituted with the corresponding 
# letter in the right column when encoding. Thus, to decode, the letters 
# are substituted the opposite way. Unencrypted message files will be simple 
# text files with file extension .txt. Encrypted message files will have the 
# same file name, but with file extension .enc. For each message encoded, a 
# new substitution key should be randomly generated and saved in a file with 
# the extension '.key'. Your program should also be able to decrypt messages 
# given a specific encoded message and the corresponding key.
#
# date:    02/21/2017
# author:  Chiayo Lin
# license: GPL 3.0

import sys, os
from math import sin
from random import randint

def getFile(prompt, flag):
    try:
        return open(input(prompt + ": "), flag)
    
    except IOError:
        sys.stderr.write("Error: file cannot be read.\n")
        sys.exit(os.EX_IOERR) # use Unix exit code

def crypto(text, vector, encryption = True):
    keyGen = lambda v: int(v * sin(v) + v)
    mode = encryption and +1 or -1
    inc = mode * 3
    
    # vector is off by one increment while deciphering
    vector += not encryption and inc
    
    result = str()
    for char in text[::mode]:
        if ord(char) in range(32, 127):
            ch_key = mode * keyGen(vector)
            result += chr((((ord(char) - 32) + ch_key) % 95) + 32)
            vector += inc

    return (result[::mode], vector)

def getVector(flag, k_file): 
    return flag and randint(0, 0xfffffff) or int(k_file.read(7), 16)

def D3():
    encrypt = input("Encyption (E) / Decryption (D): ").lower()[0] == 'e'
    
    i_file = getFile("Locate a file", 'r')
    o_file = open(i_file.name + (encrypt and ".enc" or ".txt"), 'w')
    k_file = open(i_file.name + (encrypt and ".enc.key" or ".key"), 
                                (encrypt and 'w' or 'r'))
    
    for line in i_file:
        vector = getVector(encrypt, k_file)
        result, vector = crypto(line, vector, encrypt)

        if encrypt:
            k_file.write(format(vector, '07x'))
        o_file.write(result + '\n')

    o_file.close()
    k_file.close()

    return

if __name__ == "__main__": D3()
