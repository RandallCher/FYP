import random
from flask import Flask, jsonify
from flask_cors import CORS
import serial
import threading

app = Flask(__name__)
CORS(app)

# Load trained model


# Store real-time RSSI values (default all to 127)
NUM_TX = 8
rssi_data = {f"Tx_{i}": 0 for i in range(NUM_TX)}
last_sent_data = rssi_data.copy()  # ✅ FIX: Initialize last_sent_data properly

# Serial port settings
SERIAL_PORT = "COM5"  # Replace with your Arduino's Serial port
BAUD_RATE = 9600

def read_serial():
    """Continuously read Serial data from Arduino and update RSSI values."""
    global rssi_data
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening on {SERIAL_PORT} for RSSI data...")
            while True:
                line = ser.readline().decode("utf-8").strip()
                if line:
                    print(f"Received: {line}")  # Debugging output
                    parts = line.split(": RSSI = ")
                    if len(parts) == 2 and parts[0].startswith("Tx_"):
                        tx_id = parts[0]  # "Tx_0", "Tx_1", etc.
                        try:
                            rssi = int(parts[1])  # Convert RSSI to integer
                            
                            if rssi_data[tx_id] != rssi:  # Only update if new data is different
                                rssi_data[tx_id] = rssi
                                print(f"Updated {tx_id}: {rssi}")
                        except ValueError:
                            print(f"Invalid RSSI value: {parts[1]}")
    except serial.SerialException as e:
        print(f"❌ Serial Error: {e}")

# Start Serial reading in a separate thread
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

@app.route('/rssi-values', methods=['GET'])
def get_rssi_values():
    """API endpoint to get new RSSI values if they have changed."""
    global last_sent_data  # ✅ FIX: Ensure the global variable is used

    # Only send data if there is a change
    if last_sent_data != rssi_data:
        last_sent_data = rssi_data.copy()
        return jsonify({"rssi": [last_sent_data[f"Tx_{i}"] for i in range(NUM_TX)]})
    
    return jsonify({"rssi": None}) 


@app.route('/receiver-position', methods=['GET'])
def receiver_position():
    """API endpoint to simulate receiver position (can be replaced with actual model output)."""
    return jsonify({
        "row": random.random() * 8,
        "column": random.random() * 8
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
