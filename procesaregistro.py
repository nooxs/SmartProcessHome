#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'juanfajardonavarro'


# Importación de módulos
import MySQLdb
import sys
import os
import subprocess
import datetime, calendar
from dateutil.relativedelta import relativedelta
from class_profiles import profilePython

# gestión de parámetros
# solo acepta un parámetro y que el mismo sea válido
if (len(sys.argv)> 2 or len(sys.argv)==1) or (sys.argv[1] != "-d" and sys.argv[1] != "-m"):
    print "Este programa funciona con un parámetro:"
    print "-d para procesar el día anterior"
    print "-m para procesar el mes anterior"
    sys.exit()


# gestión de configuración
config = profilePython('/etc/config/nooxs.config')

# variables generales
dFechaProceso = datetime.datetime.today()


###############################################################
# FUNCIONES ###################################################
###############################################################
def fSumariza(dDesde,dHasta):
    # Varfecha igual ayer ( esto lo hago para al menos entrar una cez al bucle)

    # Do while varfecha menor hoy

    # Leo primer registro
    # Varfecha igual a fecha registro
    # Varpin igual a pin
    # Select todos reg de igual fecha e igual pin
    # Proceso estos registros de forma diferente si el pin es analogico o digital

    # Para analogico hay que sacar medias
    # Para digital hay que contar minutos en 1 y minutos en 0

    # Cuento total reg igual al num de minutos
    # Cuento
    #

    dVarFecha = dFechaProceso+datetime.timedelta(days=-1)
    bSalir = False
    aFechas = []
    while not bSalir:
        sSQL = 'SELECT fechahora, cod_dispositivo, PIN_num, PIN_valor FROM registroinstantaneo WHERE fechahora < '
        sSQL = sSQL + sArgDB + ';'
        cursor.execute(sSQL,dHasta)

        aFilasI=cursor.fetchall()

        dFechaAnterior = aFilasI[0][0]
        aFechas.append(dFechaAnterior)
        # comprobar si hay registro en registrodiario
        iCodDispositivo = aFilas[0][1]
        sPIN = aFilas[0][2]
        iValor = aFilas[0][3]
        sSQL = 'SELECT * FROM registrodiario WHERE cod_dispositivo = '
        sSQL = sSQL + sArgDB + ' AND PIN_num = '+ sArgDB + ' AND fecha = '+sArgDB+' ;'
        cursor.execute(sSQL,(iCodDispositivo, sPIN,datetime.datetime.date(dFechaAnterior)))
        aFilasR = cursor.fetchall()
        if len(aFilasR) == 0:
            # no existe registro en registrodiario
            #
            #  esto SOLO GUARDA PARA PIN DIGITAL y OUTPUT.
            # falta toda la parte para pines digitales INPUT y pines analogicos
            #
            #
            #
            sSQL = 'INSERT INTO registrodiario VALUES ('+sArgDB+', '+sArgDB+',O,0,1,0'+', '+sArgDB+');'
            cursor.execute(sSQL,(iCodDispositivo,sPIN,datetime.datetime.date(dFechaAnterior)))
            db.commit()


        else:
            # ya existia un registro en registrodiario

        for aRegistro in aFilasI:

            if datetime.datetime.date(aRegistro[0]) != datetime.datetime.date(dFechaAnterior):
                # cambiado de día
                dFechaAnterior = aRegistro[0]
                aFechas.append(dFechaAnterior)
            else:
                # estamos en el mismo día

        #print len(aFechas)
        #x=raw_input()
        for x in aFechas:
            print 'dia ',str(x)
        bSalir= True

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
    os.system('clear')


    if sys.argv[1] == "-d":
        dAyerDesde = dFechaProceso+datetime.timedelta(days=-1)
        dAyerDesde = dAyerDesde.replace(hour=0)
        dAyerDesde = dAyerDesde.replace(minute=0)
        dAyerDesde = dAyerDesde.replace(second=0)
        dAyerHasta = dAyerDesde + datetime.timedelta(hours=24)

        print "Procesando el día de ayer... "
        print "hoy : ", str(dFechaProceso)
        print "ayer es desde : ", str(dAyerDesde)
        print "hasta: ",str(dAyerHasta)

        fSumariza(dAyerDesde, dAyerHasta)

    elif sys.argv[1] == "-m":
        print "Procesando el mes pasado... "
        print "hoy : ", dFechaProceso.strftime('%d-%m-%Y')
        dMesPasado = datetime.datetime.today() + relativedelta(months=-1)
        dMesPasado = dMesPasado.replace(day=1)
        print "procesar desde : ", dMesPasado.strftime('%d-%m-%Y')
        dPrimerDiaEsteMes = datetime.datetime.today()
        dPrimerDiaEsteMes = dPrimerDiaEsteMes.replace(day=1)
        print "hasta : ", dPrimerDiaEsteMes.strftime('%d-%m-%Y')

        fSumariza(dMesPasado,dPrimerDiaEsteMes)


except db.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
finally:
        if db:
            db.close()