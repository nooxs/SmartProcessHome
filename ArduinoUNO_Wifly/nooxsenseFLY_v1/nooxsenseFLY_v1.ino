// Comandos posibles por REST:
//ejecutar: curl http://IP_arduino/arduino/) y a continuacion:
// "digital/13"     -> digitalRead(13)
// "digital/13/1"   -> digitalWrite(13, HIGH)
// "analog/2/123"   -> analogWrite(2, 123)
// "analog/2"       -> analogRead(2)
// "mode/13/input"  -> pinMode(13, INPUT)
// "mode/13/output" -> pinMode(13, OUTPUT)
#include <SPI.h>
#include <WiFly.h>
#include <EEPROM.h>

WiFlyServer server(80);

void setup() {
  Serial.begin(9600);
  WiFly.begin();

  //pinMode(13,OUTPUT);
  //digitalWrite(13, LOW);
  //digitalWrite(13, HIGH);
  Serial.print("IP:");
  Serial.print(WiFly.ip());
  
  // recupera los valores que tenian los pines digitales antes del fallo de alimentacion
  // posiciones de la EEPROM 0->27
  // posicion (pin*2) -> mode (1:INPUT, 2:OUTPUT)
  // posicion (pin*2+1) -> valor (1:LOW, 2:HIGH)
  recupera();

  server.begin();
  
}

void loop() {
  // Escucha los peticiones clientes procedentes del servidor
  WiFlyClient client= server.available(); //Obtenemos el cliente conectado al servidor
  
  // hay un nuevo cliente?
  if (client) {
    // procesa la peticion
    process(client);

    // Cierra la conexion y libera recursos.
    client.stop();
  }

  delay(50);
}

void process(WiFlyClient client) {
  // lee la peticion desde final de 192.168.1.114/arduino/ hasta que encuentra otra / y almacena en variable command
  String sLinea = client.readString();
  Serial.println(sLinea);
  int iHasta = sLinea.indexOf("HTTP");
  sLinea = sLinea.substring(13,iHasta-1);
  Serial.println("linea: "+sLinea);
  iHasta = sLinea.indexOf("/");
  String command = sLinea.substring(0,iHasta);
  Serial.println("comando: "+command);
  sLinea = sLinea.substring(iHasta+1,sLinea.length());
  Serial.println("resto: "+sLinea); 

  // es un comando 'digital??
  if (command == "digital") {
    digitalCommand(client,sLinea);
  }

  // es un comando de un puerto 'analogico'?
  if (command == "analog") {
    analogCommand(client,sLinea);
  }

  // es un comando de tipo 'mode'?
  if (command == "mode") {
    modeCommand(client,sLinea);
  }
}

void digitalCommand(WiFlyClient client, String sLinea) {
  int pin, value;
  boolean bWrite;
  
  if (sLinea.indexOf("/") > 0)
     bWrite = true;
  else
     bWrite = false;
     
  // leer el PIN al que se refiere el comando
  int iHasta = sLinea.indexOf("/");
  String sPin = sLinea.substring(0,iHasta);
  pin = sPin.toInt();
  Serial.println("----");
  //Serial.print("sPin : ");
  //Serial.println(sPin);
  Serial.print("PIN ->");
  Serial.println(pin);
  //Serial.println("-");
  //Serial.print("bWrite: ");
  //Serial.println(bWrite);
  
  if (bWrite) {
    String sValor = sLinea.substring(iHasta+1,sLinea.length());
    value = sValor.toInt();
    Serial.print("valor a escribir: ");
    Serial.println(value);
    digitalWrite(pin, value);
  } 
  else {
    value = digitalRead(pin);
  }

  // enviar respuesta al cliente
  client.print(F("Pin D"));
  client.print(pin);
  client.print(F(" set to "));
  client.println(value);
  
}

void analogCommand(WiFlyClient client, String sLinea) {
  int pin, value;
  boolean bWrite;
  
  if (sLinea.indexOf("/") > 0)
     bWrite = true;
  else
     bWrite = false;
     
  // leer el PIN al que se refiere el comando
  int iHasta = sLinea.indexOf("/");
  String sPin = sLinea.substring(0,iHasta);
  pin = sPin.toInt();
  Serial.println("----");
  Serial.println(pin);
  Serial.println(bWrite);
 

  // Si el proximo caracter es '/' significa que tenemos una URL
  // wcon un valor parecido a: "/analog/5/120"
  if (bWrite) {
    //String sValor = sLinea.substring(sLinea.indexOf("/")+1,sLinea.length());
    String sValor = sLinea.substring(iHasta+1,sLinea.length());
    value = sValor.toInt();
    Serial.println(value);
    analogWrite(pin, value);

    // enviar respuesta al cliente
    client.print(F("Pin D"));
    client.print(pin);
    client.print(F(" set analogico "));
    client.println(value);

  }
  else {
    // leer pin analogico
    value = analogRead(pin);

    // enviar feedback al cliente
    client.print(F("Pin A"));
    client.print(pin);
    client.print(F(" leyendo analogico "));
    client.println(value);

  }
}

void modeCommand(WiFlyClient client, String sLinea) {
  int pin;

  // leer el numero de pin
  Serial.println(sLinea);
  int iHasta = sLinea.indexOf("/");
  Serial.println(iHasta);
  //String sPin = sLinea.substring(0,sLinea.indexOf("/"));
  String sPin = sLinea.substring(0,iHasta);
  Serial.println(sPin);
  pin = sPin.toInt();
  Serial.println("----");
  Serial.println(pin);
  //hasta aqui OK
  
  String sValor = sLinea.substring(iHasta+1,sLinea.length());
  Serial.println(sValor);
  
  // si el modo es incorrecto
  if (sValor != "input" && sValor != "output"  ) {
    Serial.println("error");
    client.println("error");
    return;
  }

  if (sValor == "input") {
    pinMode(pin, INPUT);
    Serial.println("----i----");
    // enviar feedback al cliente
    client.print(F("Pin D"));
    client.print(pin);
    client.println(F(" configurado como INPUT!"));
    return;
  }

  if (sValor == "output") {
    pinMode(pin, OUTPUT);
    Serial.println("----o----");
    // enviar feedback al cliente
    client.print(F("Pin D"));
    client.print(pin);
    client.println(" configurado como OUTPUT!");
    return;
  }

  client.print(F("error: modo invalido "));
  client.print(sValor);
  Serial.println("error: modo invalido ");
}

void recupera() {
  int x = 0;
  for (int x = 0; x < 14; x++){
    int imode = EEPROM.read(x*2);
    int ivalor = EEPROM.read((x*2)+1);
    switch (imode) {
      case 1:
        pinMode(x,INPUT);
        break;
      case 2:
        pinMode(x,OUTPUT);
        break;
    }
    switch (ivalor) {
      case 1:
        digitalWrite(x, LOW);
        break;
      case 2:
        digitalWrite(x, LOW);
        digitalWrite(x, HIGH);
        break;
    }
  }
  
}
