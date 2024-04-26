from hashlib import sha256
from cryptography.fernet import Fernet
import socketio
from ECC import curve, Point
from abe_utils import *
from cryptography.fernet import InvalidToken
import json
from dua import decrypt_dua
from utils import encode_data_to_json
import time

def re_encrypt(data):
    ct_do = encode_data_to_json(data)

    # ct_do = str(data)
    ct_do_bytes_value = bytes(ct_do, encoding="utf-8")
    #step1
    csk = Fernet.generate_key()
    cipher = Fernet(csk)

    #step2
    ct_csp = cipher.encrypt(ct_do_bytes_value)

    # #step3
    # serverSocket.emit('ct_do', {'ct_csp': ct_csp, 'csk':csk})
    # #print('ct_csp:',ct_csp)
    # start_time = time.time()
    # decrypt_dua({'ct_csp': ct_csp, 'csk':csk})
    # return start_time
    
