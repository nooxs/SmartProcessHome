SmartProcessHome
================

 Primer proyecto raspberry PI + Arduino
 30/05/2014

***
##Sistema de control (controlsystem)
* Raspberry Pi con BerriBoot

#### Funcionalidad:

1. Recibir información de los distintos dispositivos y almacenarlos en la DB
2. Programación de eventos
3. Lanzar eventos a los actuadores de los diferentes sistemas.

**class_profiles.py**

Módulo de gestión de ficheros de configuración

**crea_profile.py**

aplicación de creación de fichero de configuración nooxs.config

**/etc/config/nooxs.config**

**DBMantenimiento.py**

* Aplicación de Gestión de Base de Datos
* Python
* Fichero de configuracion nooxs.config
en /etc/config
* se puede conectar a DB MySQL o a SQLite
conexión en remoto o en local

**PYTHON**

* instalar nuevos módulos:
	
		sudo easy-install nuevo_modulo
	
* Upgrade módulos:

		sudo easy_install --upgrade modulo
		
* Instalar módulos:
	* html
	* MySQLdb para conexión a MySQL
	* sqlite3
	* python-apache
	
            apt-get install libapache2-mod-python
		
			
			nano /etc/apache2/Sites_available/default
		* añadir en Directory /var/www
		
				AddHandler mod_python.py
				pythonHandler mod-python .publisher
				pythonDebug ON
		* cambiar AllowOverride none por ALL
		
				/etc/init.d/apache2 restart

**WebIDE adafruit**

* <http://learn.adafruit.com/webide/installation>

* en navegador: dir_IP:8080
MYSQL

