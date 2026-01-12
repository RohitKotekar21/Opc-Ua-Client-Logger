from opcua import Client
import csv
import time
import os
from datetime import datetime


ENDPOINT = "opc.tcp://LAPTOP-LA2AESIK:48010"
INTERVAL_SEC = 60  # Requirement: Read once per minute

# Using your verified path: Demo.Dynamic.Scalar
TAGS = [
    "ns=3;s=Demo.Dynamic.Scalar.Double",    # Tag1
    "ns=3;s=Demo.Dynamic.Scalar.Boolean",   # Tag2
    "ns=3;s=Demo.Dynamic.Scalar.Int32",     # Tag3
    "ns=3;s=Demo.Dynamic.Scalar.DateTime",  # Tag4
    "ns=3;s=Demo.Dynamic.Scalar.Float",     # Tag5
    "ns=3;s=Demo.Dynamic.Scalar.Int16",     # Tag6
    "ns=3;s=Demo.Dynamic.Scalar.UInt32",    # Tag7
    "ns=3;s=Demo.Dynamic.Scalar.Byte",      # Tag8
    "ns=3;s=Demo.Dynamic.Scalar.String",    # Tag9
    "ns=3;s=Demo.Dynamic.Scalar.SByte"      # Tag10 
]

# --------- 2. INITIALIZATION ----------
client = Client(ENDPOINT)

def get_2_hourly_filename():
    """Requirement 4 & 5: Create a new file for every 2-hour block"""
    now = datetime.now()
    # Logic: 0-1 stays '00', 2-3 stays '02', etc.
    hour_block = (now.hour // 2) * 2
    return f"OPC_Log_{now.strftime('%Y-%m-%d')}_{hour_block:02d}.csv"

try:
    print(f"Connecting to {ENDPOINT}...")
    client.connect()
    print("Connected Successfully!")

    # Pre-fetch nodes for continuous automation
    nodes = [client.get_node(tag) for tag in TAGS]
    current_file = ""

    # --------- 3. MAIN AUTOMATION LOOP ----------
    while True:
        now = datetime.now()
        filename = get_2_hourly_filename()

        # Requirement 5: Switch file on the hour change (every 2 hours)
        if filename != current_file:
            current_file = filename
            is_new = not os.path.exists(filename)
            f = open(filename, "a", newline="")
            writer = csv.writer(f)
            
            if is_new:
                # Requirement 4: Specific column headers
                writer.writerow(["Timestamp", "EpochTimeUTC", "Tag1", "Tag2", "Tag3", "Tag4", "Tag5", "Tag6", "Tag7", "Tag8", "Tag9", "Tag10"])
            print(f"--- Logging into 2-hour sheet: {filename} ---")

        # Read Values
        row_values = []
        for n in nodes:
            try:
                v = n.get_value()
                # Clean boolean for the CSV output (True -> 1, False -> 0) if desired
                if isinstance(v, bool): v = int(v)
                row_values.append(v)
            except:
                row_values.append(0)

        # Timestamps
        ts_24hr = now.strftime("%Y-%m-%d %H:%M:%S")
        epoch_utc = int(time.time())

        # Write to CSV and Console in requested format
        writer.writerow([ts_24hr, epoch_utc] + row_values)
        f.flush() # Requirement 5: Continuous logging assurance
        
        # Format for console to match your output example
        print(f"{ts_24hr}, {epoch_utc}, {', '.join(map(str, row_values))}")

        # Requirement 3: Read once per minute
        time.sleep(INTERVAL_SEC)

except Exception as e:
    print(f"Connection Error: {e}")
finally:
    client.disconnect()
    print("Disconnected.")