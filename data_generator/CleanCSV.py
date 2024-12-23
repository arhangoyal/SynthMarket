import csv
import os
import pandas

def copy_csv_without_first_row(input_file, output_file):
    # Ensure the input file exists
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return

    try:
        with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            # Skip the first row
            next(reader, None)

            # Write all remaining rows to the output file
            for row in reader:
                writer.writerow(row)

        print(f"Successfully copied '{input_file}' to '{output_file}' without the first row.")
    except IOError as e:
        print(f"Error: An I/O error occurred: {e}")
    except csv.Error as e:
        print(f"Error: A CSV error occurred: {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")

import pandas as pd

def remove_specific_columns_from_csv(input_file, output_file):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(input_file)
        
        # Define the columns to remove
        columns_to_remove = ['Price', 'Variance', 'BidAskSpread']
        
        # Drop the specified columns
        df = df.drop(columns=columns_to_remove)
        
        # Save the modified DataFrame to a new CSV file
        df.to_csv(output_file, index=False)
        
        print(f"Successfully removed columns {columns_to_remove} from '{input_file}' and saved to '{output_file}'.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

