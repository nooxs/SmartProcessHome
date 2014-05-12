#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'juanfajardonavarro'

import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient

cliente = bridgeclient()

mensaje = str(cliente.get('D8'))
print "antes: "+mensaje
if mensaje == '1':
    nuevo = cliente.put('D8',0)
    print nuevo
    print "cambio a 0"
elif mensaje == '0':
    nuevo = cliente.put('D8',1)
    print nuevo
    print "cambio a 1"
print "ahora: "+str(cliente.get('D8'))
