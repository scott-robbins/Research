from Crypto.Random import get_random_bytes
import matplotlib.pyplot as plt
from Crypto.Cipher import AES
import scipy.misc as misc
import numpy as np
import base64
import sys
import os

# ## Encryption/Decryption Constants and Lambda Fcns ## #
BLOCK_SIZE = 16
PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING        # pad the text to be encrypted
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))            # encrypt with AES, encode with base64
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
# ################################################################### #


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(fname)
    return data


def str_build(arr):
    content = ''
    for element in arr:
        content += element
    return content


def spaced_str_build(arr):
    content = ''
    for line in arr:
        for element in line:
            content += element + ' '
    return content


def create_test_file(n_bytes):
    file_name = 'example.txt'
    if os.path.isfile(file_name):
        return True
    else:
        if os.name == 'posix':  # Cute trick for linux
            cmd = "python -c 'print "+'"\x68\x69"*'+str(int(round(n_bytes/2)))+"' >> "+file_name
            os.system(cmd)
        else:   # For Windows
            content = ''
            for slot in range(int(round(n_bytes/2))):
                content += '\x68\x69'
            open(file_name,'w').write(content)
        return True


def create_image(encrypted):
    """
    Create Image From Encrypted Data
    :param encrypted:
    :return:
    """
    code_points = []
    for value in encrypted:
        code_points.append(ord(value))
    data_in = np.array(code_points)
    N = int(np.ceil(np.sqrt(len(data_in.flatten()))))
    print '\033[3m* Using Block Size %d *\033[0m' % N
    if (N ** 2) - len(data_in) > 0:
        padding = (N ** 2) - len(data_in)
        for tile in range(padding):
            code_points.append(0)
        data_in = np.array(code_points)
    return data_in, N


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        Size = 1024
        if create_test_file(Size):
            print 'Test File Ready [%d Bytes]' % Size
            os.system('gzip -9 example.txt')
            raw_data = str_build(swap('example.txt.gz', False))

    elif '-e' in sys.argv:
        file_in = sys.argv[2]
        os.system('gzip -k -9 ' + file_in)
        raw_data = str_build(swap(file_in + '.gz', False))
        print 'Processing %d Word File \033[1m%s\033[0m' % (len(raw_data), file_in)

    key = base64.b64encode(get_random_bytes(16))
    cipher = AES.new(key)
    encrypted = EncodeAES(cipher, raw_data)
    open('example.encrypted', 'w').write(encrypted)
    print 'Created %d Byte Encrypted File Out' % len(encrypted)
    # TODO: Write Key to disk for DECRYPTION

    # Create Image from Encrypted Bytes
    N, data_in = create_image(encrypted)
    imat = data_in.reshape((N, N))

    print 'Min Value:  %d' % imat.min()
    print 'Max Value:  %d' % imat.max()
    print 'Mean Value: %d' % imat.mean()
    plt.imshow(imat, 'gray')
    plt.show()

    # TODO: CLEANUP
    os.remove('example.encrypted')
    if len(sys.argv) > 1:
        os.remove(file_in + '.gz')
# EOF
