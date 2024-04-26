from ECC import curve, Point
from hashlib import sha256
from abe_utils import verify2

# issuing and revoking users' attributes
# map GID to attribute list
# attr_list = ['doctor', 'nurse', 'engineers', 'greece', 'america']
# domain_list = [['doctor', 'nurse'],['engineers', 'greece', 'america']]
attr_list = []
domain_list = []
def user_init(data, list1, list2):
    from DU import userSecret
    from attribute_authority import value_of_y_and_k
    attr_list = list1
    domain_list = list2
    name = data["name"]
    attr_list_index=data["attr_list_index"]
    #print(f"A user {name} wants to get attribute about ", end='')
    attributes = data["attributes"]
    # for i, _attribute in enumerate(attributes):
    #     if _attribute:
    #         #print(attr_list[i], end=' ')

    h = int.from_bytes(sha256(name.encode('utf-8')).digest(), 'big')
    #print("Hash h in aa of name:",h)
    u_sk=[]
    for i, _attribute in enumerate(attributes):
        if not _attribute:
            continue
        attribute = attr_list[i]
        #print("for aa: ",attr_list_index," attribute: ",attribute)
        y_and_k = value_of_y_and_k(attribute)
        u_sk.append(y_and_k['y']+h*y_and_k['k'])
    #print('usk:',u_sk)
    userSecret({'usk': u_sk,'h_name':h})
    