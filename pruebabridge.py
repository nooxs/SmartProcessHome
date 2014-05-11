#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'juanfajardonavarro'

import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient

cliente = bridgeclient()

mensaje = cliente.get('Digital_8')
print mensaje
if mensaje == 1:
    nuevo = cliente.put("Digital_8","0")
elif mensaje == 0:
    nuevo = cliente.put("Digital_8","1")

mensaje = cliente.get("Digital_13")
print mensaje
if mensaje == 1:
    nuevo = cliente.put("Digital_13","0")
elif mensaje == 0:
    nuevo = cliente.put("Digital_13","1")
