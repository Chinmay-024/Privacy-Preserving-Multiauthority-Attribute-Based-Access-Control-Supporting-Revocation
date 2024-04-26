from ECC import curve, Point
from hashlib import sha256
from cryptography.fernet import Fernet
from abe_utils import *
import json
from cryptography.fernet import InvalidToken


class Attribute:
    def __init__(self):
        self.list = ['doctor', 'nurse', 'engineers', 'greece', 'america']
        self.list1 = ['doctor', 'nurse']
        self.list2 = ['engineers', 'greece', 'america']
        self.public_key = []
        self.usk_2=[]
        self.k = []
        self.y = []

def value_of_y_and_k(attr):
    if attr in attribute.list1:
        return {'y':attribute.y[0],'k':attribute.k[0]}
    else:
        return {'y':attribute.y[1],'k':attribute.k[1]}
    
def value_of_usk(attr):
    if attr in attribute.list1:
        return attribute.usk_2[0]
    else:
        return attribute.usk_2[1]
    
class Key:
    __slots__ = 'private_key','public_key'
    pass


do_key = Key()

attribute = Attribute()
users = {}
# sids = {}

# sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
# app = web.Application()
# sio.attach(app)



def setup():
    k = curve.generatePrivateKey()
    y = curve.generatePrivateKey()        
    attribute.k.append(k)        
    attribute.y.append(y)
    k = curve.generatePrivateKey()
    y = curve.generatePrivateKey()        
    attribute.k.append(k)        
    attribute.y.append(y)
    attribute.public_key.append(curve.generatePublicKey(k).compress())
    attribute.public_key.append(curve.generatePublicKey(y).compress())
    #print("## SETUP: ",attribute.public_key)
    #print("k:",k)
    #print("y:",y)
    init()
    encrypt_DO({'pk_k':attribute.k,'pk_y':attribute.y})
    
attr_list = ['doctor', 'nurse', 'engineers', 'greece', 'america']
name = ""
h=0
p_secret=0
attr_index = []


def init():
    global name, attr_index
    attributes_str = input("attr = ")
    attributes = attributes_str.split(' ')
    attr_index = []
    for i in range(0, len(attr_list)):
        attr_index.append(False)
    for attribute in attributes:
        attr_index[attr_list.index(attribute)] = True

    name = input("name = ")
    user_init({'name': name, 'attributes': attr_index})

def user_init(data):
    name = data["name"]
    #print(f"A user {name} wants to get attribute about ", end='')
    attributes = data["attributes"]
    for i, _attribute in enumerate(attributes):
        if _attribute:
            #print(attribute.list[i], end=' ')

    h = int.from_bytes(sha256(name.encode('utf-8')).digest(), 'big')
    u_sk=[attribute.y[0]+h*attribute.k[0],attribute.y[1]+h*attribute.k[1]]
    #print('usk:',u_sk)
    userSecret({'usk': u_sk,'pk_k':attribute.public_key[0],'pk_y':attribute.public_key[1],'h':h})

def userSecret(data):
    global p_secret
    p_secret = curve.generatePrivateKey()
    for i in range(0,len(data['usk'])):
        attribute.usk_2.append(data['usk'][i]+p_secret)
    #print("usk2':",attribute.usk_2)
    # serverSocket.emit('user_secret_dua', {'usk2':u_sk_2,'pk_k':data['pk_k'],'pk_y':data['pk_y'],'h':data['h'],'p':data['p']})
a=Point(None,None)

def encrypt_DO(data):
    global a
    
    #step1
    ck = Fernet.generate_key()
    cipher = Fernet(ck)
    #print('ck:',ck)

    # #step2
    pt=b"hi how are you"
    ct = cipher.encrypt(pt)
    #print('ct:',ct)

    # #step3    
    do_key.private_key=curve.generatePrivateKey()
    do_key.public_key = curve.generatePublicKey(do_key.private_key)
    ct_h=int.from_bytes(sha256(ct).digest(), 'big')*do_key.private_key*curve.G

    #step4
    access_condition = input("Type condition(and, or): ")
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

    #step6
    v = [s]
    u = [0]
    for j in range(1, l):
        v.append(curve.generatePrivateKey())
        u.append(curve.generatePrivateKey())
    for a in A:
        lamb.append(vector_mult(v, a))
        ome.append(vector_mult(u, a))

    #print('lamb:',lamb)
    #print('ome:',ome)
    #step7
    #print('ck:',ck)
    ck_m = msg_tp_point(ck.decode('utf-8'))
    #print('ck_decode:',ck.decode('utf-8'))
    
    #print(point_to_msg(ck_m))
    a=curve.generatePublicKey(s)
    #print('s*cruve.G:',a)
    
    #print('ck_m:',ck_m)
    c0 = ck_m+a
    #print('c0-sG:',c0-a)
    #print('a-a:',a-a)
    val=a-a
    #print('val:',val)
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
        
    decrypt_dua({'q_do': do_key.public_key,'c0': c0, 'c1': c1, 'c2': c2, 'ct':ct,'ct_h':ct_h,'lamb':lamb,'ome':ome,'A':A,'p':p})
    #step8
    # serverSocket.emit('decrypt_dua', {'q_do': do_key.public_key,'c0': c0.compress(), 'c1': c1, 'c2': c2, 'ct':ct,'ct_h':ct_h,'lamb':lamb,'ome':ome,'A':A})
    
