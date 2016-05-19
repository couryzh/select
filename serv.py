#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os
import multiprocessing

def handle_conn(sock, cli_addr):
    print 'Connect from %s:%s' % (cli_addr)
    sock.send('Welcome, I am pid: %s' % os.getpid())
    while True:
        data = sock.recv(1024)
        if data == 'exit' or data == '':
            break
        sock.send(data.upper())
    print ' %s:%s closed' % (cli_addr)
        

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('127.0.0.1', 8888))

s.listen(1024)

while True:
    sock, addr = s.accept()
    p = multiprocessing.Process(target=handle_conn, args=(sock, addr))
    p.run()
