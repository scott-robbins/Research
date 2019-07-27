from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import base64
import utils
import sys
import os
# ## Encryption/Decryption Constants and Lambda Fcns ## #
BLOCK_SIZE = 16
PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING        # pad the text to be encrypted
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))            # encrypt with AES, encode with base64
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
# ################################################################### #

if '-search' in sys.argv:
    sys.argv.pop(0)
    if 3<len(sys.argv)<2:
        print '** Incorrect Search Format!! **'
        print 'Usage: python engine.py -search "cat pictures"'
    query = sys.argv[1]
