from hashlib import sha256
from cryptography.fernet import Fernet
import socketio
from ECC import curve, Point
from abe_utils import *
from cryptography.fernet import InvalidToken
import json
from DUA import decrypt_dua
from utils import encode_data_to_json

def re_encrypt(data):
    ct_do = encode_data_to_json(data)
    ct_do_bytes_value = bytes(ct_do, encoding="utf-8")
    
    #step1
    csk = Fernet.generate_key()
    cipher = Fernet(csk)

    #step2
    ct_csp = cipher.encrypt(ct_do_bytes_value)

    #step3
    #print('ct_csp:',ct_csp)
    decrypt_dua({'ct_csp': ct_csp, 'csk':csk})
    
