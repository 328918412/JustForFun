#!/usr/env python3
import re
ip_list =[]

def compare(var):
    ips = var.split('-')
    fip,lip = ips
    ips0 = fip.split('.')
    ips1 = lip.split('.')
    if ips0[2] == ips1[2]:
        ip_list.append(var)
    else:
        for i in range(int(ips0[2]),int(ips1[2])+1):
            if i == int(ips0[2]):
                ip_list.append(ips0[0]+'.'+ips0[1]+'.'+str(i)+'.'+ips0[3]+'-'+ips0[0]+'.'+ips0[1]+'.'+str(i)+'.'+'254\n')
            elif i == int(ips1[2]):
                ip_list.append(ips0[0]+'.'+ips0[1]+'.'+str(i)+'.'+'1'+'-'+ips0[0]+'.'+ips0[1]+'.'+str(i)+'.'+ips1[3])
            else:
                ip_list.append(ips0[0]+'.'+ips0[1]+'.'+str(i)+'.0/24\n')

def handleIp(line):
    if '-' in line:
        compare(line)
    else:
        ip_list.append(line)
    with open('ip_result.txt','w') as result:
        print(ip_list)
        result.writelines(ip_list)


with open('ip_origin.txt','r') as f:
    for line in f.readlines():
        handleIp(line)

