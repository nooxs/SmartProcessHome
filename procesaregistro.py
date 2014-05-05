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
def ExisteRegistro(iCod,sPIN, dFecha):
    sSQL = 'SELECT * FROM registrodiario WHERE cod_dispositivo = '
    sSQL = sSQL + sArgDB + ' AND PIN_num = '+ sArgDB + ' AND fecha = '+sArgDB+' ;'
    cursor.execute(sSQL,(iCod, sPIN,dFecha))
    aFilasR = cursor.fetchall()
    return (len(aFilasR))


def InsertaRegistro(iCod,sPIN,ip1,ip0,dFecha):
    # no existe registro en registrodiario
    #
    #  esto SOLO GUARDA PARA PIN DIGITAL y OUTPUT.
    # falta toda la parte para pines digitales INPUT y pines analogicos
    #
    #
    #
    sO = "O"
    s0 = 0
    sSQL = 'INSERT INTO registrodiario VALUES ('+sArgDB+', '+sArgDB+', '+sArgDB+', '+sArgDB+', '+sArgDB+' ,'+sArgDB+','+sArgDB+');'
    cursor.execute(sSQL,(iCod,sPIN,sO,ip1,ip0,s0,dFecha))


def ModificaRegistro(iCod,sPIN,ip1,ip0,dFecha):
    # ya existia un registro en registrodiario
    sSQL = 'UPDATE registrodiario SET min0= min0+'+sArgDB+' , min1=min1+'+sArgDB+'  WHERE cod_dispositivo = '
    sSQL = sSQL + sArgDB + ' AND PIN_num = '+ sArgDB + ' AND fecha = '+sArgDB+' ;'
    cursor.execute(sSQL,(ip0,ip1,iCod,sPIN,dFecha))


def fcambia():
    cursor.execute('SELECT fechahora,PIN_num FROM registroinstantaneo;')
    aFilas=cursor.fetchall()
    for aRegistro in aFilas:
        dFecha = datetime.datetime.date(aRegistro[0])
        tHora = datetime.datetime.time(aRegistro[0])
        print dFecha
        print tHora
        cursor.execute('UPDATE registroinstantaneo SET fecha=date(fechahora), hora=time(fechahora)')

def fBorrar(dFecha):
    sSQL = 'DELETE FROM registroinstantaneo WHERE fecha <= '
    sSQL = sSQL + sArgDB+';'
    cursor.execute(sSQL,(dFecha))
    print 'borrar anterior o igual a ', dFecha, ' ---------------------------------------------------'

def fSumariza(dHoy):

    sSQL = 'SELECT fecha, cod_dispositivo, PIN_num, PIN_valor FROM registroinstantaneo WHERE fecha < '
    sSQL = sSQL + sArgDB + ';'
    cursor.execute(sSQL,dHoy)

    aFilasI=cursor.fetchall()
    iNumRegistro =  len(aFilasI)
    ix = 0
    if iNumRegistro < 1:
        print 'No hay registros para procesar...'
        return
    dFechaAnterior = aFilasI[0][0]
    dFechaCambia = dFechaAnterior

    for aRegistro in aFilasI:
        print str(ix) ,' de ', str(iNumRegistro)
        dFechaAnterior = aRegistro[0]
        # comprobar si hay registro en registrodiario
        iCodDispositivo = aRegistro[1]
        sPIN = aRegistro[2]
        iValor = aRegistro[3]
        iPara1 = 0
        iPara0 = 0
        if iValor == 1:
            iPara1 = 1
        elif iValor == 0:
            iPara0 = 1

        if ExisteRegistro(iCodDispositivo,sPIN, dFechaAnterior) == 0:
            InsertaRegistro(iCodDispositivo,sPIN,iPara1, iPara0, dFechaAnterior)
        else:
            ModificaRegistro(iCodDispositivo,sPIN,iPara1, iPara0, dFechaAnterior)
        ix=ix+1
        if (dFechaAnterior != dFechaCambia) or (ix == iNumRegistro):
            dFechaCambia = dFechaAnterior
            fBorrar(dFechaCambia)



    db.commit()

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
        #dAyerDesde = dFechaProceso+datetime.timedelta(days=-1)
        #dAyerDesde = dAyerDesde.replace(hour=0)
        #dAyerDesde = dAyerDesde.replace(minute=0)
        #dAyerDesde = dAyerDesde.replace(second=0)
        #dAyerHasta = dAyerDesde + datetime.timedelta(hours=24)
        dHoy = datetime.date.today()
        #print "Procesando el día de ayer... "
        #print "hoy : ", str(dFechaProceso)
        #print "ayer es desde : ", str(dAyerDesde)
        #print "hasta: ",str(dAyerHasta)

        fSumariza(dHoy)

    elif sys.argv[1] == "-m":
        print "Procesando el mes pasado... "
        print "hoy : ", dFechaProceso.strftime('%d-%m-%Y')
        dMesPasado = datetime.datetime.today() + relativedelta(months=-1)
        dMesPasado = dMesPasado.replace(day=1)
        print "procesar desde : ", dMesPasado.strftime('%d-%m-%Y')
        dPrimerDiaEsteMes = datetime.datetime.today()
        dPrimerDiaEsteMes = dPrimerDiaEsteMes.replace(day=1)
        print "hasta : ", dPrimerDiaEsteMes.strftime('%d-%m-%Y')

        #fSumariza(dPrimerDiaEsteMes)


except db.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
finally:
        if db:
            db.close()