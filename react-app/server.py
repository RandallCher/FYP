import random
import time
import threading
import serial
import joblib
import numpy as np
import torch
import pandas as pd 

from torch import nn
from flask import Flask, jsonify
from flask_cors import CORS

from common_utils import MLPBuilder  # Importing your model builder

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Serial Port Settings
SERIAL_PORT = "COM3"  # Change to "COM5" for laptop

BAUD_RATE = 9600
PREDICTION_INTERVAL = 2  # Predict every 2 seconds
NUM_TX = 8  # Number of transmitters

# Initialize RSSI data storage
rssi_data = {f"Tx_{i}": 0 for i in range(NUM_TX)}
last_sent_data = rssi_data.copy()
latest_prediction = {"row": None, "column": None}  # Store latest prediction

# Load Pre-trained Model & Scaler
model = MLPBuilder(no_features=NUM_TX, layers=[512, 512, 512, 512])
model_path = "./Deployed_model/DNN_model"
model.load_state_dict(torch.load(f"{model_path}/DNN_model_[512, 512, 512, 512].pth"))
model.eval()
scaler_X = joblib.load(f"{model_path}/scaler_X.pkl")


def read_serial():
    """Continuously read RSSI data from Arduino."""
    global rssi_data
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening on {SERIAL_PORT} for RSSI data...")
            while True:
                line = ser.readline().decode("utf-8").strip()
                if line:
                    print(f"Received: {line}")
                    parts = line.split(": RSSI = ")
                    if len(parts) == 2 and parts[0].startswith("Tx_"):
                        tx_id = parts[0]  # e.g., "Tx_0"
                        try:
                            rssi = int(parts[1])
                            if rssi_data[tx_id] != rssi:
                                rssi_data[tx_id] = rssi
                                print(f"Updated {tx_id}: {rssi}")
                        except ValueError:
                            print(f"Invalid RSSI value: {parts[1]}")
    except serial.SerialException as e:
        print(f"Serial Error: {e}")


def predict_position():
    """Runs prediction every 2 seconds and updates latest_prediction."""
    global latest_prediction
    while True:
        time.sleep(PREDICTION_INTERVAL)

        # Convert RSSI data to a NumPy array and normalize
        rssi_values = np.array([rssi_data[f"Tx_{i}"] for i in range(NUM_TX)]).reshape(1, -1)
        #Debugging step
        # print(f"Raw RSSI values: {rssi_values}")
        rssi_df = pd.DataFrame(rssi_values, columns=[f"Tx_{i} RSSI" for i in range(NUM_TX)])
        rssi_scaled = scaler_X.transform(rssi_df)
        rssi_tensor = torch.tensor(rssi_scaled, dtype=torch.float32)

        with torch.no_grad():
            logits_x, logits_y = model(rssi_tensor)
            pred_x = torch.argmax(logits_x, dim=1).item()
            pred_y = torch.argmax(logits_y, dim=1).item()

        latest_prediction = {"row": pred_x, "column": pred_y}
        print(f"Updated prediction: {latest_prediction}")


# Start Serial Reading & Prediction Threads
serial_thread = threading.Thread(target=read_serial, daemon=True)
prediction_thread = threading.Thread(target=predict_position, daemon=True)

serial_thread.start()
prediction_thread.start()


@app.route("/rssi-values", methods=["GET"])
def get_rssi_values():
    """Returns RSSI values only if they have changed."""
    global last_sent_data
    if last_sent_data != rssi_data:
        last_sent_data = rssi_data.copy()
        return jsonify({"rssi": [last_sent_data[f"Tx_{i}"] for i in range(NUM_TX)]})

    return jsonify({"rssi": None})


@app.route("/receiver-position", methods=["GET"])
def receiver_position():
    """Returns the latest predicted receiver position."""
    return jsonify(latest_prediction)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
