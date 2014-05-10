#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'juanfajardonavarro'

import MySQLdb
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
def fIntegridad(queDB):
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
                """
                # recoger el nombre del dispositivo.
                sSQL = "SELECT nom_dispositivo FROM dispositivos WHERE cod_dispositivo = "+sArgDB+";"
                cursor.execute(sSQL,aRegistro[0])
                aUnaFila = cursor.fetchone()
                print
                print aUnaFila[0]
                print '-------+----+--------------------------------+----+---------------------+---------+'
                """
                iAnterior = aRegistro[0]
            if aRegistro[5] == 1:           """está en HIGH"""
                sColor = "[1;42m"
            elif aRegistro[5] == 0:         """está en LOW"""
                if aRegistro[3] == "I":         """INPUT"""
                    sColor ="[1;41m"
                elif aRegistro[3] == "O":       """OUTPUT"""
                    sColor = "[1;43m"
            print chr(27)+sColor+'|{0:5d} |{1:3} | {2:30} |{3:4}| {4:19} | {5:4}    |'.format(aRegistro[0],aRegistro[1],aRegistro[2],aRegistro[3],str(aRegistro[4]),aRegistro[5])+chr(27)+"[1;m"

        print '-------+----+--------------------------------+----+---------------------+---------+'
        print
        bSalir = True


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
        print 'NOOXS - Recuperar integridad del sistema'
        print sDB, 'en ',sHost

        fIntegridad(queDB)
        bSalir=True


    print 'NOOXS'
    print ('Fin de programa Recuperar Integridad del Sistema.')


#----------------------------------------------


except db.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
finally:
        if db:
            db.close()