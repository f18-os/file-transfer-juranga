#! /usr/bin/env python3

import socket, sys, re, os
sys.path.append("../lib")
import params

current_dir = os.getcwd() + '/server/'
if not os.path.exists(current_dir):
    os.makedirs(current_dir)

switchesVarDefaults = (
        (('-l', '--listenPort') ,'listenPort', 50001),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

paramMap = params.parseParams(switchesVarDefaults)
listenPort = paramMap['listenPort']
listenAddr = ''

if paramMap['usage']:
    params.usage()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((listenAddr, listenPort))
server.listen(2)
print('Server now listening on port: {}'.format(listenPort))

output_file = None
while True:
    conn, addr = server.accept()
    print('Connection established with: {}'.format(addr))
    if not os.fork():
        header = {
            "type": "",
            "url": ""
        }
        try:
            while True:
                data = conn.recv(100).decode()
                if data == "":
                    continue
                if data == "EOF":
                    conn.send("File read. Closing connection. EOF".encode())
                    output_file.close()
                    print('File read. Connection with: {} has now been closed'.format(addr))
                    conn.close()
                    break
                if data.startswith('PUT'):
                    data_copy = data
                    data = data.split()
                    header['type'] = data[0]
                    header['url'] = current_dir + data[1]
                    if not os.path.exists(header['url']):
                        open(header['url'], 'w+').close()
                        output_file = open(header['url'], 'a')
                    else:
                        output_file = open(header['url'], 'w+')
                    conn.send(data_copy.encode())
                else:
                    if header['type'] == "PUT":
                        output_file.write(data)
                    conn.send(data.encode())
        except:
            print('Something went wrong! Connection with client has been lost.')
            conn.send("EOF".encode())
            conn.close()
            sys.exit(1)
            break

server.close()
