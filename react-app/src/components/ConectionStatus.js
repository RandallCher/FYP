import { useState, useEffect } from "react";
import { getConnectedDevice} from "./bluetooth"; // Ensure correct import path

export default function ConnectionStatus() {
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        const checkConnection = async () => {
            const device = await getConnectedDevice();
            setIsConnected(!!device);
        };

        checkConnection();
        const interval = setInterval(checkConnection, 3000); // Check every 3 seconds

        return () => clearInterval(interval); // Cleanup on unmount
    }, []);

    return (
        <div
            style={{
                display: "inline-block",
                padding: "10px 80px", // Match action-button padding
                backgroundColor: isConnected ? "green" : "red",
                color: "white",
                borderRadius: "8px", // Match action-button border radius
                fontSize: "16px",
                fontWeight: "bold",
                marginTop: "30px", // Match action-button margin-top
            }}
        >
            {isConnected ? "🟢 Connected" : "🔴 Disconnected"}
        </div>  
    );
}
