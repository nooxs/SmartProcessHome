#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'juanfajardonavarro'

import MySQLdb
import sqlite3
import os
import sys
import subprocess
import datetime
import time
from class_profiles import profilePython

config = profilePython('/etc/config/nooxs.config')


# ----------------------------------FUNCIONES ------------------------------

def fMode (queDB, iCodigo, iMode, iPIN):

    # recoger el nombre del dispositivo.
    if queDB == "M":
        cursor.execute("""SELECT IP_dispositivo FROM dispositivos WHERE cod_dispositivo = %s""",(iCodigo))
    elif queDB == "S":
        cursor.execute("""SELECT IP_dispositivo FROM dispositivos WHERE cod_dispositivo=?""",(iCodigo))
    aUnaFila = cursor.fetchone()

    if iMode == "I":
        iMode = "input"
    elif iMode == "O":
        iMode = "output"
    sWgetCommand='curl http://'+aUnaFila[0]+'/arduino/mode/'+iPIN+"/"+iMode
    sOutput=subprocess.check_output(sWgetCommand,shell=True)

def fConfiguracion(queDB):
    bSalir = False
    while not bSalir:
        os.system('clear')
        print 'NOOXS - Mantenimiento de BD nooxsense'
        print '*** Tabla Configuración ***'
        print  
        print  
        print '****************************************************************************************************************************'
        print '*cod * Nombre                       * Valor                           * Notas                                              *'
        print '****************************************************************************************************************************'
        sSQL='SELECT cod_parametro, nom_parametro, valor_parametro, notas_parametro FROM configuracion;'
        cursor.execute(sSQL)
        aFilas=cursor.fetchall()
        
        for aRegistro in aFilas:
            print '|{0:3d} |{1:30} | {2:30} | {3:40} |'.format(aRegistro[0],aRegistro[1],aRegistro[2],aRegistro[3])
        print
        print
        iOp = raw_input('(1) Añadir, (2) Borrar, (3) Modificar, (0) Volver - Opción: ')
        
        if iOp==str(0): # cambio el valor de salir a verdadero para salir del WHILE
            bSalir=True
            db.commit()
        elif iOp == str(2): # Borrar registro
            print '*** FUNCIÓN: Borrar Registro ***'
            iRegistro = raw_input('Numero de registro a borrar: ')
            sConfirmacion = raw_input('¿estás seguro (s/n)? :')
            if sConfirmacion == "s" or sConfirmacion == "S":
                if queDB == "M":
                    cursor.execute("""DELETE FROM configuracion WHERE cod_parametro = %s""", (iRegistro))
                elif queDB == "S":
                    cursor.execute("""DELETE FROM configuracion WHERE cod_parametro = ?""", (iRegistro))
                db.commit()
                
        elif iOp == str(3): # Modificar Registro
            print '*** FUNCIÓN : Modificar Registro ***'
            iRegistro = raw_input('Numero de registro a modificar: ')
            iCodigo = aRegistro[0]
            sNombre = raw_input('Nombre parametro : ')
            sValor = raw_input('Valor : ')
            sNotas = raw_input('Notas : ')
            if queDB == "M":
                cursor.execute("""UPDATE configuracion SET nom_parametro=%s,valor_parametro=%s, notas_parametro=%s WHERE cod_parametro=%s""",(sNombre, sValor, sNotas, iCodigo))
            elif queDB == "S":    
                cursor.execute("""UPDATE configuracion SET nom_parametro=?,valor_parametro=?, notas_parametro=? WHERE cod_parametro=?""",(sNombre, sValor, sNotas, iCodigo))
            db.commit()
        elif iOp == str(1): # Añadir registro
            print '*** FUNCIÓN : Añadir Registro ***'
            iCodigo = raw_input('Codigo Parametro -integer-: ')
            sNombre = raw_input('Nombre parametro : ')
            sValor = raw_input('Valor : ')
            sNotas = raw_input('Notas : ')
            if queDB == "M":
                cursor.execute("""INSERT INTO configuracion VALUES (%s, %s, %s, %s)""",(iCodigo, sNombre, sValor, sNotas))
            elif queDB == "S":
                cursor.execute("""INSERT INTO configuracion VALUES (?, ?, ?, ?)""",(iCodigo, sNombre, sValor, sNotas))
            db.commit()
            
    
