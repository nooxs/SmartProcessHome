
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

**Sistema No-IP**

para conexión a Internet.
instrucciones en <http://www.electroensaimada.com/no-ip.html>
apertura de puertos en el router ADSL

* TCP 3350

* TCP 80

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

