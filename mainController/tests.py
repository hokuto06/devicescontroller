from django.test import TestCase

# Create your tests here.
split_ip1 = '10.2.2.3'.split('.')
split_ip2 = '10.2.2.10'.split('.')


for i in range(int(split_ip1[3]), int(split_ip2[3])+1):
    print('.'.join(split_ip1[0:3])+'.'+str(i))
            

# print(ip1[3])