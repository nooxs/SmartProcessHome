SmartProcessHome
================

**Primer proyecto raspberry PI + Arduino

Sistema de control
Raspberry Pi con BerriBoot

Funcionalidad:

1.- -ok- recibir información de los distintos dispositivos y almacenarlos en la DB
2.- -pdte- Programación de eventos
3.- -pdte- Lanzar eventos a los actuadores de los diferentes sistemas.

class_profiles.py
Módulo de gestión de ficheros de configuración
crea_profile.py
aplicación de creación de fichero de configuración nooxs.config
/etc/config/nooxs.config
DBMantenimiento.py Aplicación de Gestión de Base de Datos
Python
Fichero de configuracion nooxs.config
en /etc/config
se puede conectar a DB MySQL o a SQLite
conexión en remoto o en local

PYTHON
instalar nuevos módulos: sudo easy-install nuevo_modulo
Upgrade módulos: sudo easy_install --upgrade modulo
Instalar módulos:
html
MySQLdb para conexión a MySQL
sqlite3
python-apache
apt-get install libapache2-mod-python
nano /etc/apache2/Sites_available/default
añadir en Directory /var/www
AddHandler mod_python.py
pythonHandler mod-python .publisher
pythonDebug ON
cambiar AllowOverride none por ALL
/etc/init.d/apache2 restart
WebIDE adafruit
learn.adafruit.com/webide/installation
en navegador: dir_IP:8080
MYSQL

Instalar: (tutorial completo de MySQL+Apache + PHP en http://geekytheory.com/tutorial-raspberry-pi-15-instalacion-de-apache-mysql-php/)
Configuración de accesos remotos
editar /etc/mysql/my.conf modificando la linea bin-address = 127.0.0.0, en la que se debe de indicar desde qué dirección se van a escuchar las peticiones al servidor. Indicaremos la dirección IP del servidor MySQL, o bien 0.0.0.0 para escuchar las peticiones desde cualquier IP.
Para que tenga efecto, hay que reiniciar el servidor mysql: sudo /etc/init.d/mysql restart
hay que cambiar los permisos de usuario con el que se desea acceder desde otros equipos. Lo haremos con el usuario root asignando permisos para cualquier operación:
mysql -u root -p
use mysql;
select user, host from user;
grant all privileges on *.* to root identified by 'tucontraseña';
Al volver a consultar la tabla con los permisos de los usuarios debe aparecer una nueva fila con el usuario root y el host %(cualquier host).

SQLITE
Instalar:
sudo apt-get install sqlite3
sudo apt-get install sqliteman (gestor gráfico)
crear DB en /home/nooxs/nooxsense.db

PHP
Instalar:
sudo apt-get install php5-common php5-cgi fastcgi-php php5
permisos:
sudo chown www-data:www-data /var/www
sudo chmod 775 /var/www
sudo usermod -a -G www-data pi

APACHE
instalar:
permisos:
sudo chown www-data: www-data /var/www
sudo chmod 775 /var/www
sudo usermod -a -G www-data pi
en /etc/sudoers añadir:
www-data ALL=(root) NOPASSWD:ALL
sudo /etc/init.d/apache2 restart
comandos:
/etc/init.d/apache2 [start] [stop] [restart]

Aplicación procesa.py para procesar los estados de los sistemas actuadores/sensores basados en Arduino UNO + Wifly shield. Para los sistemas basados en Arduino YUN, la aplicación procesa.py se ejecuta en el sistema LININO del propio Arduino YUN.

Aplicación de lanzadera de eventos Python arrancada siempre. Un bucle sin fin que lanza los eventos programados. Cada evento es una rutina Python independiente.
Interfaz WEB
Desde el interfaz web se podrá forzar la ejecución de un evento concreto haciendo una llamada a la rutina concreta.
Sistema No-IP para conexión a Internet.
instrucciones en http://www.electroensaimada.com/no-ip.html
apertura de puertos en el router ADSL
TCP 3350
TCP 80

Sistema actuador/sensor
Arduino YUN + Bridge_OK.pdi
directorio /nooxs. Se puede instalar en la propia memoria de la parte LININO de la placa Arduino (en /home/nooxs) o en la tarjeta SD (en /mnt/sda1/nooxs)
procesa.py
crontab:
crontab -e
* * * * * python /mnt/sda1/nooxs/procesa.py
/etc/init.d/cron restart
otros comandos de cron:
stop
start
enable
fichero cron en /etc/crontabs
poner el fichero nooxs.config en /etc/config
dar permisos: chmod 777 /etc/config/nooxs.config
configurar los parámetros de conexión a la base de datos y la IP local del Arduino.
[DB] host - poner la dirección IP del Sistema de Control donde se encuentra la Base de Datos
User - usuario de conexión a la base de datos.
[DB] Pass - password de conexión con la base de datos
[DB] DB - nombre de la base de datos
[miIP] localhost = dirección IP local

procesa.py se encarga de interrogar a la parte Arduino sobre el estado de los pines configurados en la tabla PIN de la base de datos y que se encuentren activos. Si detecta que ha cambiado el estado de alguno de los pines configurados como activo, actualiza el estado en la tabla pin. También genera un registro log de estado de los pines en la tabla registroinstantaneo. La revisión de estado de pines se hace cada minuto.
La revisión del estado de los pines se hace a través de la librería Bridge que es el puente entre la parte Arduino y la parte LININO.

INSTALAR
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


Arduino UNO + Wifly shield + xxxxxx.pdi




SISTEMA de DESARROLLO

Instalar:
MySQL
MySQL-python
I assume you have XCode, it's command line tool, Python and MySQL installed.

Install PIP:

sudo easy_install pip
Edit ~/.profile:

nano ~/.profile
Copy and paste the following two line

export PATH=/usr/local/mysql/bin:$PATH
export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/
Save and exit. Afterwords execute the following command

source  ~/.profile
Install MySQLdb

sudo pip install MySQL-python
To test if everything works fine just try

python -c "import MySQLdb”

