import pandas as pd
import os
from datetime import datetime, timedelta
import argparse
import json

def parse_json(value):
    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        raise argparse.ArgumentTypeError(f"Invalid JSON format: {e}")

def get_datetime(prompt):
    while True:
        user_input = input(prompt)
        try:
            dt = datetime.strptime(user_input, "%Y-%m-%d %H:%M:%S")
            return dt
        except ValueError:
            print("Incorrect format. Please enter in 'YYYY-MM-DD HH:MM:SS' format.")

def process_csv(input_path, output_path, start_dt, end_dt):
    # Read the CSV file
    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        print(f"Error reading CSV file '{input_path}': {e}")
        return

    # Display initial columns
    print(f"\nProcessing '{input_path}'")
    print("Initial Columns:", df.columns.tolist())

    # Remove 'BidAskSpread' and 'Variance' if they exist
    cols_to_remove = ['BidAskSpread', 'Variance']
    existing_cols_to_remove = [col for col in cols_to_remove if col in df.columns]
    if existing_cols_to_remove:
        df.drop(columns=existing_cols_to_remove, inplace=True)
        print(f"Removed columns: {existing_cols_to_remove}")
    else:
        print("No columns to remove.")

    # Check if 'Time' column exists
    if 'Time' not in df.columns:
        print("Error: 'Time' column not found in the CSV.")
        return

    # Calculate total number of time steps
    total_steps = len(df)
    print(f"Total time steps in simulation: {total_steps}")

    # Calculate the total simulation duration
    total_duration = end_dt - start_dt
    print(f"Total simulation duration: {total_duration}")

    # Calculate the time delta per step
    delta_per_step = total_duration / total_steps
    print(f"Time delta per step: {delta_per_step}")

    # Generate a list of datetime objects
    df['Datetime'] = [start_dt + i * delta_per_step for i in range(total_steps)]

    # Rearrange columns to place 'Datetime' first
    cols = ['Datetime'] + [col for col in df.columns if col != 'Datetime']
    df = df[cols]

    # Remove the original 'Time' column
    df.drop(columns=['Time'], inplace=True)
    print("Dropped 'Time' column.")

    # Save the processed DataFrame to CSV
    try:
        df.to_csv(output_path, index=False)
        print(f"Processed CSV saved to '{output_path}'")
    except Exception as e:
        print(f"Error saving processed CSV '{output_path}': {e}")
        return

    # Optional: Remove Plotting Prompt and Calls
    # Since plots are no longer desired, these sections are omitted.

def main():
    print("=== Batch Synthetic Market Data Processor ===\n")

    # Define the simulation_output directory
    simulation_output_dir = "simulation_output"

    # Check if the directory exists
    if not os.path.exists(simulation_output_dir):
        print(f"Directory '{simulation_output_dir}' does not exist.")
        return

    # List all CSV files starting with 'simulation_output' in the directory
    all_files = os.listdir(simulation_output_dir)
    simulation_files = [f for f in all_files if f.startswith('simulation_output') and f.endswith('.csv')]

    if not simulation_files:
        print(f"No CSV files starting with 'simulation_output' found in '{simulation_output_dir}'.")
        return

    print(f"Found {len(simulation_files)} simulation CSV file(s) in '{simulation_output_dir}':")
    for f in simulation_files:
        print(f" - {f}")

    # Ask the user whether to use a common simulation period for all files or individual periods
    choice = input("\nDo you want to use the same simulation period for all files? (y/n): ").lower()
    if choice == 'y':
        # Get simulation period once
        print("\nEnter the simulation period for time conversion (applied to all files).")
        start_datetime = get_datetime("Start Date and Time (YYYY-MM-DD HH:MM:SS): ")
        end_datetime = get_datetime("End Date and Time (YYYY-MM-DD HH:MM:SS): ")

        if end_datetime <= start_datetime:
            print("Error: End datetime must be after start datetime.")
            return

        # Process each CSV file
        for file in simulation_files:
            input_path = os.path.join(simulation_output_dir, file)
            model_name = file.replace('simulation_output_', '').replace('.csv', '')
            output_filename = f'process_simulation_output_{model_name}.csv'
            output_path = os.path.join(simulation_output_dir, output_filename)

            process_csv(input_path, output_path, start_datetime, end_datetime)
    else:
        # Process each CSV file with individual simulation periods
        for file in simulation_files:
            input_path = os.path.join(simulation_output_dir, file)
            model_name = file.replace('simulation_output_', '').replace('.csv', '')
            output_filename = f'process_simulation_output_{model_name}.csv'
            output_path = os.path.join(simulation_output_dir, output_filename)

            print(f"\n--- Processing '{file}' ---")
            print("Enter the simulation period for time conversion.")
            start_datetime = get_datetime("Start Date and Time (YYYY-MM-DD HH:MM:SS): ")
            end_datetime = get_datetime("End Date and Time (YYYY-MM-DD HH:MM:SS): ")

            if end_datetime <= start_datetime:
                print("Error: End datetime must be after start datetime. Skipping this file.")
                continue

            process_csv(input_path, output_path, start_datetime, end_datetime)

    print("\nAll files processed successfully.")

if __name__ == "__main__":
    main()
