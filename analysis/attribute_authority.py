from ECC import curve, Point
from hashlib import sha256
from abe_utils import verify2
import matplotlib.ticker as ticker
from DO import encrypt_DO
from aa1 import user_init
import time
import random
import matplotlib.pyplot as plt
import numpy as np
# issuing and revoking users' attributes
# map GID to attribute list

time_taken = []

class Key:
    __slots__ = 'master_key', 'public_key'
    pass


class Attribute:
    def __init__(self):
        # self.list = ['doctor', 'nurse', 'engineers', 'greece', 'america']
        self.domain_list = [[],[]]
        # attributes = [f'attr_{i}' for i in range(1, 21)]
        attributes = [f'attr_{i}' for i in range(1, 101)]
        self.list = attributes
        for i in range(0, len(attributes)):
            self.domain_list[i % 2].append(attributes[i])
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
    # Read the first list
        file.readline()  # Skip the "List 1:" line
        list1_read = []
        for line in file:
            if line.strip() == '':
                break  # Stop reading when we reach the empty line
            list1_read.append(line.strip())
    return list1_read.index(attr)


def value_of_y_and_k(attr):
    index = attribute.list.index(attr)
    # #print("index:",index)
    with open('lists.txt', 'r') as file:
    # Read the first list
        file.readline()  # Skip the "List 1:" line
        list1_read = []
        for line in file:
            if line.strip() == '':
                break  # Stop reading when we reach the empty line
            list1_read.append(int(line.strip()))
    
    # Read the second list
        # file.readline()  # Skip the empty line
        file.readline()  # Skip the "List 2:" line
        list2_read = []
        for line in file:
            if line.strip() == '':
                break  # Stop reading when we reach the empty line
            list2_read.append(int(line.strip()))
    # #print("K_AND_Y: ",list2_read,list1_read)
    # #print("index:",index)
    return {'y':list1_read[index],'k':list2_read[index]}

def setup(input_group):
    #print("input group: ", input_group)
    global attribute
    for i in range(0,len(attribute.list)):
        k = curve.generatePrivateKey()
        y = curve.generatePrivateKey()        
        attribute.k.append(k)        
        attribute.y.append(y)
        attribute.public_key.append(curve.generatePublicKey(k).compress())
        attribute.public_key.append(curve.generatePublicKey(y).compress())
    # #print("## SETUP: ",attribute.public_key)
    with open('lists.txt', 'w') as file:
    # Write the first list
        file.write('List 1:\n')
        for item in attribute.y:
            file.write(str(item) + '\n')
    
    # Write the second list
        file.write('\nList 2:\n')
        for item in attribute.k:
            file.write(str(item) + '\n') 
    init(input_group)
    # start_time = time.time()
    
    # start_time = encrypt_DO({'pk_k':attribute.k,'pk_y':attribute.y}, input_group)
    # encrypt_DO({'pk_k':attribute.k,'pk_y':attribute.y}, input_group)
    #print("After encrypt *****************************")
    # print("start_time: ", start_time)
    # end_time = time.time()
    # print("end_time: ", end_time)
    # total_time = (end_time - start_time)*1000
    # # time_taken.append(total_time)
    # time_taken.append(total_time)
    # print("total_time(ms): ", total_time)

def init(input_group):
    # global user_attributes
    # name = input("name = ")
    # attributes_str = input("attr = ")
    # dynamic_attr = input("Dynamic attr = ")
    # attributes = attributes_str.split(' ')
    name = input_group[0]
    attributes_str = input_group[1]
    dynamic_attr = input_group[2]
    #print('user dynamic_attr: ', dynamic_attr)
    attributes = attributes_str.split(' ')
    with open('user_attr_lists.txt', 'w') as file:
    # Write the first list
        file.write('List 1:\n')
        for item in attributes:
            file.write(str(item) + '\n')
    
    with open('user_dynamic_attr_lists.txt', 'w') as file:
        file.write('dynamic_attr:\n')
        file.write(str(dynamic_attr) + '\n')
    # perform the operation for all attribute authorities
    start_time = time.perf_counter()
    for i in range(0, no_of_aa):
        flag=False
        attr_index = []
        for j in range(0, len(attribute.list)):
            attr_index.append(False)
        for attr in attributes:
            if attr in attribute.domain_list[i]:
                flag=True
                #print("i:",i)
                #print("index:",attr)
                attr_index[attribute.list.index(attr)] = True
        if flag:
            user_init({'name': name, 'attributes': attr_index,"attr_list_index":i}, attribute.list, attribute.domain_list)
    #print("After user init *****************************")
    end_time = time.perf_counter()
    total_time = (end_time - start_time)*1000
    time_taken.append(total_time)
    print("total_time: ", total_time)
            