def fDispositivos(queDB):
    bSalir = False
    while not bSalir:
        os.system('clear')
        print 'NOOXS - Mantenimiento de BD nooxsense'
        print '*** Tabla Dispositivos ***'
        print 
        print  
        print '**************************************************************************************************************************'
        print '*cod  * Nombre                        * MAC               * IP              *Clave                           * Activo    *'
        print '**************************************************************************************************************************'
        sSQL='SELECT cod_dispositivo, nom_dispositivo, MAC_dispositivo, IP_dispositivo, clave_dispositivo, activo FROM dispositivos;'
        cursor.execute(sSQL)
        aFilas=cursor.fetchall()
        
        for aRegistro in aFilas:
            if aRegistro[5] == 1:
                sColor = "[1;42m"
            elif aRegistro[5] == 0:
                sColor ="[1;41m"
            print chr(27)+sColor+'|{0:4d} |{1:30} | {2:17} | {3:15} | {4:30} | {5:6}    |'.format(aRegistro[0],aRegistro[1],aRegistro[2],aRegistro[3],aRegistro[4],aRegistro[5])+chr(27)+'[1;m'
        print
        print
        iOp = raw_input('(1) Añadir, (2) Borrar, (3) Modificar, (4) Activar/desactivar (0) Volver - Opción: ')
        
        if iOp==str(0): # cambio el valor de salir a verdadero para salir del WHILE
            bSalir=True
            db.commit()
        elif iOp == str(2): # Borrar registro
            print '*** FUNCIÓN: Borrar Registro ***'
            iRegistro = raw_input('Numero de registro a borrar: ')
            sConfirmacion = raw_input('¿estás seguro (s/n)? :')
            if sConfirmacion == "s" or sConfirmacion == "S":
                # antes de borrar, confirmar que no está activo. Si está activo, no se puede borrar. Primero hay que desactivarlo
                if queDB == "M":
                    cursor.execute("""DELETE FROM dispositivos WHERE cod_dispositivo = %s""", (iRegistro))
                elif queDB == "S":
                    cursor.execute("""DELETE FROM dispositivos WHERE cod_dispositivo = ?""", (iRegistro))
                db.commit()
                
        elif iOp == str(3): # Modificar Registro
            print '*** FUNCIÓN : Modificar Registro ***'
            iRegistro = raw_input('Numero de registro a modificar: ')
            sNombre = raw_input('Nombre dispositivo : ')
            sMAC = raw_input('MAC : ')
            sIP = raw_input('IP : ')
            sClave = raw_input('Clave : ')
            iActivo = raw_input('Activo (1 Activo , 0 No Activo) : ')

            # si cambia el estado a desactivo, comprobar primero si alguno de los pines está HIGH. Si alguno está HIGH no se puede desactivar

            if queDB == "M":
                cursor.execute("""UPDATE dispositivos SET nom_dispositivo=%s,MAC_dispositivo=%s, IP_dispositivo=%s, clave_dispositivo=%s, activo=%s WHERE cod_dispositivo=%s""",(sNombre, sMAC, sIP, sClave, iActivo,iRegistro))
            elif queDB == "S":    
                cursor.execute("""UPDATE dispositivos SET nom_dispositivo=?,MAC_dispositivo=?, IP_dispositivo=?, clave_dispositivo=?, activo=? WHERE cod_dispositivo=?""",(sNombre, sMAC, sIP, sClave, iActivo,iRegistro))
            db.commit()
        elif iOp == str(1): # Añadir registro
            print '*** FUNCIÓN : Añadir Registro ***'
            iCodigo = raw_input('Codigo Dispositivo -integer-: ')
            sNombre = raw_input('Nombre dispositivo : ')
            sMAC = raw_input('MAC : ')
            sIP = raw_input('IP : ')
            sClave = raw_input('Clave : ')
            iActivo = raw_input('Activo (1 Activo , 0 No Activo) : ')
            if queDB == "M":
                cursor.execute("""INSERT INTO dispositivos VALUES(%s, %s, %s, %s, %s, %s)""",(iCodigo, sNombre, sMAC, sIP, sClave, iActivo))
            elif queDB == "S":   
                cursor.execute("""INSERT INTO dispositivos VALUES(?, ?, ?, ?, ?, ?)""",(iCodigo, sNombre, sMAC, sIP, sClave, iActivo))
            db.commit()
        elif iOp == str(4): #Activar / Desactivar
            print '*** FUNCIÓN : Activar / Desactivar ***'
            iRegistro = raw_input('Numero de registro a Activar / Desactivar: ')
            sConfirmacion = raw_input('¿estás seguro (s/n)? :')
            if sConfirmacion == "s" or sConfirmacion == "S":

                # si cambia el estado a desactivo, comprobar primero si alguno de los pines está activo. Si alguno está activo no se puede desactivar
                if queDB == "M":
                    sSQL = "SELECT * FROM pin WHERE cod_dispositivo = %s AND activo = 1"
                elif queDB == "S":
                    sSQL = "SELECT * FROM pin WHERE cod_dispositivo = ? AND activo = 1"

                if cursor.execute(sSQL,(iRegistro)) == 0:   # no hay pines activos

                    # comprobar si estaba activo o desactivo y cambiar
                    if queDB == "M":
                        cursor.execute("""SELECT activo FROM dispositivos WHERE cod_dispositivo=%s""",(iRegistro))
                    elif queDB == "S":
                        cursor.execute("""SELECT activo FROM dispositivos WHERE cod_dispositivo=?""",(iRegistro))

                    aFilas=cursor.fetchone()
                    if aFilas[0] == 1:
                        if queDB == "M":
                            cursor.execute("""UPDATE dispositivos SET activo=0 WHERE cod_dispositivo=%s""",(iRegistro))
                        elif queDB == "S":
                            cursor.execute("""UPDATE dispositivos SET activo=0 WHERE cod_dispositivo=?""",(iRegistro))
                    elif aFilas[0] == 0:
                        if queDB == "M":
                            cursor.execute("""UPDATE dispositivos SET activo=1 WHERE cod_dispositivo=%s""",(iRegistro))
                        elif queDB == "S":
                            cursor.execute("""UPDATE dispositivos SET activo=1 WHERE cod_dispositivo=?""",(iRegistro))
                    db.commit()
    
