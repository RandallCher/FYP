let connectedDevice = null;
let gattServer = null;
let rssiCharacteristic = null;
//not used anymore//

// Service and characteristic UUIDs (replace with actual UUIDs from your BLE device)
const SERVICE_UUID = "YOUR_SERVICE_UUID"; 
const RSSI_CHARACTERISTIC_UUID = "YOUR_CHARACTERISTIC_UUID"; 

export async function connectToNano33() {
    try {
        console.log("🔍 Scanning for Arduino Nano 33 BLE...");

        const device = await navigator.bluetooth.requestDevice({
            acceptAllDevices: true,
            optionalServices: [SERVICE_UUID], // Ensure the correct service UUID is included
        });

        console.log("✅ Device found:", device.name);

        device.addEventListener("gattserverdisconnected", () => {
            console.warn("❌ Disconnected from device.");
            connectedDevice = null;
        });

        gattServer = await device.gatt.connect();
        connectedDevice = device;

        const service = await gattServer.getPrimaryService(SERVICE_UUID);
        rssiCharacteristic = await service.getCharacteristic(RSSI_CHARACTERISTIC_UUID);

        console.log("🔗 Connected to:", device.name);
        return device;
    } catch (error) {
        console.error("⚠️ Bluetooth Connection Error:", error);
        return null;
    }
}

export function getConnectedDevice() {
    return connectedDevice;
}

export async function disconnectFromNano33() {
    if (connectedDevice) {
        console.log("🔌 Disconnecting...");
        connectedDevice.gatt.disconnect();
        connectedDevice = null;
    }
}

export async function readRssiValues() {
    if (!connectedDevice || !rssiCharacteristic) {
        console.warn("⚠️ No device connected.");
        return null;
    }

    try {
        const value = await rssiCharacteristic.readValue();
        const decoder = new TextDecoder("utf-8");
        const rssiData = decoder.decode(value);

        console.log("📡 RSSI Data:", rssiData);
        return rssiData; // Example format: "Tx_0,-58\nTx_1,-72\nTx_2,-65"
    } catch (error) {
        console.error("⚠️ Error reading RSSI:", error);
        return null;
    }
}
