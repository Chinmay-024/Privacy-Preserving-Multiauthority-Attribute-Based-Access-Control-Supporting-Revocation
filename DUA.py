from ECC import curve, Point
from abe_utils import *
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from hashlib import sha256
from DU import decrypt_DU_final,value_of_usk
from utils import decode_json_to_data,find_c
import json
from DOA import calc_c,verify_dynamic_attr

name = ""
attr_index = []
h_name = 0
def decrypt_dua(data):
    from CA import user_attribute_index
    global h_name
    cipher = Fernet(data['csk'])
    ct_do_2_byte_value=cipher.decrypt(data['ct_csp'])
    # ct_do = json.loads(ct_do_2)
    ct_do_2 = str(ct_do_2_byte_value, encoding="utf-8")
    ct_do = decode_json_to_data(ct_do_2)

    c0=ct_do['c0']
    lamb=ct_do['lamb']
    ome=ct_do['ome']
    sigma1=ct_do['sigma1']
    sigma2=ct_do['sigma2']
    c1=ct_do['c1']
    c2=ct_do['c2']
    A=ct_do['A']
    # c0=data['c0']
    p=ct_do['p']
    d=calc_c()
    c=[]
    for i in range(0,len(d)):
        c.append(round(d[i]))
    verify_dynamic_attr(sigma1,sigma2,c)
    #print('c:',c)
    #print('A:',A)
    #print('lamb:',lamb)
    #print('ome:',ome)
        
    D=[]
    
    # h = int.from_bytes(sha256(name.encode('utf-8')).digest(), 'big')
    for i in range(0,len(A)):
        # attr=p[i]
        usk_index=user_attribute_index(p[i])
        data_usk=value_of_usk(usk_index)
        usk_2=data_usk['usk_2']
        h_name=data_usk['h_name']
        D.append(c1[i]-usk_2*curve.G+h_name*c2[i])
    
    #print("Hash h in dua of name:",h_name)
    #print('D:',D[0])
    
    #step5:
    n1=Point((None,None),curve)
    for i in range(0,len(c)):
        n1+=(c[i]*D[i])
        
    n2=Point((None,None),curve)
    for i in c:
        n2+=(i*curve.G)
        
    decrypt_DU_final( {'q_do':ct_do['q_do'],'c0':c0,'ct':ct_do['ct'],'ct_h':ct_do['ct_h'],'n1':n1,'n2':n2})