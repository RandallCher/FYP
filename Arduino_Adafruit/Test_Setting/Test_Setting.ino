#include <ArduinoBLE.h>

#define NUM_TX 8 // Number of transmitters
const unsigned long timeout = 3000; // 3s timeout for scanning each device

BLEService sensorService("180C"); // Custom BLE Service
BLEIntCharacteristic sensorCharacteristic("2A56", BLERead | BLENotify); // RSSI characteristic

BLEDevice scan_for_device(int i) {
    unsigned long startTime = millis();
    String deviceName = "ADA_" + String(i);

    BLE.scan();

    while (millis() - startTime < timeout) {
        if (BLE.scanForName(deviceName)) {
            BLEDevice peripheral = BLE.available();
            if (peripheral && peripheral.localName() == deviceName) {
                BLE.stopScan();
                return peripheral; // ✅ Return valid device
            }
        }
    }

    BLE.stopScan();
    return BLEDevice(); // ✅ Return an empty BLEDevice if not found
}

void setup() {
    Serial.begin(9600);
    while (!Serial);  // Wait for Serial to initialize

    Serial.println("Serial initialized...");

    if (!BLE.begin()) {
        Serial.println("Failed to start BLE!");
        while (1);
    }

    BLE.setLocalName("Nano33BLE_Receiver");
    BLE.setAdvertisedService(sensorService);
    sensorService.addCharacteristic(sensorCharacteristic);
    BLE.addService(sensorService);
    BLE.advertise();

    Serial.println("BLE Receiver is now advertising...");
}

void collect_rssi_data() {
    for (int i = 0; i < NUM_TX; i++) {
        int rssiValue = 127; // Default to 127 if device not found

        BLEDevice peripheral = scan_for_device(i); // Scan for device

        if (peripheral) {
            rssiValue = peripheral.rssi();
        }

        sensorCharacteristic.writeValue(rssiValue); // Send RSSI
        Serial.print("Tx_");
        Serial.print(i);
        Serial.print(": RSSI = ");
        Serial.println(rssiValue);
    }
}

void loop() {
    BLEDevice central = BLE.central(); // Check for connection

    if (central) {
        Serial.println("Connected to: " + central.address());

        while (central.connected()) {
            collect_rssi_data(); // Continuously collect and send RSSI data
            delay(1000);
        }

        Serial.println("Disconnected...");
        BLE.advertise();
    } else {
        collect_rssi_data(); // Keep collecting even if no connection
        delay(3000); // Reduce scanning frequency when not connected
    }
}
