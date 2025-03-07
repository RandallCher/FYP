#include <bluefruit.h>

#define VBATPIN A6

BLEService batteryService = BLEService(0x180F);                           // Battery Service UUID
BLECharacteristic batteryLevelCharacteristic = BLECharacteristic(0x2A19); // Battery Level Characteristic UUID

float measuredvbat;

void setup()
{
    Bluefruit.begin();

    // Set params
    Bluefruit.setName("ADA_0"); //Change the name here
    Bluefruit.setTxPower(2); // set to +2dBm

    // Turn off blue LED
    Bluefruit.autoConnLed(false);

    // Set up advertising packet
    Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
    Bluefruit.Advertising.addTxPower();
    Bluefruit.Advertising.addName();
    Bluefruit.Advertising.setInterval(80, 160); // between 50ms and 100ms (interval in units of 0.625ms)
    Bluefruit.Advertising.restartOnDisconnect(true);

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

    delay(100); // update the value periodically
}