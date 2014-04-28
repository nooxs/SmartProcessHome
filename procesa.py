#!/usr/bin/env python
# -*- coding: utf-8 -*-

# llamar al programa : python procesa.py 0.0.0.0  0.0.0.0 donde :
# argumento 1 es la dirección IP del servidor MySQL. 'localhost' si se ejecuta desde el propio servidor
# argumento 2 es la dirección IP del Arduino local
# esta aplicación funciona con Bridge_OK cargado en Arduino YUN

import MySQLdb
import sys
import os
import subprocess
import datetime
import time
from class_profiles import profilePython

config = profilePython('/etc/config/nooxs.config')

try:
        sHost = config.profile('MySQL','host')
        sUser = config.profile('MySQL','USER')
        sPass = config.profile('MySQL','PASS')
        sDB = config.profile('MySQL','DB')
        smiIP = config.profile('procesa','miIP')
        #if len(sys.argv) < 2:
        #    print ("Error: Faltan argumentos. Debe de especificar como argumentos:")
        #    print ("argumento 1: direccion IP del servidor de base de datos MySQL")
        #    print ("argumento 2: direccion IP de localhost")
        #    sys.exit(1)
        print sHost,'-',sUser,'-',sPass,'-',sDB,'-',smiIP
        db=MySQLdb.connect(host=sHost,user=sUser,passwd=sPass,db=sDB)
        #db=MySQLdb.connect(host=sys.argv[1],user='root',passwd='jfajardo1',db='nooxsense')
        cursor=db.cursor()

        #registros de la tabla dispositivos de los dispositivos activos
        #cursor.execute("""SELECT cod_dispositivo, IP_dispositivo FROM dispositivos WHERE activo=1 AND IP_dispositivo= %s""",(sys.argv[2]))
        cursor.execute("""SELECT cod_dispositivo, IP_dispositivo FROM dispositivos WHERE activo=1 AND IP_dispositivo= %s""",(smiIP))
        aFilas=cursor.fetchall()
        for aRegistro in aFilas:
                iCodDispositivo=aRegistro[0]
                sIPDisp=aRegistro[1]
                
                #selecciono los registros de la tabla PIN del dispositivo seleccionado (solo los activos)
                cursor.execute("""SELECT PIN_num, PIN_nombre, PIN_tipo, valor_actual FROM pin WHERE activo=1 AND cod_dispositivo=%s""",(iCodDispositivo))
                aFilas2=cursor.fetchall()
                for aReg2 in aFilas2:
                        
                        #ejecutar curl que comprueba el estado del pin
                        sWgetCommand='curl http://'+sIPDisp+'/arduino/digital/'+aReg2[0]
                        sOutput=subprocess.check_output(sWgetCommand,shell=True)
                        
                        #curl devuelve una cadena como: Pin D13 set to 1
                        
                        #selecciono lo que hay a partir de to
                        iDonde=sOutput.find("to")+3
                        
                        #el numero de PIn es el valor convertido a int desde la posicion hasta el final                
                        iVPin=int(sOutput[iDonde:])
                        dFechayHora=datetime.datetime.now()
        
                        #guardar registroinstantaneo
                        cursor.execute("""INSERT INTO registroinstantaneo VALUES (%s, %s, %s, %s)""",(iCodDispositivo,dFechayHora,aReg2[0],iVPin))
                        
                        #si el valor actual es diferente al valor anterior cambio el estado
                        if iVPin != aReg2[3]:
                            
                            #cambiar el estado del pin en tabla pin
                            cursor.execute("""UPDATE pin SET valor_actual=%s,fechahora_actualizacion=%s WHERE cod_dispositivo=%s AND PIN_num=%s AND activo=1""",(iVPin,dFechayHora,iCodDispositivo,aReg2[0]))
                        db.commit()
except db.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
finally:
        if db:
                db.close()

