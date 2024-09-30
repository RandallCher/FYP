#include <ArduinoBLE.h>

BLEDevice peripheral;
BLECharacteristic batteryLevelChar;  // Declare this as a global variable
BLECharacteristic batteryChar;         // This will hold the reference to battery level characteristic

const char* batteryServiceUUID = "180F"; // Battery Service UUID
const char* batteryCharUUID = "2A19";    // Battery Level Characteristic UUID
const char* targetDeviceName = "Tx_0";   // Name of your Bluefruit device

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Initialize BLE
  if (!BLE.begin()) {
    Serial.println("Failed to initialize BLE!");
    while (1);
  }

  Serial.println("Scanning for BLE devices...");
  BLE.scan();
}

void loop() {
  // Check if a BLE device is available
  BLEDevice discoveredDevice = BLE.available();

  if (discoveredDevice) {
    if (discoveredDevice.hasLocalName() && discoveredDevice.localName() == targetDeviceName) {
      Serial.print("Found target device: ");
      Serial.println(discoveredDevice.localName());

      // Stop scanning and connect to the device
      BLE.stopScan();

      if (connectToPeripheral(discoveredDevice)) {
        readBatteryLevel();  // Call to read the battery level
        reportRSSI(discoveredDevice);
      }

      
      // Disconnect after reading
      BLE.disconnect();
      Serial.println("Disconnected from the peripheral.");
      delay(1000); // Add a delay of 1 second
      BLE.scan(); // Restart scanning
    }
  }
}

bool connectToPeripheral(BLEDevice peripheral) {
  Serial.println("Connecting to peripheral...");

  if (peripheral.connect()) {
    Serial.println("Connected!");

    // Discover services on the peripheral device
    if (peripheral.discoverService(batteryServiceUUID)) {
      Serial.println("Battery service discovered.");

      // Initialize the batteryChar
      batteryChar = peripheral.characteristic(batteryCharUUID);  // Set the batteryChar variable
      return true;
    } else {
      Serial.println("Battery service not found.");
      return false;
    }
  } else {
    Serial.println("Failed to connect.");
    return false;
  }
}

void readBatteryLevel() {
  // Check if the battery characteristic is available
  if (batteryChar) {
    if (batteryChar.canRead()) {
      byte batteryLevelData[4];  // Create a buffer to hold the 4 bytes (since floats are 4 bytes)
      batteryChar.readValue(batteryLevelData, 4);  // Read the 4 bytes into the buffer

      // Convert the byte array to a float
      float batteryLevel;
      memcpy(&batteryLevel, batteryLevelData, sizeof(batteryLevel));  // Copy the bytes into the float variable

      Serial.print("Battery level: ");
      Serial.println(batteryLevel, 2);  // Print the battery level with 2 decimal points
    }
  } else {
    Serial.println("Battery level characteristic not found.");
  }
}

void reportRSSI(BLEDevice& peripheral) {
    // While connected, report the RSSI every 0.01 second
    while (peripheral.connected()) {
        int rssi = peripheral.rssi();
        Serial.print("RSSI: ");
        Serial.print(rssi);
        Serial.println(" dBm");
        delay(10); // Delay before the next RSSI reading
    }
}
