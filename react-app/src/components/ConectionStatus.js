import { useState, useEffect } from "react";

export function SerialStatus() {
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        const checkConnection = async () => {
            try {
                const response = await fetch("http://127.0.0.1:5000/rssi-values");
                if (response.ok) {
                    setIsConnected(true);
                } else {
                    setIsConnected(false);
                }
            } catch (error) {
                setIsConnected(false);
            }
        };

        checkConnection(); // Initial check

        const interval = setInterval(checkConnection, 3000); // Check every second
        return () => clearInterval(interval); // Cleanup function
    }, []);

    return (
        <div
            style={{
                display: "inline-block",
                padding: "10px 80px",
                backgroundColor: isConnected ? "green" : "red",
                color: "white",
                borderRadius: "8px",
                fontSize: "16px",
                fontWeight: "bold",
                marginTop: "30px",
            }}
        >
            {isConnected ? "Server Online" : "Server Offline"}
        </div>
    );
}
