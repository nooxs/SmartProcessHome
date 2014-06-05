//
// Inicializa las posiciones 0->25 de la EEPROM
//
#include <EEPROM.h>
int x = 0;

void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);
  delay(5000);
  Serial.println("Inicializando.....");
  delay(2000);
  //if (Serial.available()) {
    for (int x = 0; x < 28; x++) {
      EEPROM.write(x,0);
      Serial.print("EEPROM byte: ");
      Serial.println(x);
      Serial.println("->0");
      delay(500);
    }

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("inicializada EEPROM");
  delay(5000);
}
