from mainController.ruckusApi import Ruckus

ip_address = '10.10.152.66'
# user = 'super'
# password = 'n3tw0rks.'

users = ['n1mbu5','super']
passwords = ['sp-admin','n3tw0rks.','N3tw0rks.','N3tw0rks','n3tw0rks']

for user in users:
    for x, password in enumerate(passwords):
        device = Ruckus (ip_address, user, passwords[x])
        if device.status == 1:
            print('user: ',user, '  password: ',passwords[x])
            break


# users = ['pedro','juan','pablo']
# passwords = ['123','456','789']
# for user in users:
#     for y, password in enumerate(passwords):
#         print(user,' ',passwords[y])