import serial
import time
class SerialHandler:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.serial = None
        self.timeout = 2  # Set the timeout in seconds

    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            print(f"Connected to {self.port} at {self.baud_rate} baud")
        except serial.SerialException as e:
            print(f"Error connecting to {self.port}: {str(e)}")

    def disconnect(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            print(f"Disconnected from {self.port}")

    def send_message(self, message):
        if self.serial and self.serial.is_open:
            self.serial.write(message.encode())
            print(f"Sent message: {message}")
        else:
            print("Serial port is not open. Cannot send message.")

    def receive_message(self):
        if self.serial and self.serial.is_open:
            try:
                # Read the raw bytes from the serial port
                message_bytes = self.serial.readline()
                
                # If you expect ASCII data, you can decode using 'latin-1' encoding
                message = message_bytes.decode('latin-1').strip()
                
                # If you expect binary data, you can handle it without decoding
                # message = message_bytes.strip()
                
                print(f"Received message: {message}")
                return message
            except serial.SerialTimeoutException:
                print("Timeout occurred while receiving message.")
                return None
        else:
            print("Serial port is not open. Cannot receive message.")
            return None

    def send_receive_message(self, message):
        self.send_message(message)
        time.sleep(0.1)  # Add a small delay to allow the device to respond
        response = self.receive_message()
        return response