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
def fProgramador(queDB):
    bSalir = False
    while not bSalir:
        os.system('clear')
        print 'NOOXS - SmartProcessHome'
        print '*** Sensores / Actuadores de la red ***'
        print "\033[1;33m- nota V1: solo para pines digitales, Output, Activos-\033[1;m"
        print
        print

        iOp = raw_input('(0) Volver - Opción: ')
        if iOp==str(0): # cambio el valor de salir a verdadero para salir del WHILE
            bSalir=True
            db.commit()

def fManual(queDB):
    bSalir = False
    while not bSalir:
        os.system('clear')
        print 'NOOXS - SmartProcessHome'
        print '*** Sensores / Actuadores de la red ***'
        print "\033[1;33m- nota V1: solo para pines digitales, Output, Activos-\033[1;m"
        print
        print
        print '***********************************************************************************'
        print '|disp  | PIN |Nombre                        |Mode |         Valor Actual           |'
        print '|      |     |                              |     | fecha/Hora           | valor   |'
        print '*******+****+*******************************+*****+**********************+**********'
        sSQL='SELECT cod_dispositivo, PIN_num, PIN_nombre, PIN_mode, fechahora_actualizacion, valor_actual FROM pin WHERE activo=1 AND PIN_tipo = "D";'
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
                print '-------+----+--------------------------------+----+---------------------+---------+'
                iAnterior = aRegistro[0]
            if aRegistro[5] == 1:
                sColor = "[1;42m"
            elif aRegistro[5] == 0:
                if aRegistro[3] == "I":
                    sColor ="[1;41m"
                elif aRegistro[3] == "O":
                    sColor = "[1;43m"
            print chr(27)+sColor+'|{0:5d} |{1:3} | {2:30} |{3:4}| {4:19} | {5:4}    |'.format(aRegistro[0],aRegistro[1],aRegistro[2],aRegistro[3],str(aRegistro[4]),aRegistro[5])+chr(27)+"[1;m"

        print '-------+----+--------------------------------+----+---------------------+---------+'
        print
        print
        iOp = raw_input('(M) Mode (V) Cambiar valor (0) Volver - Opción: ')
        if iOp==str(0): # cambio el valor de salir a verdadero para salir del WHILE
            bSalir=True
            db.commit()

        elif iOp.upper() == "M": # establecer mode
            print '*** FUNCIÓN: Cambiar Mode ***'
            iRegistro = raw_input('Código de Dispositivo: ')
            iPIN = raw_input('PIN: ')
            sSQL = "SELECT valor_actual, PIN_mode FROM pin WHERE activo = 1 and cod_dispositivo="+sArgDB+" AND PIN_num="+sArgDB+";"
            cursor.execute(sSQL,(iRegistro, iPIN))
            aFilas=cursor.fetchone()
            while aFilas is not None:
                if len(aFilas) == 2:
                    if aFilas[1] == "I":
                        sPregunta = "Estas seguro (s/n) de poner el PIN a Output? "
                        sValor = "output"
                    elif aFilas[1] == "O":
                        sPregunta = "Estas seguro (s/n) de poner el PIN a Input? "
                        sValor = "input"
                    sConfirmacion = raw_input(sPregunta)
                    if sConfirmacion == "s" or sConfirmacion == "S":
                        # buscar el valor de la IP
                        sSQL = "SELECT IP_dispositivo FROM dispositivos WHERE cod_dispositivo ="+sArgDB+";"
                        cursor.execute(sSQL,(iRegistro))
                        aUnaFila = cursor.fetchone()
                        while aUnaFila is not None:
                            if len(aUnaFila) == 1:
                                sSQL = "UPDATE pin SET PIN_mode="+sArgDB+" WHERE cod_dispositivo="+sArgDB+" AND PIN_num="+sArgDB+";"
                                cursor.execute(sSQL,(sValor.upper(),iRegistro, iPIN))
                                db.commit()
                                # CURL
                                sWgetCommand='curl http://'+aUnaFila[0]+'/arduino/mode/'+iPIN+"/"+sValor
                                sOutput=subprocess.check_output(sWgetCommand,shell=True)
                            break
                break
        elif iOp.upper() == "V": # Cambia VALOR
            print '*** FUNCIÓN: Cambia Valor ***'
            iRegistro = raw_input('Código de Dispositivo: ')
            iPIN = raw_input('PIN: ')
            sSQL = "SELECT valor_actual,PIN_mode FROM pin WHERE activo=1 and cod_dispositivo="+sArgDB+" AND PIN_num="+sArgDB+";"
            cursor.execute(sSQL,(iRegistro, iPIN))
            aFilas=cursor.fetchone()
            while aFilas is not None:
                if len(aFilas)== 2 and aFilas[1] == "O":
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
                        while aUnaFila is not None:
                            if len(aUnaFila) == 1:
                                sSQL = "UPDATE pin SET valor_actual="+sArgDB+",fechahora_actualizacion="+sArgDB+" WHERE cod_dispositivo="+sArgDB+" AND PIN_num="+sArgDB+";"
                                cursor.execute(sSQL,(iValor, datetime.datetime.today(),iRegistro, iPIN))
                                db.commit()
                                # CURL
                                sWgetCommand='curl http://'+aUnaFila[0]+'/arduino/digital/'+iPIN+"/"+str(iValor)
                                sOutput=subprocess.check_output(sWgetCommand,shell=True)
                            break
                elif len(aFilas) == 0:
                    print 'Error. Datos incorrectos. Pulse una tecla...'
                    iOp=raw_input()
                break



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

    bSalir = False
    while not bSalir:
        os.system('clear')
        print 'NOOXS - Actuadores / Sensores'
        print sDB, 'en ',sHost

        print
        print 'Menu Principal'
        print
        print '1 - Manual'
        print '2 - Programador'
        print '0 - Salir'
        print
        op = raw_input('Opcion: ')
        print
        if op == str(1):
            fManual(queDB)
        if op == str(2):
            fProgramador(queDB)
        if op==str(0): # cambio el valor de salir a verdadero
            bSalir=True

        os.system('clear')
        print
    # esta linea permite que el programa no termine hasta que se de Enter
    print 'NOOXS'
    print ('Fin de programa Actuadores / Sensores.')


#----------------------------------------------


except db.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
finally:
        if db:
            db.close()