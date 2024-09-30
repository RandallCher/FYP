import serial
import csv
import time
from datetime import datetime

# Configure your serial port and baud rate
serial_port = 'COM3'  # Replace with your port (e.g., '/dev/ttyUSB0' on Linux)
baud_rate = 9600
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'rssi_data_{current_time}.csv'

# Open the serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Allow some time for the connection to establish
time.sleep(2)

# Open the CSV file for writing
with open(output_file, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header
    writer.writerow(['Timestamp', 'RSSI'])

    try:
        while True:
            # Read a line from the serial output
            line = ser.readline().decode('utf-8').strip()
            if line:  # Check if the line is not empty
                print(line)  # Print to console (optional)

                # Parse the line for timestamp and RSSI
                if "Timestamp:" in line and "RSSI:" in line:
                    timestamp = line.split("Timestamp: ")[1].split("ms")[0].strip()  # Extract timestamp
                    rssi = line.split("RSSI: ")[1].split(" ")[0].strip()  # Extract RSSI value

                    # Write to CSV
                    writer.writerow([timestamp, rssi])
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        ser.close()  # Close the serial connection
