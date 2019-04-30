#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import socket
messages = ['This is the message',
            'It will be sent',
            'in parts'
         ]
print("Connect to the server")
server_address = ("192.168.100.42",10001)

socks = []
for i in range(10):
    socks.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))

for s in socks:
    s.connect(server_address)

counter = 0

for message in messages:
    for s in socks:
        counter +=1
        print(" {} sending {} version {}".format(s.getpeername(),message,counter))
        msg = message+" version "+str(counter)
        s.send(msg.encode())
    for s in socks:
        data = s.recv(1024)
        print("{} received {}".format(s.getpeername(),data))
        if not data:
            print("Closing socket",s.getpeername())
            s.close()
