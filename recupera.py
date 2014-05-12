#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'juanfajardonavarro'

#
#  este programa solo es necesario en ARDUINO + WIFLY
# en Arduino YUN se recupera la integridad automáticamente a través de Bridge.begin()
#


import MySQLdb
import os
import sys
import subprocess
from class_profiles import profilePython

# gestión de configuración
config = profilePython('/etc/config/nooxs.config')

# variables generales

###############################################################
# FUNCIONES ###################################################
###############################################################
def ejectutaCURL(sComando):
    # probar os.system(sWgetCommand)
    # probar subprocess.call(sWgetCommand,shell=True)
    # mejor: proceso = subprocess.Popen(sWgetCommand,stdout=PIPE, stderr=PIPE)
    # error_encontado= proceso.stderr.read()
    # proceso.stderr.close()
    # listado = proceso.stdout.read()
    # proceso.stdout.close()
    # if not error_encontrado:
    #   print listado
    # else:
    #   print "Se produjo error: \n%s" % error_encontrado

    outfd = open('recupera_out', 'w+')
    errfd = open('recupera_err', 'w+')
    iError = subprocess.call(sComando, shell=True, stdout=outfd, stderr=errfd)
    outfd.close()
    errfd.close()
    if not iError == 0:
        return True
    else:
        return False

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
        sSQL='SELECT cod_dispositivo, PIN_num, PIN_nombre, PIN_mode, valor_actual FROM pin WHERE activo=1 AND PIN_tipo = "D";'
        cursor.execute(sSQL)
        aFilas=cursor.fetchall()
        for aRegistro in aFilas:
            if aRegistro[4] == 1:
                # ------------------------ HIGH -------------------
                sColor = "[1;42m"
                iPIN = aRegistro[1]
                iValor = 1
                sMode = "output"
            elif aRegistro[4] == 0:
                # ------------------------- LOW -------------------
                if aRegistro[3] == "I":
                    # --------------------- INPUT -----------------
                    sColor ="[1;41m"
                    iPIN = aRegistro[1]
                    iValor = 0
                    sMode = "input"
                elif aRegistro[3] == "O":
                    # ----------------------- OUTPUT ----------------
                    sColor = "[1;43m"
                    iPIN = aRegiastro[1]
                    iValor = 0
                    sMode = "output"

            print chr(27)+sColor+'|{0:5d} |{1:3} | {2:30} |{3:4}| {5:4}    |'.format(aRegistro[0],aRegistro[1],aRegistro[2],aRegistro[3],aRegistro[4])+chr(27)+"[1;m"

            # buscar el valor de la IP
            sSQL = "SELECT IP_dispositivo FROM dispositivos WHERE cod_dispositivo ="+sArgDB+";"
            cursor.execute(sSQL,(aRegistro[0]))
            aUnaFila = cursor.fetchone()
            while aUnaFila is not None:
                if len(aUnaFila) == 1:
                    # CURL del modo
                    sWgetCommand='curl http://'+aUnaFila[0]+'/arduino/mode/'+iPIN+"/"+sMode
                    if not ejecutaCURL(sWgetCommand):
                        print "error..."
                        break
                    else:
                    # CURL del valor
                    sWgetCommand='curl http://'+aUnaFila[0]+'/arduino/digital/'+iPIN+"/"+str(iValor)
                    if not ejecutaCURL(sWgetCommand):
                        print "error..."
                        break
                break

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