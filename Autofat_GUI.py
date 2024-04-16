import customtkinter as ctk
from test_automation import run_test
from serial_communication import SerialHandler
from data_processing import save_to_csv
import datetime
import serial.tools.list_ports
import os

BAUD_RATE = 115200
class AutoFatGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto Fat Test")
        self.geometry("400x450")

        self.board_number_var = ctk.StringVar()
        self.p10201_version_var = ctk.StringVar()
        self.serial_port_var = ctk.StringVar()
        self.status_text = ctk.CTkTextbox(self, height=200, width=350)

        ctk.CTkLabel(self, text="Board Number:").pack(pady=(20, 0))
        ctk.CTkEntry(self, textvariable=self.board_number_var).pack(pady=(0, 10))

        ctk.CTkLabel(self, text="P10201 Version:").pack()
        ctk.CTkEntry(self, textvariable=self.p10201_version_var).pack(pady=(0, 10))

        ctk.CTkLabel(self, text="Serial Port:").pack()
        self.serial_port_dropdown = ctk.CTkComboBox(self, variable=self.serial_port_var, values=self.get_available_ports())
        self.serial_port_dropdown.pack(pady=(0, 20))

        ctk.CTkButton(self, text="Start Auto Fat Test", command=self.start_auto_fat).pack()

        ctk.CTkLabel(self, text="Test Status:").pack(pady=(20, 0))
        self.status_text.pack()

    def get_available_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def start_auto_fat(self):
        board_number = self.board_number_var.get()
        p10201_version = self.p10201_version_var.get()
        selected_port = self.serial_port_var.get()

        self.status_text.delete("1.0", ctk.END)
        self.status_text.insert(ctk.END, f"Starting Auto Fat Test for Board: {board_number}, P10201 Version: {p10201_version}\n\n")

        

        # Create a SerialHandler instance
        serial_handler = SerialHandler(selected_port, BAUD_RATE)

        # Connect to the serial port
        serial_handler.connect()

        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create the CSV file name with Board Number, P10201 Version, and timestamp
        csv_filename = f"AutoFatTest_{board_number}_{p10201_version}_{timestamp}.csv"

        self.status_text.insert(ctk.END, "Running Auto Fat Test...\n")
        self.status_text.update()

        result = run_test(serial_handler)
        if result is None:
            self.status_text.insert(ctk.END, "Test failed: Timeout occurred while receiving test data.\n\n")
        else:
            self.status_text.insert(ctk.END, f"Test Result: {result}\n\n")
            self.status_text.update()

            # Save the test result to the CSV file
            save_to_csv(result, csv_filename, board_number, p10201_version)

            # Print the CSV file location to the text box
            self.status_text.insert(ctk.END, f"CSV file location: {os.path.abspath(csv_filename)}\n")
            self.status_text.update()

        # Disconnect from the serial port
        serial_handler.disconnect()

        self.status_text.insert(ctk.END, "Auto Fat Test Completed.")

if __name__ == "__main__":
    gui = AutoFatGUI()
    gui.mainloop()