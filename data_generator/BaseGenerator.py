from abc import ABC, abstractmethod
import pandas as pd
import matplotlib.pyplot as plt
import os

class BaseGenerator(ABC):
    @abstractmethod
    def generate(self):
        """
        Generate the data for the model.
        Must be implemented by all subclasses.
        """
        pass

    def save_to_file(self, filename, data):
        """
        Save generated data to a file in the 'generated_data/' folder.
        
        Parameters:
        - filename: Name of the file to save (e.g., 'data.csv')
        - data: DataFrame containing the generated data
        """
        # Ensure the 'generated_data/' folder exists
        directory = "generated_data"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Full path to the file
        filepath = os.path.join(directory, filename)
        
        # Save the data to the file
        data.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")

    def plot_data(self, data, columns, title):
        """
        Plot the specified columns from the generated data.
        
        Parameters:
        - data: DataFrame containing the generated data
        - columns: List of column names to plot (e.g., ['Price'])
        - title: Title for the plot
        """
        plt.figure(figsize=(12, 6))
        for column in columns:
            plt.plot(data['Time'], data[column], label=column)
        plt.title(title, fontsize=16)
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Value', fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.show()
