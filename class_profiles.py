# -*- coding: utf8 -*
#http://elviajedelnavegante.blogspot.com.es/2010/06/gestion-de-ficheros-de-configuracion-de.html

import os
import time

class profilePython(object):
   '''
   Clase que implementa el mecanismo de utilización de ficheros
   de configuración.
   '''
   def __init__(self, filename):
       '''
       Inicialización.
       '''
       # Nombre del fichero.
       self.__fichero = filename
       # Líneas del fichero.
       self.__lineas_fichero = []
       # Carga del fichero.
       self.__cargar_fichero()
      
   def __esvacio(self,cadena):
       '''
       Método que devuelve True si la cadena pasada como parámetro
       está vacía y False en caso contrario.
       '''
       if cadena is None: return True
       try:
           if len(str(cadena)) == 0: return True
       except:
           pass
       return False
  
   def __cargar_fichero(self):
       '''
       Carga del fichero en memoria.
       '''
       try:
           # Abrimos el fichero.
           fichero = open(os.path.realpath(self.__fichero),'r')
           seguir = True
       except:
           seguir = False
       if seguir:
           # Volcamos el contenido del fichero a una estructura.
           while True:
               f = fichero.readline()
               if not f: break
               if not self.__esvacio(f):
                   # Quitamos retornos de carro y demás.
                   f = f.replace("\n","")
                   f = f.replace("\r","")
                   f = f.strip()
                   # Lo añadimos a la lista de líneas.
                   self.__lineas_fichero.append(f)
           # Cerramos el fichero.
           fichero.close()
  
   def __posicionar(self, seccion, clave = None):
       '''
       Método para posicionarse en la sección, clave (opcional).
       Devuelve True, posicion de la clave (si encuentra la clave).
       Devuelve True, posición de la sección (si encuentra sección y
       clave = None).
       Devuelve False, -1 (si no encuentra sección).
       Devuelve False, posición de la sección (si no encuentra clave).
       '''    
       # Buscamos la sección..
       encontrado = False
       puntero = 0
       for i in self.__lineas_fichero:
           puntero += 1
           if i.strip() == '['+str(seccion)+']':
               encontrado = True
               break
       if not encontrado: return False, -1
       if clave is not None:
           # Buscamos la clave.
           encontrado = False
           for i in range(puntero,len(self.__lineas_fichero)):
               # Buscamos el carácter '='.
               linea = self.__lineas_fichero[i].split('=')
               if len(linea) == 1:
                   # Nos vamos. La clave no está en esta sección.
                   break
               if len(linea) == 2:
                   # Miramos si es lo que buscamos.
                   if str(linea[0]).strip() == str(clave).strip():
                       # Devolvemos posición.
                       return True, i
           # La clave no existe. Devolvemos posición de la sección.
           return False, puntero
       else:
           # Devolvemos la posición de la sección.
           return True, puntero
      
   def profile(self, seccion, clave, por_defecto = None):
       '''
       Método para obtener valor de clave en sección.
       '''
       # La sección y clave no pueden estar vacíos.
       if self.__esvacio(seccion) or self.__esvacio(clave): return por_defecto
       # Buscamos la clave.
       seguir, posicion = self.__posicionar(seccion, clave)
       if seguir:
           # Obtenemos el valor de la clave.
           linea = self.__lineas_fichero[posicion].split('=')
           try:
               return str(linea[1]).strip()
           except:
               return por_defecto
       else: return por_defecto
      
   def set_profile(self, seccion, clave = None, valor = None):
       '''
       Método para crear secciones y claves (y darles valores).
       '''
       # Si no hay sección, nos vamos.
       if self.__esvacio(seccion): return
       # Incluimos una sección.
       # Si la sección no existe, se crea.
       seguir, posicion = self.__posicionar(seccion)
       if not seguir:
           self.__lineas_fichero.append('['+str(seccion).strip()+']')
       # Asignamos ó incluimos si no existe, el valor
       # de una clave a una sección.
       if not self.__esvacio(clave):
           # Vemos si la (sección,clave) ya existe.
           seguir, posicion = self.__posicionar(seccion,clave)
       # Formateamos valor.
           if valor is None: valor = ''
           # Si existe, damos nuevo valor.
           if seguir:
               self.__lineas_fichero[posicion] = str(clave).strip()+' = '+\
               str(valor).strip()
           else:
               # Si no existe, creamos una nueva clave con su valor.
               if posicion != -1:
                   # Insertamos nueva clave
                   clave_valor = str(clave).strip()+' = '+str(valor).strip()
                   self.__lineas_fichero.insert(posicion,clave_valor)

   def save_profile(self, backup = True):
       '''
       Método para salvar datos en fichero profile. Si backup es True
       se crea una copia de seguridad del mismo. Devuelve True si se
       guardó el fichero y False en caso contrario.
       '''
       # Formamos etiqueta identificación.
       etiqueta = '_backup_'+str(time.time()).strip()
       try:
           if backup:
               # Renombramos fichero.
               os.rename(os.path.realpath(self.__fichero),\
               self.__fichero+etiqueta)
       except: pass
       ret = True
       try:
           # Creamos fichero.
           fichero = open(os.path.realpath(self.__fichero),'w')
           # Guardamos cada una de las líneas.
           for i in self.__lineas_fichero:
               linea = str(i) + '\r\n'
               fichero.write(linea)
           # Cerramos fichero.
           fichero.close()
       except: ret = False
       # Devolvemos estado.
       return ret