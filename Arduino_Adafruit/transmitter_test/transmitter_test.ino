#include <bluefruit.h>

#define VBATPIN A6

BLEService batteryService = BLEService(0x180F);                           // Battery Service UUID
BLECharacteristic batteryLevelCharacteristic = BLECharacteristic(0x2A19); // Battery Level Characteristic UUID

float measuredvbat;

void setup()
{
    // Initialize Bluefruit
    Bluefruit.begin();
    Bluefruit.setName("Tx_0");
    Bluefruit.setTxPower(0); // set initial Tx power (e.g., +4 dBm)

    // Set params
    Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
    // Bluefruit.Advertising.addTxPower();
    Bluefruit.Advertising.addName();

    // Set up the battery service
    Bluefruit.Advertising.addService(batteryService);
    batteryService.begin();

    // Set up the battery level characteristic
    batteryLevelCharacteristic.setUuid(0x2A19);
    batteryLevelCharacteristic.setProperties(CHR_PROPS_READ);                  // read-only by the central
    batteryLevelCharacteristic.setPermission(SECMODE_OPEN, SECMODE_NO_ACCESS); // readable, but not writable
    batteryLevelCharacteristic.setFixedLen(4);                                 // 4 bytes for a float
    batteryLevelCharacteristic.begin();

    // Update the battery level characteristic with the actual value
    measuredvbat = analogRead(VBATPIN) * 2 * 3.6 / 1024;
    batteryLevelCharacteristic.writeFloat(measuredvbat);

    // Start advertising
    Bluefruit.Advertising.start(0); // do not stop advertising

}

void loop()
{
    // Update the battery level characteristic with the current value
    measuredvbat = analogRead(VBATPIN) * 2 * 3.6 / 1024;
    batteryLevelCharacteristic.writeFloat(measuredvbat);

    delay(500); // update the value periodically
}
