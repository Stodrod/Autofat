from serial_communication import SerialHandler
from data_processing import process_data
import time

def run_test(serial_handler):
    # Send the "START_TEST" command to initiate the test
    serial_handler.send_message("START_TEST")

    # Receive the test data with a timeout
    start_time = time.time()
    timeout_seconds = 5  # Set the desired timeout value in seconds
    data = None
    while time.time() - start_time < timeout_seconds:
        data = serial_handler.receive_message()
        if data is not None:
            break

    if data is None:
        print("Timeout occurred while receiving test data.")
        return None

    # Process the received data
    processed_data = process_data(data)

    # Return the processed data
    return processed_data

def main():
    # Serial communication configuration
    port = "COM3"  # Replace with the appropriate serial port

    # Create a SerialHandler instance
    serial_handler = SerialHandler(port)

    # Connect to the serial port
    serial_handler.connect()

    # Run the test
    result = run_test(serial_handler)

    print("Test Result:", result)

    # Disconnect from the serial port
    serial_handler.disconnect()

if __name__ == "__main__":
    main()