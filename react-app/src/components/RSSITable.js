import React, { useState, useEffect } from "react";

const RSSITable = () => {
    const [rssiData, setRssiData] = useState(Array(8).fill(127)); // Default RSSI values

    useEffect(() => {
        const fetchRSSI = async () => {
            try {
                const response = await fetch("http://127.0.0.1:5000/rssi-values");
                if (!response.ok) throw new Error("Failed to fetch RSSI data");

                const data = await response.json();
                console.log("Fetched RSSI Data:", data); // Debugging

                if (data.rssi && Array.isArray(data.rssi)) {
                    if (data.rssi.some((rssi, index) => rssi !== rssiData[index])) {
                        setRssiData(data.rssi); // Only update state if there is a change
                    }
                }
            } catch (error) {
                console.error("Error fetching RSSI data:", error);
            }
        };

        const interval = setInterval(fetchRSSI, 2000); // Poll every 2 seconds

        return () => clearInterval(interval);
    }, [rssiData]); // Dependency array ensures state updates only when needed

    return (
        <div style={{ padding: "20px", textAlign: "center" }}>
            <h2>RSSI Signal Strength</h2>
            <table border="1" style={{ width: "50%", margin: "0 auto", borderCollapse: "collapse" }}>
                <thead>
                    <tr>
                        <th>Transmitter</th>
                        <th>RSSI Value</th>
                    </tr>
                </thead>
                <tbody>
                    {rssiData.map((rssi, index) => (
                        <tr key={index}>
                            <td>Tx_{index}</td>
                            <td style={{ color: rssi === 127 ? "gray" : "black" }}>{rssi}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default RSSITable;