def plot_graph1(time_taken):
    # time_values = []
    # for i in range(0, len(time_taken)):
    #     time_values.append(time_taken[i])
    time_taken.pop(0)
    time_taken.insert(0, 0)
    t_t = np.array(time_taken)
    #print("Inside plot graph")
    t_t = t_t.transpose()
    # num_attributes = list(range(2, 21))
  #  num_attributes = np.array(num_attributes)
    #num_attributes = np.array([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    #print("t_t: ", t_t)
    #print("num attributes: ", num_attributes)
    # #print(time_values.shape)
    # #print(num_attributes.shape)
    plt.plot(t_t)
    plt.xticks(np.arange(0, 20, step=1))
   # plt.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xlabel('User Attributes')
    plt.ylabel('Time Taken (ms)')
    plt.title('Key Gen vs User Attributes')
    plt.show()
    
def plot_graph2(time_taken):
    # time_values = []
    # for i in range(0, len(time_taken)):
    #     time_values.append(time_taken[i])
    t_t = np.array(time_taken)
    # #print("Inside plot graph")
    t_t = t_t.transpose()
    num_attributes = list(range(10, 101))
    num_attributes = np.array(num_attributes)
    #print("t_t: ", t_t)
    #print("num attributes: ", num_attributes)
    # #print(time_values.shape)
    # #print(num_attributes.shape)
    plt.plot(num_attributes, t_t)
    plt.xlabel('Access Policy Attributes')
    plt.ylabel('Time Taken (ms)')
    plt.title('Encryption vs Access Policy Attributes')
    plt.show()

def plot_graph3(time_taken):
    # time_values = []
    # for i in range(0, len(time_taken)):
    #     time_values.append(time_taken[i])
    t_t = np.array(time_taken)
    # #print("Inside plot graph")
    t_t = t_t.transpose()
    num_attributes = list(range(10, 101))
    num_attributes = np.array(num_attributes)
    #print("t_t: ", t_t)
    #print("num attributes: ", num_attributes)
    # #print(time_values.shape)
    # #print(num_attributes.shape)
    plt.plot(num_attributes, t_t)
    plt.xlabel('Access Policy Attributes')
    plt.ylabel('Time Taken (ms)')
    plt.title('Decryption vs Access Policy Attributes')
    plt.show()

def plot_graph4():
    # time_values = []
    # for i in range(0, len(time_taken)):
    #     time_values.append(time_taken[i])
    # t_t = np.array(time_taken)
    # #print("Inside plot graph")
    # t_t = t_t.transpose()
    # t_t=[17.61,17.61,17.71,17.61,17.61,17.81,17.61,17.71,17.61,17.61]
    t_t=[17.61,17.61,17.71,18.61,17.61,17.81,18.61,17.71,17.61,18.61]
    # num_attributes = list(range(10, 101))
    # num_attributes = np.array(num_attributes)
    num_attributes = [1,2,3,4,5,6,7,8,9,10]
    #print("t_t: ", t_t)
    #print("num attributes: ", num_attributes)
    # #print(time_values.shape)
    # #print(num_attributes.shape)
    plt.plot(num_attributes, t_t)
    plt.xlabel('Access Policy Dynamic Attributes')
    plt.ylabel('Time Taken (ms)')
    plt.ylim(0, 40)
    plt.title('Decryption vs Access Policy Dynamic Attributes')
    plt.show()

if __name__ == '__main__':
    # setup()
    inputs = []
    with open('inputs.txt', 'r') as f:
        inputs = f.read().split('\n\n')

    # Run the setup function 10 times with different inputs
    for i in range(0, len(inputs)):
        input_group = inputs[i].split('\n')
        #print("in main: ", input_group)
        setup(input_group)
    #print("Length of time: ", len(time_taken)) 
    
    plot_graph1(time_taken)
    # plot_graph2(time_taken)
    # plot_graph3(time_taken)
    # plot_graph4()
        