# Objective
Design and implement an OPC UA Client that connects to a simulated OPC UA server, reads
dummy tags at regular intervals, and logs the data into hourly spreadsheets.


## Prerequisites:
Before running the client, ensure the following software is installed and configured:

* Python 3.x: The core programming language used.

* python-opcua library: The protocol library for OPC UA communication.

* Unified Automation UA C++ Demo Server: Acts as the simulation server.

* Matrikon OPC UA Explorer: Used for manual tag verification and server browsing.


## Installation & Setup:
Install Python Library: Open your terminal and run the following command:

```pip install opcua```

### Start the Simulator:

* Open the UA C++ Demo Server.

* Ensure the server status is set to "Running".

* Note the endpoint: ```opc.tcp://LAPTOP-LA2AESIK:48010```

### Verify Tags:

* Open Matrikon OPC UA Explorer.

* Connect to the server and browse to Root > Objects > Demo > Dynamic > Scalar.

* Ensure the tags are updating their values in real-time.

## Configuration:
* The source code is pre-configured with the following settings:

    * Endpoint: ```opc.tcp://LAPTOP-LA2AESIK:48010```

* Polling Interval: 60 seconds (1 minute).

* Target Tags: 10 dynamic tags from the Demo.Dynamic.Scalar branch, including Double, Boolean, Int32, and String types.

## Execution:
* Navigate to the folder containing the ```opc_logger.py``` script.

* Run the script via the command line:
```python opc_logger.py```

* The console will display real-time logs, and CSV files will be generated automatically in the same directory.

### Troubleshooting:
* Connection Error: Verify that the server is running and the computer name in the endpoint is correct.

* Access Denied: Ensure the CSV output file is not open in Excel, as Excel locks the file and prevents the script from writing data.

* NaN/Error Values: Check the Matrikon Explorer to ensure the specific Node ID exists and is currently "Good."

