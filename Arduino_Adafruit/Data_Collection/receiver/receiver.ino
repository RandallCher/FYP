#include <ArduinoBLE.h>

#define NUM_TX 8

BLEDevice peripheral;

BLEDevice scan_for_device(int i)
{
    const unsigned long timeout = 3000; // 5s timeout in milliseconds
    unsigned long startTime = millis(); // reset the start time for each device

    String deviceName = "Adafruit_" + String(i);

    BLE.scan(); // start scanning for devices

    while (millis() - startTime < timeout)
    {
        if (BLE.scanForName(deviceName))
        {
            peripheral = BLE.available();

            if (peripheral)
                if (peripheral.localName() == deviceName)
                {
                    BLE.stopScan(); // stop scanning once the device is found
                    return peripheral;
                }
        }
    }

    BLE.stopScan();
    BLEDevice empty;
    return empty;
}

void collect_data()
{
    unsigned long startTime = millis();

    Serial.println("[Rx] Starting data collection...");

    for (int k = 0; k < 100; k++) // collect 20 samples each
    {
        for (int i = 0; i < NUM_TX; i++)
        {
            BLEDevice peripheral = scan_for_device(i);                            // scan for device by name
            Serial.println("Tx_" + String(i) + ": " + String(peripheral.rssi())); // send RSSI data to RPi
        }
        delay(100); // wait 0.1s before the next loop iteration
    }
    Serial.println("[Rx] Data collection complete.");
}

void setup()
{
    Serial.begin(9600);
    while (!Serial)
        ;

    if (!BLE.begin())
    {
        Serial.println("[Rx] Failed to initialize BLE!");
        while (1)
            ;
    }

    Serial.println("[Rx] Waiting for start command from Raspberry Pi...");
}

void loop()
{
    // Wait for the start command from RPi
    if (Serial.available())
    {
        String command = Serial.readStringUntil('\n');

        if (command == "START")
        {
            // Collect data
            collect_data();

            // Send end command to RPi
            Serial.println("END");
        }
        else if (command == "STOP")
        {
            Serial.println("[Rx] Received stop command. Exiting...");
            exit(1); // exit the program
        }
    }
}