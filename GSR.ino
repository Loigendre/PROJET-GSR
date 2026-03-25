#include <ArduinoBLE.h>

const int GSR = A0;
BLEService gsrService("abcdefab-cdef-1234-5678-abcdefabcdef");

BLEFloatCharacteristic gsrChar("abcdefab-cdef-1234-5678-abcdefabcdea", BLERead | BLENotify);
BLEByteCharacteristic startChar("abcdefab-cdef-1234-5678-abcdefabcdeb", BLEWrite);

bool started = false;
const int SERIAL_CALIBRATION = 520;  // à ajuster selon ton réglage à vide

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!BLE.begin()) {
    Serial.println("❌ BLE init failed");
    while (1);
  }

  BLE.setLocalName("Arduino-GSR");
  BLE.setAdvertisedService(gsrService);

  gsrService.addCharacteristic(gsrChar);
  gsrService.addCharacteristic(startChar);
  BLE.addService(gsrService);

  BLE.advertise();
  Serial.println("🔵 BLE prêt — attente de connexion");
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("📲 Connecté à : ");
    Serial.println(central.address());

    started = false;
    startChar.writeValue(0);

    while (central.connected() && !started) {
      if (startChar.written() && startChar.value() == 1) {
        started = true;
        Serial.println("🚀 Signal reçu → démarrage GSR");
      }
      delay(100);
    }

    while (central.connected() && started) {
      long sum = 0;
      for (int i = 0; i < 10; i++) {
        sum += analogRead(GSR);
        delay(1);
      }
      int gsrValue = sum / 10;

      float resistance = ((1024.0 + 2 * gsrValue) * 10000.0) / (SERIAL_CALIBRATION - gsrValue);
      float conductance_uS = 1e6 / resistance;

      gsrChar.writeValue(conductance_uS);
      Serial.print("📡 GSR (uS): ");
      Serial.println(conductance_uS);

      delay(100);
    }

    Serial.println("❌ Déconnecté");
  }
}
