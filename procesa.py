#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'juanfajardonavarro'


import MySQLdb
import sys
import subprocess
import datetime
from class_profiles import profilePython

config = profilePython('/etc/config/nooxs.config')

try:
        sHost = config.profile('MySQL','host')
        sUser = config.profile('MySQL','USER')
        sPass = config.profile('MySQL','PASS')
        sDB = config.profile('MySQL','DB')
        sExternos = config.profile('procesa','DispExternos')
        aExternos = [config.profile('procesa','Ext1'), config.profile('procesa','Ext2'), config.profile('procesa','Ext3'), config.profile('procesa','Ext4')]
        aExternos = aExternos + [config.profile('procesa','Ext5'), config.profile('procesa','Ext6'), config.profile('procesa','Ext7'), config.profile('procesa','Ext8'), config.profile('procesa','Ext9')]

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

        for w in aExternos:
            if sExternos == "0":
                # no hay que procesar IP externas y por lo tanto solo hay que procesar la IP de smi IP
                sIPProcesar = smiIP

            else:
                # hay que procesar IP's externas
                # en cada vuelta del for proceso una IP diferente hasta que encuentre una IP vacía
                sIPProcesar = w

            if sIPProcesar != "":
                print "procesa ", sIPProcesar
                #cursor.execute("""SELECT cod_dispositivo, IP_dispositivo FROM dispositivos WHERE activo=1 AND IP_dispositivo= %s""",(sys.argv[2]))
                cursor.execute("""SELECT cod_dispositivo, IP_dispositivo FROM dispositivos WHERE activo=1 AND IP_dispositivo= %s""",(sIPProcesar))
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
                                dFecha = datetime.datetime.date(dFechayHora)
                                dHora = datetime.datetime.time(dFechayHora)

                                #guardar registroinstantaneo
                                cursor.execute("""INSERT INTO registroinstantaneo (cod_dispositivo,fechahora,PIN_num,PIN_valor,fecha,hora) VALUES (%s, %s, %s, %s, %s, %s)""",(iCodDispositivo,dFechayHora,aReg2[0],iVPin, dFecha, dHora))

                                #si el valor actual es diferente al valor anterior cambio el estado
                                if iVPin != aReg2[3]:

                                    #cambiar el estado del pin en tabla pin
                                    cursor.execute("""UPDATE pin SET valor_actual=%s,fechahora_actualizacion=%s WHERE cod_dispositivo=%s AND PIN_num=%s AND activo=1""",(iVPin,dFechayHora,iCodDispositivo,aReg2[0]))
                                db.commit()
                if sExternos == "0":
                    # no hay que procesar IP's externas por lo tanto , al terminar de procesar miIP acabo el proceso
                    break
except db.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
finally:
        if db:
                db.close()

