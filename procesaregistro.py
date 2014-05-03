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
def fSumariza(dDesde,dHasta)
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
    do while dVarFecha < 


###############################################################
# PRINCIPAL ###################################################
###############################################################
try:
    sHost = config.profile('MySQL','host')
    sUser = config.profile('MySQL','USER')
    sPass = config.profile('MySQL','PASS')
    sDB = config.profile('MySQL','DB')
    db=MySQLdb.connect(host=sHost,user=sUser,passwd=sPass,db=sDB)

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