def fSensores(queDB):
    bSalir = False
    while not bSalir:
        os.system('clear')
        print 'NOOXS - Mantenimiento de BD nooxsense'
        print '*** Tabla Sensores / Actuadores ***'
        print 
        print  
        print '*****************************************************************************+*********************************'
        print '|disp  | PIN |Nombre                         | D/A |    Valor     |Modo| Activo|         Valor Actual           |'
        print '|      |     |                               |     | Desde| Hasta |    |       | fecha/Hora           | valor   |'
        print '*******+****+********************************+*****+******+*******+****+*******+**********************+**********'
        sSQL='SELECT cod_dispositivo, PIN_num, PIN_nombre, PIN_tipo, PIN_valor_desde, PIN_valor_hasta, PIN_mode, activo, fechahora_actualizacion, valor_actual FROM pin;'
        cursor.execute(sSQL)
        aFilas=cursor.fetchall()
        iAnterior=0
        for aRegistro in aFilas:
            if aRegistro[0] != iAnterior:
                # recoger el nombre del dispositivo.
                if queDB == "M":
                    cursor.execute("""SELECT nom_dispositivo FROM dispositivos WHERE cod_dispositivo = %s""",(aRegistro[0]))
                elif queDB == "S":
                    cursor.execute("""SELECT nom_dispositivo FROM dispositivos WHERE cod_dispositivo=?""",(aRegistro[0]))
                aUnaFila = cursor.fetchone()
                print
                print aUnaFila[0]
                print '-------+----+--------------------------------+-----+------+-----+------+--------+---------------------+---------+'
                iAnterior = aRegistro[0]

            if aRegistro[7] == 1:
                sColor = "[1;42m"
            elif aRegistro[7] == 0:
                sColor ="[1;41m"
            print chr(27)+sColor+'|{0:5d} |{1:3} | {2:30} | {3:3} | {4:4} | {5:4} | {6:3} | {7:6} | {8:19} | {9:4}    |'.format(aRegistro[0],aRegistro[1],aRegistro[2],aRegistro[3],aRegistro[4],aRegistro[5],aRegistro[6],aRegistro[7],str(aRegistro[8]),aRegistro[9])+chr(27)+'[1;m'
        print '-------+----+--------------------------------+-----+------+-------+----+--------+---------------------+---------+'
        print
        print
        iOp = raw_input('(1) Añadir, (2) Borrar, (3) Modificar, (4) Activar/desactivar (0) Volver - Opción: ')
        
        if iOp==str(0): # cambio el valor de salir a verdadero para salir del WHILE
            bSalir=True
            db.commit()
        elif iOp == str(2): # Borrar registro
            print '*** FUNCIÓN: Borrar Registro ***'
            iRegistro = raw_input('Código de Dispositivo: ')
            iPIN = raw_input('PIN: ')

            # comprobar si está HIGH. Si está HIHG no se puede borrar
            # si está activo tampoco se puede borrar
            sSQL = 'SELECT activo, valor_actual FROM pin WHERE cod_dispositivo='+sArgDB+' AND PIN_num='+sArgDB+';'
            cursor.execute(sSQL,(iRegistro, iPIN))
            aFilas=cursor.fetchone()
            if aFilas[0] == 0 and aFilas[1] == 0:

                sConfirmacion = raw_input('¿estás seguro de borrar ese PIN (s/n)? :')
                if sConfirmacion == "s" or sConfirmacion == "S":
                    sSQL = 'DELETE FROM pin WHERE cod_dispositivo ='+sArgDB+' AND PIN_num ='+sArgDB+';'
                    cursor.execute(sSQL, (iRegistro,iPIN))
                    db.commit()
            else:
                sConfirmacion = raw_input('Error. Pulsa una tecla para volver...')
                
        elif iOp == str(3): # Modificar Registro
            print '*** FUNCIÓN : Modificar Registro ***'
            iRegistro = raw_input('Código de Dispositivo: ')
            iPIN = raw_input('PIN: ')
            sNombre = raw_input('Nombre PIN : ')
            sTipo = raw_input('Tipo ([A]nalógico o [D]igital : ')
            if sTipo == "A":
                iDesde = raw_input('Valor Desde: ')
                iHasta = raw_input('Valor Hasta: ')
                iMode = ""
            else:
                iDesde=0
                iHasta=0
                iMode = raw_input('Modo [I]nput o [O]utput : ')
            iActivo = raw_input('Activo ([1] Activo , [0] No Activo) : ')
            if queDB == "M":
                cursor.execute("""UPDATE pin SET cod_dispositivo=%s,PIN_num=%s, PIN_nombre=%s, PIN_tipo=%s, PIN_valor_desde=%s, PIN_valor_hasta=%s, activo=%s WHERE cod_dispositivo=%s AND PIN_num=%s""",(iRegistro, iPIN, sNombre, sTipo, iDesde, iHasta, iActivo,iRegistro, iPIN))
            elif queDB == "S":   
                cursor.execute("""UPDATE pin SET cod_dispositivo=?,PIN_num=?, PIN_nombre=?, PIN_tipo=?, PIN_valor_desde=?, PIN_valor_hasta=?, activo=? WHERE cod_dispositivo=? AND PIN_num=?""",(iRegistro, iPIN, sNombre, sTipo, iDesde, iHasta, iActivo,iRegistro, iPIN))
            db.commit()

            # poner el pin en mode PIN_mode
            if sTipo == "D" and (iMode == "I" or iMode == "O"):
                fMode(queDB, iRegistro, iMode, iPIN)
            else:
                print ("Modo incorrecto, debe de ser O para Output o I para Input. Solo se admiten esos valores. Vuelva a intentarlo.")
        elif iOp == str(1): # Añadir registro
            print '*** FUNCIÓN : Añadir Registro ***'
            iCodigo = raw_input('Codigo Dispositivo -integer-: ')
            iPIN = raw_input('PIN: ')
            sNombre = raw_input('Nombre PIN : ')
            sTipo = raw_input('Tipo ([A]nalógico o [D]igital : ')
            if sTipo == "A":
                iDesde = raw_input('Valor Desde: ')
                iHasta = raw_input('Valor Hasta: ')
                iMode = ""
            else:
                iDesde = 0
                iHasta = 0
                iMode = raw_input('Modo [I]nput o [O]utput : ')
            iActivo = raw_input('[1] Activo , [0] No Activo) : ')
            if queDB == "M":
                cursor.execute("""INSERT INTO pin (cod_dispositivo, PIN_num, PIN_nombre, PIN_tipo, PIN_valor_desde, PIN_valor_hasta, activo, PIN_mode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",(iCodigo, iPIN, sNombre, sTipo, iDesde, iHasta, iActivo, iMode))
            elif queDB == "S":   
                cursor.execute("""INSERT INTO pin (cod_dispositivo, PIN_num, PIN_nombre, PIN_tipo, PIN_valor_desde, PIN_valor_hasta, activo, PIN_mode) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",(iCodigo, iPIN, sNombre, sTipo, iDesde, iHasta, iActivo, iMode))
            db.commit()

            # poner el pin en mode PIN_mode
            if sTipo == "D" and (iMode == "I" or iMode == "O"):
                fMode(queDB, iCodigo, iMode, iPIN)
            else:
                print ("Modo incorrecto, debe de ser O para Output o I para Input. Solo se admiten esos valores. Vuelva a intentarlo.")
        elif iOp == str(4): #Activar / Desactivar
            print '*** FUNCIÓN : Activar / Desactivar ***'
            iCodigo = raw_input('Código de Dispositivo: ')
            iPIN = raw_input('Numero de PIN a Activar / Desactivar: ')
            sConfirmacion = raw_input('¿estás seguro (s/n)? :')
            if sConfirmacion == "s" or sConfirmacion == "S":
                # comprobar si estaba activo o desactivo y cambiar
                if queDB == "M":
                    cursor.execute("""SELECT activo FROM pin WHERE cod_dispositivo=%s AND PIN_num=%s""",(iCodigo, iPIN))
                elif queDB == "S":   
                    cursor.execute("""SELECT activo FROM pin WHERE cod_dispositivo=? AND PIN_num=?""",(iCodigo, iPIN))
                aFilas=cursor.fetchone()
                if aFilas[0] == 1:
                    if queDB == "M":
                        cursor.execute("""UPDATE pin SET activo=0 WHERE cod_dispositivo=%s AND PIN_num=%s""",(iCodigo, iPIN))
                    elif queDB == "S":   
                        cursor.execute("""UPDATE pin SET activo=0 WHERE cod_dispositivo=? AND PIN_num=?""",(iCodigo, iPIN))
                elif aFilas[0] == 0:
                    if queDB == "M":
                        cursor.execute("""UPDATE pin SET activo=1 WHERE cod_dispositivo=%s AND PIN_num=%s""",(iCodigo, iPIN))
                    elif queDB == "S":   
                        cursor.execute("""UPDATE pin SET activo=1 WHERE cod_dispositivo=? AND PIN_num=?""",(iCodigo, iPIN))
                db.commit()


def fRegistro(queDB):
    bSalir = False
    while not bSalir:
        os.system('clear')
        print 'NOOXS - Mantenimiento de BD nooxsense'
        print '*** Tabla Registro Instantaneo ***'
        print 
        print  
        print '*************************************************'
        print '| Fecha     |Disp    |PIN  |Hora        |Valor  |'
        print '*************************************************'
        sSQL='SELECT fecha, cod_dispositivo, PIN_num, hora, PIN_valor FROM registroinstantaneo ;'
        cursor.execute(sSQL)
        aFilas=cursor.fetchall()

        for aRegistro in aFilas:
            print '|{0:10} | {1:5d} | {2:4} | {3:10} | {4:1}     |'.format(str(aRegistro[0]), aRegistro[1], aRegistro[2], str(aRegistro[3]), str(aRegistro[4]))
            print '––––––––––––––––––––––––––––––––––––––––––––––––––'

        print
        print
        iOp = raw_input('Pulsa cualquier tecla para volver ')
        bSalir= True
        db.commit()

def fRegistroDiario(queDB):
    bSalir = False
    while not bSalir:
        os.system('clear')
        print 'NOOXS - Mantenimiento de BD nooxsense'
        print '*** Tabla Registro Diario ***'
        print
        print
        print 'SOLO PARA PINES DIGITALES Y EN MODO OUTPUT'
        print
        print '*******************************************'
        print '|           |       |      | minutos en   |'
        print '| Fecha     |Disp   |PIN   |  1   |  0    |'
        print '*******************************************'
        sSQL='SELECT fecha, cod_dispositivo, PIN_num, min1,min0 FROM registrodiario ;'
        cursor.execute(sSQL)
        aFilas=cursor.fetchall()
        x = 0
        dFechaAnterior = aFilas[0][0]
        for aRegistro in aFilas:
            if dFechaAnterior != aRegistro[0]:
                dFechaAnterior = aRegistro[0]
                print
                print
            print '|{0:10} | {1:5d} | {2:4} | {3:5d}| {4:5d} |'.format(str(aRegistro[0]), aRegistro[1], aRegistro[2],aRegistro[3],aRegistro[4])
            print '–––––––––––––––––––––––––––––––––––––––––––'
            x = x +1
            if x == 100:
                x= 0
                y=raw_input('pulse una tecla para continuar...')

        print
        print
        iOp = raw_input('Pulsa cualquier tecla para volver ')
        bSalir= True
        db.commit()
# FIN FUNCIONES --------------------------

# ------------------------------ P R I N C I P A L --------------------------------------------------
try:
    salir = False
    while not salir:
        os.system('clear')
        print 'NOOXS - Mantenimiento de BD nooxsense'
        queDB = config.profile('DB', 'db')
        if queDB == 'MySQL':
            sHost = config.profile('MySQL','host')
            sUser = config.profile('MySQL','USER')
            sPass = config.profile('MySQL','PASS')
            sDB = config.profile('MySQL','DB')
            sArgDB = config.profile('DB','Argumentos')
            db=MySQLdb.connect(host=sHost,user=sUser,passwd=sPass,db=sDB)
            queDB = "M"
            salir = True
        elif queDB == 'SQLite':
            sDB = config.profile('SQLite','DB')
            sHost = config.profile('SQLite','host')
            db=sqlite3.connect(sDB)
            sArgDB = config.profile('DB','Argumentos')
            salir = True
            queDB = "S"
    
    cursor=db.cursor()
    
    #entro en el bucle
    salir = False
    # evaluo la condicion si la variable salir es verdadera entonces entro al bucle
    # el operador (not) invierte el valor de la variable
    os.system('clear')
    
    while not salir:
        print 'NOOXS - Mantenimiento de BD nooxsense'
        print sDB, 'en ',sHost

        print
        print 'Menu Principal'
        print
        print '1 - Configuracion'
        print '2 - Dispositivos'
        print '3 - Sensores / Actuadores'
        print '4 - Registro instantaneo'
        print '5 - Registro Diario'
        print '0 - Salir'
        print
        op = raw_input('Opcion: ')
        print
        if op == str(1):
            fConfiguracion(queDB)
        if op == str(2):
            fDispositivos(queDB)
        if op == str(3):
            fSensores(queDB)
        if op == str(4):
            fRegistro(queDB)
        if op == str(5):
            fRegistroDiario(queDB)
        if op==str(0): # cambio el valor de salir a verdadero
            salir=True
    
        os.system('clear')
        print
    # esta linea permite que el programa no termine hasta que se de Enter
    print 'NOOXS'
    print ('Fin de programa Mantenimiento DB.')

except db.Error, e:
        if queDB == "M":
            print "Error %d: %s" % (e.args[0],e.args[1])
        elif queDB == "S":
            print "Error %s" % e.args[0]        
        sys.exit(1)
finally:
        if db:
                db.commit()
                db.close()