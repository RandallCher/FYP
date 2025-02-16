let connectedDevice = null;

export const connectToNano33 = async () => {
    try {
        console.log("Requesting Bluetooth device...");
        const device = await navigator.bluetooth.requestDevice({
            acceptAllDevices: true,
            optionalServices: ['12345678-1234-5678-1234-56789abcdef0'] // Update with correct UUID
        });

        console.log("Connecting to GATT server...");
        await device.gatt.connect();
        console.log("Connected to GATT Server");

        console.log("Successfully connected to Nano 33 BLE Sense!");
        
        // Store the connected device globally
        connectedDevice = device;

        // Handle device disconnection
        device.addEventListener("gattserverdisconnected", () => {
            console.log("Device disconnected");
            connectedDevice = null;
        });

        return device; // Return device if needed elsewhere

    } catch (error) {
        console.error("Error connecting to Nano 33 BLE Sense:", error);
    }
};

export const getConnectedDevice = async () => {
    if (connectedDevice && connectedDevice.gatt.connected) {
        return connectedDevice;
    }
    return null;
};

