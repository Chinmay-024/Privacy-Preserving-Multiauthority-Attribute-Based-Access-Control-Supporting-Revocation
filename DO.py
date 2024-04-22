from ECC import curve, Point
from hashlib import sha256
import socketio
from ECC import curve, Point
from abe_utils import *
from DUA import decrypt_dua
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from CSP import re_encrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets
from DOA import generate_B
from base64 import urlsafe_b64encode
from utils import bytes_from_matrix

attr_list = ['doctor', 'nurse', 'engineers', 'greece', 'america']
name = ""
attr_index = []


class Key:
    __slots__ = 'private_key','public_key'
    pass


do_key = Key()

A=[]

# Choose a large prime number (p) and a generator (g)
p = 67867967
# Generate a private key (a)
a = secrets.randbelow(p-1) + 1
g = 53


def encrypt_DO(data):
    global A
    from CA import value_of_y_and_k
    #step1
    ck = Fernet.generate_key()
    cipher = Fernet(ck)
    #print('ck:',ck)

    #step4
    access_condition = input("Type condition(and, or): ")
    dynamic_list = input("Type Dynamic Attr list(seperated by ,): ")
    dynamic_list2= msg_tp_point(dynamic_list)
    msg = input("msg: ")
    conditions = access_condition.split(' ')
    postfix = make_postfix(conditions)
    root = make_tree(postfix)
    A, p = levelorder(root)
    #print("A:",A)
    #print('p:',p)

    #step5
    l = len(A[0])
    s = curve.generatePrivateKey()
    #print('s:',s)
    lamb = []
    ome = []
    sigma1=[]
    sigma2=[]

    #step6
    v = [s]
    u = [0]
    w1=[dynamic_list2.x]
    w2=[dynamic_list2.y]
    for j in range(1, l):
        v.append(curve.generatePrivateKey())
        u.append(curve.generatePrivateKey())
        w1.append(curve.generatePrivateKey())
        w2.append(curve.generatePrivateKey())
    for a in A:
        lamb.append(vector_mult(v, a))
        ome.append(vector_mult(u, a))
        sigma1.append(vector_mult(w1, a))
        sigma2.append(vector_mult(w2, a))

    #print('lamb:',lamb)
    #print('ome:',ome)
    #print('sigma1:',sigma1)
    #print('sigma2:',sigma2)
    
    #step7
    #print('ck:',ck)
    ck_m = msg_tp_point(ck.decode('utf-8'))
    a=s*curve.G
    c0 = ck_m+a
    ck_m=c0-a
    
    key_string=point_to_msg(ck_m)
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
    # fernet = Fernet(key)
    cipher = Fernet(key)

    pt_bytes_value = bytes(msg, encoding="utf-8")
    ct = cipher.encrypt(pt_bytes_value)
    #print('ct:',ct)

    # #step3    
    do_key.private_key=curve.generatePrivateKey()
    do_key.public_key = curve.generatePublicKey(do_key.private_key)
    ct_h=int.from_bytes(sha256(ct).digest(), 'big')*do_key.private_key*curve.G
    #print("New ck_m:",point_to_msg(ck_m))
    c1 = []
    c2 = []
    for lam, om, attr in zip(lamb, ome,p):
        y_and_k=value_of_y_and_k(attr)
        c1.append((lam * curve.G + y_and_k['y'] * curve.G))
        c2.append((om * curve.G + y_and_k['k'] * curve.G))
        
    #print('c0:',c0)
    #print('c1:',c1)
    #print('c2:',c2)
    #print('ct:',ct)
    #print('ct_h:',ct_h)
    #print('A:',A)
    
    #step8
    generate_A()
    generate_B()    
    encrypt(A)
    re_encrypt({'q_do':do_key.public_key,'c0':c0, 'c1':c1, 'c2':c2, 'ct':ct,'ct_h':ct_h,'lamb':lamb,'ome':ome,'sigma1':sigma1,'sigma2':sigma2,'A':A,'p':p})


def generate_A ():
    global a,p,g
    # Calculate the public key (A)
    A = pow(g, a, p)

    # Write the public key (A) to a file
    with open('public_key_a.txt', 'w') as f:
        f.write(str(A))

def encrypt (data):
    global a,p
    # Read the public key (B) from the file
    with open('public_key_b.txt', 'r') as f:
        B = int(f.read())

    # Calculate the shared secret key (k)
    k = pow(B, a, p)

    #print("Shared secret key (k):", k)

    # Use the shared key (k) and the Fernet key for encryption/decryption
    key_string=str(k)
    key_bytes = key_string.encode()

    # Use PBKDF2-HMAC to derive a 32-byte key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"",
        iterations=100000,
    )
    key = urlsafe_b64encode(kdf.derive(key_bytes))
    #print('encrypt_key:',key)
    cipher = Fernet(key)
    #step2
    enc_data = cipher.encrypt(bytes_from_matrix(data))
    #print(enc_data)
    # Write the enc_data to a file
    with open('enc_data.txt', 'w') as f:
        f.write(enc_data.decode('utf-8'))
    return enc_data
    
