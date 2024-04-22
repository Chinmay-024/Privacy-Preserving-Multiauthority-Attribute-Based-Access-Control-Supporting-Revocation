from ECC import curve, Point
from hashlib import sha256
from abe_utils import verify2
from DO import encrypt_DO
from AA import user_init

class Key:
    __slots__ = 'master_key', 'public_key'
    pass


class Attribute:
    def __init__(self):
        self.list = ['doctor', 'nurse', 'engineers', 'greece', 'america']
        self.domain_list = [['doctor', 'nurse'],['engineers', 'greece', 'america']]
        self.public_key = []
        self.usk_2=[]
        self.k = []
        self.y = []

key = Key()
attribute = Attribute()
users = {}
sids = {}
no_of_aa = 2
k_val = attribute.k

def user_attribute_index(attr):
    with open('user_attr_lists.txt', 'r') as file:
        file.readline()
        list1_read = []
        for line in file:
            if line.strip() == '':
                break
            list1_read.append(line.strip())
    return list1_read.index(attr)


def value_of_y_and_k(attr):
    index = attribute.list.index(attr)
    with open('lists.txt', 'r') as file:
        file.readline()
        list1_read = []
        for line in file:
            if line.strip() == '':
                break 
            list1_read.append(int(line.strip()))
    
        file.readline()  
        list2_read = []
        for line in file:
            if line.strip() == '':
                break
            list2_read.append(int(line.strip()))
    return {'y':list1_read[index],'k':list2_read[index]}

def setup():
    global attribute
    for i in range(0,len(attribute.list)):
        k = curve.generatePrivateKey()
        y = curve.generatePrivateKey()        
        attribute.k.append(k)        
        attribute.y.append(y)
        attribute.public_key.append(curve.generatePublicKey(k).compress())
        attribute.public_key.append(curve.generatePublicKey(y).compress())
    #print("## SETUP: ",attribute.public_key)
    with open('lists.txt', 'w') as file:
    # Write the first list
        file.write('List 1:\n')
        for item in attribute.y:
            file.write(str(item) + '\n')
    
    # Write the second list
        file.write('\nList 2:\n')
        for item in attribute.k:
            file.write(str(item) + '\n') 
    init()
    encrypt_DO({'pk_k':attribute.k,'pk_y':attribute.y})

def init():
    name = input("name = ")
    attributes_str = input("attr = ")
    dynamic_attr = input("Dynamic attr = ")
    attributes = attributes_str.split(' ')
    with open('user_attr_lists.txt', 'w') as file:
        file.write('List 1:\n')
        for item in attributes:
            file.write(str(item) + '\n')
    
    with open('user_dynamic_attr_lists.txt', 'w') as file:
        file.write('dynamic_attr:\n')
        file.write(str(dynamic_attr) + '\n')
    # perform the operation for all attribute authorities
    for i in range(0, no_of_aa):
        flag=False
        attr_index = []
        for j in range(0, len(attribute.list)):
            attr_index.append(False)
        for attr in attributes:
            if attr in attribute.domain_list[i]:
                flag=True
                attr_index[attribute.list.index(attr)] = True
        if flag:
            user_init({'name': name, 'attributes': attr_index,"attr_list_index":i})


if __name__ == '__main__':
    setup()