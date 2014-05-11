#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'juanfajardonavarro'

import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient

cliente = bridgeclient()

mensaje = cliente.get('D8')
print mensaje
if mensaje == 1:
    nuevo = cliente.put("D8",0)
elif mensaje == 0:
    nuevo = cliente.put("D8",1)

mensaje = cliente.get("D13")
print mensaje
if mensaje == 1:
    nuevo = cliente.put("D13",0)
elif mensaje == 0:
    nuevo = cliente.put("D13",1)
