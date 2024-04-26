import socketio
from ECC import curve, Point
from abe_utils import *
from hashlib import sha256
from aa1 import user_init
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
import time

class Usk:
    p_secret = curve.generatePrivateKey()
    def __init__(self):
        self.list = ['doctor', 'nurse', 'engineers', 'greece', 'america']
        
        self.usk_2=[]

h=0
        
usk_class = Usk()

def value_of_usk(index):
    return {'usk_2':usk_class.usk_2[index],'h_name':h}

def userSecret(data):
    global h
    h=data['h_name']
    for i in range(0,len(data['usk'])):
        usk_class.usk_2.append(data['usk'][i]+usk_class.p_secret)
    #print("usk2':",usk_class.usk_2)

def decrypt_DU_final(data):
    c0=data['c0']
    n1=data['n1']
    n2=data['n2']
    ct=data['ct']
    ct_h=data['ct_h']
    q_do=data['q_do']
    #print('c0:',c0)
    #print('n1:',n1)
    #print('n1+n2*p_secret:',n1 + usk_class.p_secret*n2)
    
    ck_2=c0-n1-usk_class.p_secret*n2
    #print('ck:',ck_2)
    #print('ck:',point_to_msg(ck_2))
    # print(time.time())
    

        
    h = int.from_bytes(sha256(ct.encode('utf-8')).digest(), 'big')
    check=h*q_do
    #print('check:',check)
    #print('ct_h:',ct_h)
    if(ct_h==check):
        print('success')
    else:
        print('Fail')
        
    key_string=point_to_msg(ck_2)
    # Convert the key string to bytes
    key_bytes = key_string.encode()

    # Use PBKDF2-HMAC to derive a 32-byte key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"",
        iterations=100000,
    )
    key = urlsafe_b64encode(kdf.derive(key_bytes))

    # Create the Fernet object
    # cipher = Fernet(key)

    # pt_byte_value=cipher.decrypt(ct)
    # pt = str(pt_byte_value, encoding="utf-8")
    # print("Msg(pt) after decryption: ",pt) 

    