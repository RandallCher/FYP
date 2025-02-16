import React, { useState, useEffect } from "react";

const RSSITable = () => {
    const [rssiData, setRssiData] = useState(Array(8).fill(127)); // Default RSSI values

    useEffect(() => {
        const fetchRSSI = async () => {
            try {
                const response = await fetch("http://127.0.0.1:5000/rssi-values");

                if (!response.ok) throw new Error("Failed to fetch RSSI data");

                const data = await response.json();
                
                if (data.rssi && Array.isArray(data.rssi) && data.rssi.length === 8) {
                    setRssiData(data.rssi); // ✅ Update RSSI values
                } else {
                    console.error("Invalid RSSI data format received:", data.rssi);
                }
            } catch (error) {
                console.error("Error fetching RSSI data:", error);
            }
        };

        fetchRSSI();
        const interval = setInterval(fetchRSSI, 2000); // Refresh every 2s

        return () => clearInterval(interval);
    }, []);

    return (
        <div style={{ padding: "20px", textAlign: "center" }}>
            <h2>RSSI Signal Strength</h2>
            <table border="1" style={{ width: "50%", margin: "0 auto" }}>
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
                            <td>{rssi}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default RSSITable;
