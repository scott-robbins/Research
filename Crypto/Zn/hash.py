from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from threading import Thread
import base64
import os

NODE_UID = base64.b64encode(get_random_bytes(16))
print NODE_UID

if os.path.isdir('Common'):
    local_resources = os.listdir('Common')
else:
    os.mkdir('Common')
    print '\033[3m* Shared [Synced] Folder Created\033[0m'
