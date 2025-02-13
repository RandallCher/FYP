import os
import serial
import csv
import time
from datetime import datetime
import threading
import subprocess

num_TX = 8  # Number of transmitters in the system

device_serials = {
    "Rx_0": "8C21C2E93EEE20A1",
    "Rx_1": "138E03ADCDFEDE9E",
    "Rx_2": "AFFB2A2F74E48031",
}


def get_device_port_by_serial(serial_number):
    try:
        result = subprocess.check_output(["ls /dev/serial/by-id/"], shell=True)
        result = result.decode("utf-8").splitlines()

        for line in result:
            if serial_number in line:
                # Get the full path to the serial port
                port_path = os.path.join("/dev/serial/by-id", line)
                return os.path.realpath(port_path)  # Get the actual /dev/ttyACMx path
    except subprocess.CalledProcessError as e:
        print(f"Error detecting port for serial {serial_number}: {e}")

    return None


def setup_serial(port):
    ser = serial.Serial(port, 9600)  # USB CDC device
    time.sleep(2)  # wait for serial connection to be established
    return ser


def start_collection(ser, device_id):
    ser.write(b"START\n")
    print(f"[RPi] Start command sent to Nano 33 Sense receiver {device_id}.")

    folder_path = "../../../../logs"
    formatted_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    file_name = f"ble_datalog__{device_id}__" + formatted_time + ".csv"
    file_path = os.path.join(folder_path, file_name)

    # Open the CSV file for writing with flush enabled
    with open(file_path, mode="w", newline="", buffering=1) as file:
        writer = csv.writer(file)

        # Write the header row (Transmitter numbers with RSSI, Battery, and Time)
        header = []
        for i in range(num_TX):
            header.append(f"Tx_{i} RSSI")
        writer.writerow(header)

        row_data = [None] * num_TX  # Initialize list for row of data

        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode("utf-8").strip()

                if data == "END":
                    print(
                        f"[RPi, {device_id}] Data collection completed. Ending session."
                    )
                    break
                elif data.startswith("Tx"):
                    print(f"[{device_id}] {data}")

                    # Parse transmitter number, RSSI, and battery values
                    parts = data.split(": ")
                    tx_id = int(parts[0].split("_")[1])  # Extract Tx ID
                    rssi_value = parts[1]

                    # Store RSSI, battery, and timestamp values in row_data
                    row_data[tx_id] = rssi_value

                    # Once row_data is complete, write the row to the CSV and flush
                    if None not in row_data:  # Check if all data is ready
                        writer.writerow(row_data)
                        file.flush()  # Ensure data is written immediately
                        row_data = [None] * (num_TX)  # Reset row for next data
                else:
                    print(f"[{device_id}] {data}")  # Print non-Tx data

    print(f"[RPi, {device_id}] Data saved to {file_path}")


def handle_device(device_id, serial_number):
    port = get_device_port_by_serial(serial_number)
    if port:
        ser = setup_serial(port)
        start_collection(ser, device_id)
    else:
        print(f"[Error] Could not find port for serial {serial_number} ({device_id}).")


if __name__ == "__main__":
    threads = []
    for device_id, serial_number in device_serials.items():
        # Create a separate thread for each device
        thread = threading.Thread(target=handle_device, args=(device_id, serial_number))
        thread.start()
        threads.append(thread)

    # Join the threads (optional, to wait for all threads to complete)
    for thread in threads:
        thread.join()
