#!/usr/bin/env python
# -*- coding: utf-8 -*-
# use select 
# zhpp Fri May 20 01:12:58 CST 2016
# FIXME: cann't use yet

import os
import socket
import select


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setblocking(False)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 8888))

s.listen(10)

rlist = [s]
wlist = []
xlist = []
closed = []
wbuf = {}
sock_addr = {}
while True:
    ready_rl, ready_wl, ready_xl = select.select(rlist, wlist, xlist)
    for sock in ready_rl:
        if sock is s:
            sock, addr = s.accept()
            sock.setblocking(False)
            sock_addr[sock] = addr
            rlist.append(sock)
        else:
            data = sock.recv(1024)
            if data == '' or data == 'exit':
                closed.append(sock)
            else:
                addr = sock_addr[sock]
            wbuf['%s:%s' % addr] = data.upper()
    for sock in ready_wl:
        addr = sock_addr[sock]
        data = wbuf.pop('%s:%s' % addr)
        sock.send(data)
    for sock in ready_xl:
        addr = sock_addr[sock]
        print '%s:%s error occur' % addr 
        closed.append(sock)
    for s in closed:
        try:
            rlist.remove(s)
            wlist.remove(s)
            xlist.remove(s)
        except ValueError:
            pass
        
    closed = []
    if len(rlist) == 0:
        break
