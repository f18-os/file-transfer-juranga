#! /usr/bin/env python3

import socket, sys, re, os
sys.path.append("../lib")
import params

current_dir = os.getcwd() + '/server/'
if not os.path.exists(current_dir):
    os.makedirs(current_dir)

switchesVarDefaults = (
        (('-l', '--listenPort') ,'listenPort', 50016),
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

header = {
    "type": "",
    "url": "",
    "data": ""
}
output_file = None
while True:
    conn, addr = server.accept()
    x = 1
    if not x == 2:
        while True:
            while True:
                data = conn.recv(100).decode()
                if data == "":
                    continue
                if data[-3:] == "EOF":
                    output_file.write(data[0:-3])
                    conn.send("File read. Closing connection. EOF".encode())
                    output_file.close()
                    conn.close()
                    sys.exit(0)
                if data.startswith('PUT'):
                    dc = data
                    data = data.split()
                    header['type'] = data[0]
                    header['url'] = current_dir + data[1]
                    if not os.path.exists(header['url']):
                        open(header['url'], 'w+').close()
                    else:
                        conn.send("Closing connection. File exists in server. EOF".encode())
                        conn.close()
                        sys.exit(0)
                    output_file = open(header['url'], 'a')
                    conn.send(dc.encode())
                else:
                    output_file.write(data)
                    print("Should be sending data: ", data)
                    conn.send(data.encode())
server.close()
