#!/usr/bin/env python3

import select
import socket
import queue


# Create a socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setblocking(False)

server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_address = ('192.168.100.42',10001)
server.bind(server_address)
server.listen(10)
inputs = [server]
outputs = []
message_queues = {}
timeout = 20
while inputs:
    print('waiting for next event')
    readable,writable,exceptional = select.select(inputs,outputs,inputs,timeout)
    if not (readable or writable or exceptional):
        print('Time out!')
        break;
    for s in readable:
        if s is server:
            connection,client_address = s.accept()
            print("connection from client_address")
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                print(" received",data,"from",s.getpeername())
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                print("Closing",client_address)
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            print("",s.getpeername(),'queue empty')
            outputs.remove(s)
        else:
            print(" Sending ",next_msg," to ",s.getpeername())
            s.send(next_msg)
    for s in exceptional:
        print("Exception condition on ",s.getpeername())
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        c.close()
        del message_queues[s]
