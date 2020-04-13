import socket
import utils
import sys
import os


# try:
#     listener = utils.start_listener(54123,3600)
# except socket.error:
#     print '[!!] Listener Broken'
#     pass
# Get Remote Host
if len(sys.argv) >=2:
    remote = sys.argv[2]
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((remote, 32145))
    client.send('Can you hear me??')
    print client.recv(1024)
except socket.error:
    pass
