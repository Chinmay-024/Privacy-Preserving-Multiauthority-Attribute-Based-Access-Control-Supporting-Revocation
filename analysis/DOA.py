from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from abe_utils import point_to_msg
from cryptography.fernet import Fernet
import secrets
from ECC import curve, Point
import math
from utils import find_c, str_to_matrix,vector_multiplication

# Choose a large prime number (p) and a generator (g)
p = 67867967
g = 53
# Generate a private key (b)
b = secrets.randbelow(p-1) + 1

def generate_B ():
    global b,p,g
    # Calculate the public key (B)
    B = pow(g, b, p)

    # Write the public key (B) to a file
    with open('public_key_b.txt', 'w') as f:
        f.write(str(B))

    
def decrypt (encrypted_data):
    global b,p
    # Read the public key (A) from the file
    with open('public_key_a.txt', 'r') as f:
        A = int(f.read())

    # Calculate the shared secret key (k)
    k = pow(A, b, p)

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
    #print("decrypt_key:",key)
    cipher = Fernet(key)
    #step2
    #print("encrypted_data:",encrypted_data)
    dec_data = cipher.decrypt( bytes(encrypted_data, encoding="utf-8"))
    dec_data_2=str_to_matrix(dec_data.decode('utf-8'))
    #print("dec_data_2:",dec_data_2)
    return find_c(dec_data_2)

def calc_c():
    with open('enc_data.txt', 'r') as f:
        A= str(f.read())
    return decrypt(A)

def verify_dynamic_attr(sigma1,sigma2,c):
    result = vector_multiplication(sigma1,sigma2,c )
    l1= result['result1']
    l2= result['result2']
    #print("dynamic_attr l1,l2:",l1,l2)
    dynamic_attr2=Point((l1,l2),curve)
    dynamic_attr = point_to_msg(dynamic_attr2)
    #print("dynamic_attr after sending: ",dynamic_attr)
    dynamic_list = dynamic_attr.split(",")
    user_dynamic_attr2=[]
    with open('user_dynamic_attr_lists.txt', 'r') as file:
    # Read the first list
        file.readline()  # Skip the "List 1:" line
        for line in file:
            if line.strip() == '':
                break  # Stop reading when we reach the empty line
            user_dynamic_attr= line.strip()
    for attr in user_dynamic_attr.split(","):
        user_dynamic_attr2.append(attr)
    #print("user_dynamic_attr2:",user_dynamic_attr2)
    #print("dynamic_list:",dynamic_list)
    flag=True
    for attr in dynamic_list:
        if(attr in user_dynamic_attr2):
            flag=False
            break
    if flag:
        raise Exception("User Dynamic Attributes doesn't match with Dynamic Attribute list!!!! ")
            
    
    
    
