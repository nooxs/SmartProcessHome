//
// lectura y comprobacion las posiciones 0->25 de la EEPROM
//
#include <EEPROM.h>
int x = 0;

void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);
  delay(5000);
  Serial.println("Leyendo.....");
  delay(2000);  
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int x = 0; x < 28; x++) {
      Serial.print("EEPROM byte: ");
      Serial.println(x);
      Serial.println("->");
      Serial.println(EEPROM.read(x));
      delay(500);
    }
  delay(5000);
}
