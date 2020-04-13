from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import socket
import base64
import time
import os

BLOCK_SIZE = 16     # the block size for the cipher object; must be 16 per FIPS-197
PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING        # pad text to be encrypted
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))            # encrypt with AES
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)


def create_timestamp():
    date = time.localtime(time.time())
    mo = str(date.tm_mon)
    day = str(date.tm_mday)
    yr = str(date.tm_year)

    hr = str(date.tm_hour)
    min = str(date.tm_min)
    sec = str(date.tm_sec)

    date = mo + '/' + day + '/' + yr
    timestamp = hr + ':' + min + ':' + sec
    return date, timestamp


def swap(file_name, destroy):
    data = []
    for line in open(file_name, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(file_name)
    return data


def cmd(shell):
    os.system('%s >> tmp.txt' % shell)
    return swap('tmp.txt', True)


def arr2str(arr):
    content = ''
    for e in arr:
        content += e + ' '
    return content


def arr2lines(arr):
    content = ''
    for line in arr:
        content += line + '\n'
    return content


def start_listener(port, timeout):
    started = False
    while not started:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print '[!!] Unable to create listener'
            time.sleep(timeout)
        try:
            s.bind(('0.0.0.0', port))
            s.listen(5)
            started = True
        except socket.error:
            print '[!!] Unable to create listener'
            s.close()
            time.sleep(timeout)
    return s


def get_nx_info():
    get_public = 'curl -s https://api.ipify.org'
    get_private = 'ifconfig | grep "inet " | grep broadcast | cut -d " " -f 10'
    get_iface = 'ifconfig | grep BROADCAST | grep RUNNING | cut -d ":" -f 1'
    public  = cmd(get_public).pop()
    private = cmd(get_private).pop()
    iface   = cmd(get_iface).pop()
    return public, private, iface


# ############################ NETWORKING FUNCTIONS ############################ #
def parse_ping(result):
    open('ping.txt', 'wb').write(result)
    routable = False
    ping_time = 0
    for line in swap('ping.txt', True):
        try:
            ping_time = float(line.split('time=')[1].split(' ')[0])
            routable = True
        except IndexError:
            pass
    return routable, ping_time

