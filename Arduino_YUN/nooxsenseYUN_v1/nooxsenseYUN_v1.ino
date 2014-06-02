// Comandos posibles por REST:
//poner en navegador http://arduinoyun01/ (o IP_arduinoYUN/arduino/) y a continuacion:
// "digital/13"     -> digitalRead(13)
// "digital/13/1"   -> digitalWrite(13, HIGH)
// "analog/2/123"   -> analogWrite(2, 123)
// "analog/2"       -> analogRead(2)
// "mode/13/input"  -> pinMode(13, INPUT)
// "mode/13/output" -> pinMode(13, OUTPUT)


#include <Bridge.h>
#include <YunServer.h>
#include <YunClient.h>
//#include <Console.h>

// por defecto se activa el servidor HTTP en el puerto 5555
YunServer server;

void setup() {
  Serial.begin(9600);
  /*Console.begin();
  while (!Console){
    ; // wait for Console port to connect.
  }
  Console.println("You're connected to the Console!!!!");
  */
  
  // se inicia Bridge (puente entre procesador Arduino y procesador Linino
  pinMode(13,OUTPUT);
  digitalWrite(13, LOW);
  Bridge.begin();
  digitalWrite(13, HIGH);

  // Escuchar conexiones entrantes solo desde localhost
  // (Nadie desde la red externa se puede conectar)
  server.listenOnLocalhost();
  server.begin();
}

void loop() {
  // Escucha los peticiones clientes procedentes del servidor
  YunClient client = server.accept();

  // hay un nuevo cliente?
  if (client) {
    // procesa la peticion
    process(client);

    // Cierra la conexion y libera recursos.
    client.stop();
  }

  delay(50);
}

void process(YunClient client) {
  // lee la peticion desde final de 192.168.1.114/arduino/ hasta que encuentra otra / y almacena en variable command
  String command = client.readStringUntil('/');

  // es un comando 'digital??
  if (command == "digital") {
    digitalCommand(client);
  }

  // es un comando de un puerto 'analogico'?
  if (command == "analog") {
    analogCommand(client);
  }

  // es un comando de tipo 'mode'?
  if (command == "mode") {
    modeCommand(client);
  }
}

void digitalCommand(YunClient client) {
  int pin, value;

  // leer el PIN al que se refiere el comando
  pin = client.parseInt();

  // Si el proximo caracter es '/' significa que tenemos una URL
  // con un valor parecido a: "/digital/13/1"
  if (client.read() == '/') {
    value = client.parseInt();
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
  /*
  Console.print(F("Pin D"));
  Console.print(pin);
  Console.print(F(" set to "));
  Console.println(value);
  */
  

  // actualiza el datastore key con el actual valor del pin
  String key = "D";
  key += pin;
  Bridge.put(key, String(value));
}

void analogCommand(YunClient client) {
  int pin, value;

   // leer el PIN al que se refiere el comando
  pin = client.parseInt();

  // Si el proximo caracter es '/' significa que tenemos una URL
  // wcon un valor parecido a: "/analog/5/120"
  if (client.read() == '/') {
    // leer el valor y ejecutar el comando
    value = client.parseInt();
    analogWrite(pin, value);

    // enviar respuesta al cliente
    client.print(F("Pin D"));
    client.print(pin);
    client.print(F(" set analogico "));
    client.println(value);

    // actualiza el datastore key con el actual valor del pin
    String key = "D";
    key += pin;
    Bridge.put(key, String(value));
  }
  else {
    // leer pin analogico
    value = analogRead(pin);

    // enviar feedback al cliente
    client.print(F("Pin A"));
    client.print(pin);
    client.print(F(" leyendo analogico "));
    client.println(value);

    // actualiza el datastore key con el actual valor del pin
    String key = "A";
    key += pin;
    Bridge.put(key, String(value));
  }
}

void modeCommand(YunClient client) {
  int pin;

  // leer el numero de pin
  pin = client.parseInt();

  // si el proximo caracter no es  '/' tenemos un error en el URL
  if (client.read() != '/') {
    client.println(F("error"));
    return;
  }

  String mode = client.readStringUntil('\r');

  if (mode == "input") {
    pinMode(pin, INPUT);
    // enviar feedback al cliente
    client.print(F("Pin D"));
    client.print(pin);
    client.print(F(" configurado como INPUT!"));
    return;
  }

  if (mode == "output") {
    pinMode(pin, OUTPUT);
    // enviar feedback al cliente
    client.print(F("Pin D"));
    client.print(pin);
    client.print(F(" configurado como OUTPUT!"));
    return;
  }

  client.print(F("error: modo invalido "));
  client.print(mode);
}