# def re_encrypt(data):
#     ct_do=json.dumps(data)
#     #step1
#     csk = Fernet.generate_key()
#     cipher = Fernet(csk)

#     #step2
#     ct_csp = cipher.encrypt(ct_do)

#     # #step3
#     # serverSocket.emit('ct_do', {'ct_csp': ct_csp, 'csk':csk})
#     decrypt_dua({'ct_csp': ct_csp, 'csk':csk})
       
    
def decrypt_dua(data):
    # cipher = Fernet(data['csk'])
    # ct_do_2=cipher.decrypt(data['ct_do'])
    # ct_do = json.loads(ct_do_2)
    ct_do=data
    c0=data['c0']
    lamb=ct_do['lamb']
    ome=ct_do['ome']
    c1=ct_do['c1']
    c2=ct_do['c2']
    A=ct_do['A']
    c0=data['c0']
    p=data['p']
    c=[0]*len(A)
    for i in range (0,len(A[0])):
        c[0]=c[0]+A[0][i]
    c[0]=(int)(1/c[0])
    #print('c:',c)
    #print('A:',A)
    #print('lamb:',lamb)
    #print('ome:',ome)
        
    D=[]
    D1=[]    
    for i in range(0,len(A)):
        attr=p[i]
        usk_2=value_of_usk(attr)
        D.append(c1[i]-usk_2*curve.G+h*c2[i])
        D1.append(lamb[i]*curve.G+h*ome[i]*curve.G-p_secret*curve.G)
    
    #print('D:',D[0])
    #step5:
    n1=[]
    for i in range(0,len(c)):
        n1.append(c[i]*D[i])
    n2=[]
    for i in c:
        n2.append(i*curve.G)
        
    #print('n1:',n1)
    #print('n2:',n2)
    #print('n1+p_secret*n2:',n1[0]+p_secret*n2[0])
    #print('a:',a-(n1[0]+p_secret*n2[0])+c0)
    #print('c0-n1-p_secret*n2:',c0-n1[0]-p_secret*n2[0])
    
    #print('c:',c)
    decrypt_DU_final( {'q_do':data['q_do'],'c0':c0,'ct':ct_do['ct'],'ct_h':ct_do['ct_h'],'n1':n1,'n2':n2})
    # serverSocket.emit('encrypt_DU_final', {'q_do':data['q_do'],'c0':ct_do['c0'],'ct':ct_do['ct'],'ct_h':ct_do['ct_h'],'n1':n1,'n2':n2})

def decrypt_DU_final(data):
    c0=data['c0']
    n1=data['n1']
    n2=data['n2']
    ct=data['ct']
    ct_h=data['ct_h']
    q_do=data['q_do']
    #print('c0:',c0)
    #print('n1[0]:',n1[0])
    
    ck_2=c0-n1[0]-p_secret*n2[0]
    #print('ck:',ck_2)
    #print('ck:',point_to_msg(ck_2))
    

        
    h = int.from_bytes(sha256(ct).digest(), 'big')
    check=h*q_do
    #print('check:',check)
    #print('ct_h:',ct_h)
    if(ct_h==check):
        #print('success')
    else:
        #print('Fail')
    
    # x=point_to_msg(ck_2)
    # x2=bytes(x, 'utf-8')
    # #print('x2:',x2)
    # cipher = Fernet()
    # pt=cipher.decrypt(ct)
    # #print(pt)
    
    #print('ct_h-Point(None,None):',ct_h-Point(None,None))
    #print('ct_h+Point(None,None):',ct_h+Point(None,None))


if __name__ == '__main__':
    setup()