/*
en la direccion del navegador poner 192.168.1.124/?LED=F para apagar o LED=T para encender
llamar a http://192.168.1.124  para llamar a la p´gina web
*/

#include <SPI.h>
#include <WiFly.h>

WiFlyServer servidor(80);
//WiFlyClient WebServidor("192.168.1.125/PR201403LedInterruptor_wifly",80);  // cliente del php

int PIN_LED=8;
String readString=String(30);
String state=String(3);
String cabecera="HTTP/1.1 200 OK \n Content-Type: text/html \n"; //necesaria para el envio de datos a la aplicacion

void setup()
{
  //Ethernet.begin(mac, ip); //Inicializamos con las direcciones asignadas
  WiFly.begin();  //Inicializamos el servidor
  pinMode(PIN_LED,OUTPUT);
  Serial.begin(9600);
  digitalWrite(PIN_LED,HIGH);
  state="ON";
  Serial.print("IP:");
  Serial.println(WiFly.ip());
  servidor.begin();
}

void loop()
{
  WiFlyClient cliente= servidor.available(); //Obtenemos el cliente conectado al servidor
  
  if(cliente)
  {
    boolean lineaenblanco=true;
    while(cliente.connected())//Cliente conectado
    {
      if(cliente.available())
      {
        char c=cliente.read();
        if(readString.length()<30)//Leemos petición HTTP caracter a caracter
        {
          readString.concat(c); //Almacenar los caracteres en la variable readString
        }
        if(c=='\n' && lineaenblanco)//Si la petición HTTP ha finalizado
        {
          int LED = readString.indexOf("LED=");
          if(readString.substring(LED,LED+5)=="LED=F")
          {
            /*cliente.println(cabecera);*/
            /*cliente.println(cabecera+"\nEncendido");*/
            digitalWrite(PIN_LED,LOW);
            state="OFF";
            Serial.println(state);
            /* llamar a funcion que graba el dato en PHP del servidor web*/
            /*GrabaEstadoEnPHP(state);*/
            /*
            if(WebServidor.connect()){
              WebServidor.println("GET /add.php?");
              WebServidor.println("estado=");
              WebServidor.println(state);
              WebServidor.println( " HTTP/1.1");
              WebServidor.println( "Host: 192.168.1.125/PR201403LedInterruptor_wifly" );
              WebServidor.println( "Content-Type: application/x-www-form-urlencoded" );
              WebServidor.println( "Connection: close" );
              WebServidor.println();
              WebServidor.println();
            }
            else Serial.println("no conectado a servidor PHP");
            
            WebServidor.stop();
            */
          } else if (readString.substring(LED,LED+5)=="LED=T")
          {
            /*cliente.println(cabecera+"\nApagado");*/
            digitalWrite(PIN_LED,HIGH);
            state="ON";
            Serial.println(state);
            /* llamar a funcion que graba el dato en PHP del servidor web*/
            /*GrabaEstadoEnPHP(state);*/
            /*
            if(WebServidor.connect()){
              WebServidor.println("GET /add.php?");
              WebServidor.println("estado=");
              WebServidor.println(state);
              WebServidor.println( " HTTP/1.1");
              WebServidor.println( "Host: 192.168.1.125/PR201403LedInterruptor_wifly" );
              WebServidor.println( "Content-Type: application/x-www-form-urlencoded" );
              WebServidor.println( "Connection: close" );
              WebServidor.println();
              WebServidor.println();
            }
            else Serial.println("no conectado a servidor PHP");
            
            WebServidor.stop();*/
          }
          
          // si queremos verlo en pagina web
          //Cabecera HTTP estándar
          
          cliente.println("HTTP/1.1 200 OK");
          cliente.println("Content-Type: text/html");
          cliente.println();        
          //Página Web en HTML
          cliente.println("<html>");
          cliente.println("<head>");
          cliente.println("<title>LAMPARA ON/OFF</title>");
          cliente.println("</head>");
          cliente.println("<body width=100% height=100%>");
          cliente.println("<center>");
          cliente.println("<h1>LAMPARA ON/OFF</h1>");
          cliente.print("<br><br>");
          cliente.print("Estado de la lampara: ");
          cliente.print(state);
          cliente.print("<br><br><br><br>");
          cliente.println("<input type=submit value=ON style=width:200px;height:75px onClick=location.href='./?LED=T\'>");
          cliente.println("<input type=submit value=OFF style=width:200px;height:75px onClick=location.href='./?LED=F\'>");
          cliente.println("</center>");
          cliente.println("</body>");
          cliente.println("</html>");
          
          cliente.stop();//Cierro conexión con el cliente
          readString="";
          //delay(1000);
        }
      }
    }
  }
}

