#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'juanfajardonavarro'

# Importación de módulos
import MySQLdb
import sqlite3
import os
import sys
import subprocess
import datetime
import time
from class_profiles import profilePython

# gestión de configuración
config = profilePython('/etc/config/nooxs.config')

# variables generales

###############################################################
# FUNCIONES ###################################################
###############################################################

###############################################################
# PRINCIPAL ###################################################
###############################################################
try:
    sHost = config.profile('MySQL','host')
    sUser = config.profile('MySQL','USER')
    sPass = config.profile('MySQL','PASS')
    sDB = config.profile('MySQL','DB')
    queDB = config.profile('DB', 'db')
    sArgDB = config.profile('DB','Argumentos')
    db=MySQLdb.connect(host=sHost,user=sUser,passwd=sPass,db=sDB)
    cursor=db.cursor()

    salir = False

    while not salir:
        os.system('clear')
        print 'NOOXS - SmartProcessHome'
        print '*** Sensores / Actuadores de la red ***'
        print "\033[1;33m- nota V1: solo para pines digitales, Output, Activos-\033[1;m"
        print
        print
        print '*******************************************************************************'
        print '|disp  | PIN |Nombre                         |         Valor Actual           |'
        print '|      |     |                               | fecha/Hora           | valor   |'
        print '*******+****+********************************+*****+****************+**********'
        sSQL='SELECT cod_dispositivo, PIN_num, PIN_nombre, fechahora_actualizacion, valor_actual FROM pin WHERE activo=1 AND PIN_tipo = "D" AND PIN_mode= "O";'
        cursor.execute(sSQL)
        aFilas=cursor.fetchall()
        iAnterior=0
        for aRegistro in aFilas:
            if aRegistro[0] != iAnterior:
                # recoger el nombre del dispositivo.
                sSQL = "SELECT nom_dispositivo FROM dispositivos WHERE cod_dispositivo = "+sArgDB+";"
                cursor.execute(sSQL,aRegistro[0])
                aUnaFila = cursor.fetchone()
                print
                print aUnaFila[0]
                print '-------+----+--------------------------------+---------------------+---------+'
                iAnterior = aRegistro[0]
            if aRegistro[9] == 1:
                sColor = "[1;32m"
            elif aRegistro[9] == 0:
                sColor ="[1;31m"
            print chr(27)+sColor+'|{0:5d} |{1:3} | {2:30} | {3:19} | {4:4}    |'.format(aRegistro[0],aRegistro[1],aRegistro[2],aRegistro[4],str(aRegistro[3]),aRegistro[4])+chr(27)+"[1;m"

        print '-------+----+--------------------------------+---------------------+---------+'
        print
        print
        iOp = raw_input('(1) Cambiar valor (0) Volver - Opción: ')
        if iOp==str(0): # cambio el valor de salir a verdadero para salir del WHILE
            bSalir=True
            db.commit()
        elif iOp == str(1): # Cambia VALOR
            print '*** FUNCIÓN: Cambia Valor ***'
            iRegistro = raw_input('Código de Dispositivo: ')
            iPIN = raw_input('PIN: ')
            sSQL = "SELECT activo FROM pin WHERE cod_dispositivo="+sArgDB+" AND PIN_num="+sArgDB+";""
            cursor.execute(sSQL,(iCodigo, iPIN))
            aFilas=cursor.fetchone()
            if len(aFilas)== 1:
                if aFilas[0] == 1:
                    sPregunta = "Estas seguro (s/n) de poner el PIN a LOW? "
                    iValor = 0
                elif aFilas[0] == 0:
                    sPregunta = "Estas seguro (s/n) de poner el PIN a HIGH? "
                    iValor = 1
                sConfirmacion = raw_input(sPregunta)
                if sConfirmacion == "s" or sConfirmacion == "S":

                    # buscar el valor de la IP
                    sSQL = "SELECT IP_dispositivo FROM dispositivos WHERE cod_dispositivo ="+sArgDB+";"
                    cursor.execute(sSQL,(iRegistro))
                    aUnaFila = cursor.fetchone()
                    if len(aUnaFila) == 1:
                        sSQL = "UPDATE pin SET activo="+sArgDB+" WHERE cod_dispositivo="+sArgDB+" AND PIN_num="+sArgDB+";"
                        cursor.execute(sSQL,(iValor, iCodigo, iPIN))
                        db.commit()
                        # CURL
                        WgetCommand='curl http://'+aUnaFila[0]+'/arduino/digital/'+iPIN+"/"+str(iValor)
                        sOutput=subprocess.check_output(sWgetCommand,shell=True)

            elif len(aFilas) == 0:
                print 'Error. Datos incorrectos. Pulse una tecla...'
                iOp=raw_input()
    print 'NOOXS'
    print ('Fin de programa SmartProcessHome.')


except db.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
finally:
        if db:
            db.close()