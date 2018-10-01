#! /usr/bin/env python3

import socket, sys, re, os
sys.path.append("../lib")
import params

current_dir = os.getcwd() + '/server/'

switchesVarDefaults = (
        (('-l', '--listenPort') ,'listenPort', 50011),
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
    if not os.fork():
        while True:
            try:
                data = conn.recv(100).decode()
                if data[-3:] == "EOF":
                    output_file.write(data[0:-3])
                    conn.send("File read. Closing connection. EOF".encode())
                    output_file.close()
                    conn.close()
                    sys.exit(0)
                conn.sendall(data.encode())
                if data.startswith('PUT'):
                    data = data.split()
                    header['type'] = data[0]
                    header['url'] = current_dir + data[1]
                    if not os.path.exists(data[1]):
                        open(data[1], 'w+').close()
                    else:
                        conn.send("Closing connection. File exists in server. EOF".encode())
                        conn.close()
                        sys.exit(0)
                    output_file = open(data[1], 'a')
                    data = ' '.join(data[2::])
                    output_file.write(data)
                else:
                    output_file.write(data)
            except:
                continue
