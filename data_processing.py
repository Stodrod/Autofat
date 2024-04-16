import pandas as pd
import os

def process_data(data):
    # Process the received data
    # Perform any necessary data manipulation or analysis
    processed_data = data  # Placeholder, replace with your actual processing logic

    return processed_data

def save_to_csv(data, filename, board_number, p10201_version):
    # Create a DataFrame from the data
    df = pd.DataFrame([data], columns=["Test Result"])
    df["Board Number"] = board_number
    df["P10201 Version"] = p10201_version

    # Check if the file exists
    if os.path.isfile(filename):
        # Append the DataFrame to the existing CSV file
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        # Create a new CSV file and write the DataFrame
        df.to_csv(filename, index=False)