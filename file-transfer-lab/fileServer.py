#! /usr/bin/env python3

import socket, sys, re, os
sys.path.append("../lib")
import params

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

while True:
    conn, addr = s.accept()
    if not os.fork():
        try:
            header = {
                "type": "",
                "url": "",
                "data": data
            }
            data = server.recv(100).decode()
            data_len = len(data)
            output_file = None
            while data_len <= 100 and not data_len[:-3] == "EOF":
                if data.startswith('PUT'):
                    data = data.split()
                    header['type'] = data[0]
                    header['url'] = data[1]
                    if not os.path.exists(data[1]):
                        open(data[1], 'w+').close()
                        output_file = open(data[1], 'a')
                    else:
                        conn.send("Closing connection. File exists in server. EOF".encode())
                        conn.close()
                        sys.exit(0)
                    for i in range(2, len(data)):
                        output_file.write(data[3])
                else:
                    output_file.write(data)
            if data_len[:-3] == "EOF":
                output_file.write(data[0:-3])
                conn.send("File read. Closing connection. EOF".encode())
                conn.close()
                sys.exit(0)
            
