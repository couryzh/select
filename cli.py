#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket

def socket_cli():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect(('127.0.0.1', 8888))

    print s.recv(1024)

    while True:
        data = sys.stdin.readline()
        if data == '':
            break
        s.send(data)
        rs = s.recv(1024)
        sys.stdout.write(rs)
    s.send('exit')
    s.close()
    
socket_cli()