* Instalar: (tutorial completo de MySQL+Apache + PHP en <http://geekytheory.com/tutorial-raspberry-pi-15-instalacion-de-apache-mysql-php/>)
* Configuración de accesos remotos
	* editar 
	
			/etc/mysql/my.conf 
			
	* modificando la linea bin-address = 127.0.0.0, en la que se debe de indicar desde qué dirección se van a escuchar las peticiones al servidor. Indicaremos la dirección IP del servidor MySQL, o bien 0.0.0.0 para escuchar las peticiones desde cualquier IP.
	* Para que tenga efecto, hay que reiniciar el servidor mysql:
	
			sudo /etc/init.d/mysql restart
	
	* hay que cambiar los permisos de usuario con el que se desea acceder desde otros equipos. Lo haremos con el usuario root asignando permisos para cualquier operación:
	
			mysql -u root -p
			use mysql;
			select user, host from user;
			
			grant all privileges on *.* to root identified by 'tucontraseña';
	* Al volver a consultar la tabla con los permisos de los usuarios debe aparecer una nueva fila con el usuario root y el host %(cualquier host).

**SQLITE**

* Instalar:

		sudo apt-get install sqlite3
		sudo apt-get install sqliteman (gestor gráfico)
		crear DB en /home/nooxs/nooxsense.db

**PHP**

* Instalar:

		sudo apt-get install php5-common php5-cgi fastcgi-php php5
	* permisos:

			sudo chown www-data:www-data /var/www
			sudo chmod 775 /var/www
			sudo usermod -a -G www-data pi

**APACHE**

* instalar:
* permisos:

		sudo chown www-data: www-data /var/www
		sudo chmod 775 /var/www
		sudo usermod -a -G www-data pi
		
	* en /etc/sudoers añadir:
	
			www-data ALL=(root) NOPASSWD:ALL
			sudo /etc/init.d/apache2 restart
		
* comandos:

		/etc/init.d/apache2 [start] [stop] [restart]

**Aplicación procesa.py**

para procesar los estados de los sistemas actuadores/sensores basados en Arduino UNO + Wifly shield. Para los sistemas basados en Arduino YUN, la aplicación procesa.py se ejecuta en el sistema LININO del propio Arduino YUN.

Aplicación de lanzadera de eventos Python arrancada siempre. Un bucle sin fin que lanza los eventos programados. Cada evento es una rutina Python independiente.

**Interfaz WEB**

Desde el interfaz web se podrá forzar la ejecución de un evento concreto haciendo una llamada a la rutina concreta.

**Sistema No-IP**

para conexión a Internet.
instrucciones en <http://www.electroensaimada.com/no-ip.html>
apertura de puertos en el router ADSL

* TCP 3350

* TCP 80

**Base de datos nooxsense.db**


* dispositivos

campo            | tipo       | PK   |
-----------------|------------|------|
cod_dispositivo  |Int         |YES   |
nom_dispositivo  |varchar(30) |      |
MAC_dispositivo  |varchar(17) |      |
IP_dispositivo   |varchar(15) |      |
clave_dispositivo|varchar(30) |      |
activo           |int         |      |


* Pin

campo                   | tipo       | PK   |
------------------------|------------|------|
cod_dispositivo         |int         |      |
PIN_num                 |varchar(2)  |YES   |
PIN_tipo                |varchar(1)  |      |
PIN_valor_desde         |int         |      |
PIN_valor_hasta         |int         |      |
PIN_nombre              |varchar(30) |      |
activo                  |int         |      |
fechahora_actualizacion |datetime    |      |
valor_actual            |int         |      |


* Configuracion

campo            | tipo       | PK   |
-----------------|------------|------|
cod_parametro    |int         |YES   |
nom_parametro    |varchar(30) |      |
valor_parametro  |varchar(30) |      |
notas_parametro  |varchar(50) |      |


* errorlog

campo            | tipo       | PK   |
-----------------|------------|------|
MAC_dispositivo  |varchar(17) |      |
IP_dispositivo   |varchar(15) |      |
error            |varchar(50) |      |
fechahora        |datetime    |      |


* Tabla RegistroInstantaneo

campo            | tipo       | PK   |
-----------------|------------|------|
cod_dispositivo  |int         |      |
fechahora        |datetime    |      |
PIN_num          |varchar(2)  |      |
PIN_valor        |int         |      |


* Tabla RegistroPermanente

campo            | tipo       | PK   |
-----------------|------------|------|
cod_dispositivo  |varchar(17) |      |
PIN_num          |varchar(2)  |      |
mediayear        |int         |      |
media01          |int         |      |
media02          |int         |      |
media03          |int         |      |
media04          |int         |      |
media05          |int         |      |
media06          |int         |      |
media07          |int         |      |
media08          |int         |      |
media09          |int         |      |
media10          |int         |      |
media11          |int         |      |
media12          |int         |      |



***
##Sistema actuador/sensor (sensorsystem)

###Arduino YUN + Bridge_OK.pdi

**directorio /nooxs**

Se puede instalar en la propia memoria de la parte LININO de la placa Arduino (en /home/nooxs) o en la tarjeta SD (en /mnt/sda1/nooxs)

**procesa.py**
**crontab:**

	crontab -e
		* * * * * python /mnt/sda1/nooxs/procesa.py
	/etc/init.d/cron [restart] [stop][start][enable]
	
*fichero cron en /etc/crontabs*

* poner el fichero nooxs.config en /etc/config
* dar permisos: 

		chmod 777 /etc/config/nooxs.config
			
* configurar los parámetros de conexión a la base de datos y la IP local del Arduino.

		[DB] host - poner la dirección IP del Sistema de Control donde se encuentra la Base de Datos
		User - usuario de conexión a la base de datos.
		[DB] Pass - password de conexión con la base de datos
		[DB] DB - nombre de la base de datos
		[miIP] localhost = dirección IP local

**procesa.py**

se encarga de interrogar a la parte Arduino sobre el estado de los pines configurados en la tabla PIN de la base de datos y que se encuentren activos. Si detecta que ha cambiado el estado de alguno de los pines configurados como activo, actualiza el estado en la tabla pin. También genera un registro log de estado de los pines en la tabla registroinstantaneo. La revisión de estado de pines se hace cada minuto.

La revisión del estado de los pines se hace a través de la librería Bridge que es el puente entre la parte Arduino y la parte LININO.

**INSTALAR**

	opkg update (para actualizar los paquetes)
	nano
	opkg install nano
	vi /etc/profile
	añadir primera linea de la lista export
		export TERM=xterm-color
	opkg install mc
	opkg openssh-sftp-server
	opkg python-mysql
	opkg sqlite3
	opkg python-sqlite3


###Arduino UNO + Wifly shield + xxxxxx.pdi



***
##SISTEMA de DESARROLLO (devsystem)

* Instalar:

		MySQL
		MySQL-python
Asumimos que tenemos instalado X Code, y por lo tanto tenemos instalado Python.

Instalar PIP:

	sudo easy_install pip
	Edit ~/.profile:

	nano ~/.profile
copiar y pegar las siguientes dos lineas

	export PATH=/usr/local/mysql/bin:$PATH
	export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/
Salvar y salir. 

Ejecutar:

	source  ~/.profile
	Install MySQLdb

	sudo pip install MySQL-python

Para probar si todo funciona bien:

	python -c "import MySQLdb”

