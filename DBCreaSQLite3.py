#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

db=sqlite3.connect('/home/pi/nooxs/nooxsense.db')
cursor=db.cursor()

try:
    print "dispositivos"
    iOp= raw_input("Crear (S)i - (N)o ?")
    if iOp == "s" or iOp == "S":
        sSQL='CREATE TABLE dispositivos (cod_dispositivo int NOT NULL , nom_dispositivo varchar(30), MAC_dispositivo varchar(17), IP_dispositivo varchar(15), clave_dispositivo varchar(30), activo int, PRIMARY KEY (cod_dispositivo));'
        cursor.execute(sSQL)
    print "pin"
    iOp= raw_input("Crear (S)i - (N)o ?")
    if iOp == "s" or iOp == "S":
        sSQL='CREATE TABLE pin (cod_dispositivo int NOT NULL , PIN_num varchar(2) NOT NULL, PIN_nombre varchar(30), PIN_tipo varchar(1), PIN_valor_desde int, PIN_valor_hasta int, activo int, fechahora_actualizacion datetime, valor_actual int, PRIMARY KEY (cod_dispositivo, PIN_num));'
        cursor.execute(sSQL)
    print "configuracion"
    iOp= raw_input("Crear (S)i - (N)o ?")
    if iOp == "s" or iOp == "S":
        sSQL='CREATE TABLE configuracion (cod_parametro int NOT NULL , nom_parametro varchar(2), valor_parametro varchar(30), notas_parametro varchar(30), PRIMARY KEY (cod_parametro));'
        cursor.execute(sSQL)
    print "errorlog"
    iOp= raw_input("Crear (S)i - (N)o ?")
    if iOp == "s" or iOp == "S":
        sSQL='CREATE TABLE errorlog (MAC_dispositivo varchar(30) NOT NULL , IP_dispositivo varchar(15), error varchar(50), fechahora datetime);'
        cursor.execute(sSQL)
    print "registroinstantaneo"
    iOp= raw_input("Crear (S)i - (N)o ?")
    if iOp == "s" or iOp == "S":
        sSQL='CREATE TABLE registroinstantaneo (cod_dispositivo varchar(17) NOT NULL , fechahora datetime, PIN_num varchar(2), PIN_valor int);'
        cursor.execute(sSQL)
    print "registropermanente"
    iOp= raw_input("Crear (S)i - (N)o ?")
    if iOp == "s" or iOp == "S":
        sSQL='CREATE TABLE registropermanente (cod_dispositivo varchar(17) NOT NULL, PIN_num varchar(2), mediayear int, media01 int, media02 int, media03 int, media04 int, media05 int, media06 int, media07 int, media08 int, media09 int, media10 int, media11 int, media12 int);'
        cursor.execute(sSQL)

except db.Error, e:
        print "Error %s" % e.args[0]
        sys.exit(1)
finally:
        if db:
            db.commit()
            db.close()