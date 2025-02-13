#include <ArduinoBLE.h>

BLEService sensorService("180C"); // Custom BLE Service
BLEIntCharacteristic sensorCharacteristic("2A56", BLERead | BLENotify); // Custom Characteristic

void setup() {
    Serial.begin(115200);
    while (!Serial);

    if (!BLE.begin()) {
        Serial.println("Failed to start BLE!");
        while (1);
    }

    BLE.setLocalName("Nano33BLE");
    BLE.setAdvertisedService(sensorService);
    sensorService.addCharacteristic(sensorCharacteristic);
    BLE.addService(sensorService);
    BLE.advertise();

    Serial.println("BLE device is now advertising...");
}

void loop() {
    BLEDevice central = BLE.central();

    if (central) {
        Serial.println("Connected to: " + central.address());

        while (central.connected()) {
            int sensorValue = analogRead(A0); // Example sensor reading
            sensorCharacteristic.writeValue(sensorValue);
            Serial.println("Sent value: " + String(sensorValue));
            delay(1000);
        }

        Serial.println("Disconnected...");
    }
}
