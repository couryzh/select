#!/usr/bin/env python
# -*- coding: utf-8 -*-
# use select 
# zhpp Fri May 20 01:12:58 CST 2016

import os
import socket
import select

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(False)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 8888))

s.listen(10)

rlist = [s]
xlist = [s]
closed = []
while True:
    ready_rl, ready_wl, ready_xl = select.select(rlist, [], xlist)
    for sock in ready_rl:
        if sock is s:
            sock, addr = s.accept()
            sock.setblocking(False)
            rlist.append(sock)
        else:
            data = sock.recv(1024)
            if data == '' or data == 'exit':
                closed.append(sock)
            else:
                sock.send(data)
    for sock in ready_xl:
        print '%s:%s error occur' % sock.getpeername()
        closed.append(sock)
    for cs in closed:
        try:
            rlist.remove(cs)
            xlist.remove(cs)
        except ValueError:
            pass
        
        cs.close()

    closed = []
    if len(rlist) == 0:
        break
