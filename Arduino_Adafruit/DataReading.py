import serial
import csv
import re

# Set up serial connection (replace 'COM3' with your actual port)
ser = serial.Serial('COM5', 9600)

# Regular expression to match the Arduino output format
rssi_pattern = re.compile(r'Timestamp: (\d+)ms, RSSI: (-?\d+) dBm')

# Open CSV file for writing
with open('rssi_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp (ms)', 'rssi (dBm)'])  # Write the CSV header

    try:
        while True:
            # Read line from serial input
            line = ser.readline().decode('utf-8').strip()
            print(f"Received: {line}")  # For debugging purposes
            
            # Use regular expression to extract timestamp and rssi values
            match = rssi_pattern.match(line)
            if match:
                timestamp = match.group(1)
                rssi = match.group(2)
                
                # Write data to the CSV file
                writer.writerow([timestamp, rssi])
                
    except KeyboardInterrupt:
        print("Terminating script.")
    finally:
        ser.close()  # Ensure the serial connection is closed
