import os
import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

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

    def plot_data(self, data, columns, title, tick_size=None, initial_price=None):
        """
        Plot the specified columns from the generated data.
        
        Parameters:
        - data: DataFrame containing the generated data
        - columns: List of column names to plot (e.g., ['Price'])
        - title: Title for the plot
        - tick_size: Tick size in USD (optional, default is None)
        - initial_price: Initial stock price in USD (optional, default is None)
        """
        plt.figure(figsize=(12, 6))
        for column in columns:
            plt.plot(data['Time'], data[column], label=column)
        plt.title(title, fontsize=16)
        plt.xlabel('Time (hours)', fontsize=12)
        plt.ylabel('Stock Value (USD)', fontsize=12)  # Updated y-axis label
        plt.legend()
        plt.grid(True)

        # Add tick size and initial price as annotations
        annotation_text = []
        if tick_size is not None:
            annotation_text.append(f"Tick Size: ${tick_size:.2f}")
        if initial_price is not None:
            annotation_text.append(f"Initial Price: ${initial_price:.2f}")
        
        if annotation_text:
            plt.text(0.95, 0.02, '\n'.join(annotation_text),
                     fontsize=10, color='blue', ha='right', va='bottom',
                     transform=plt.gca().transAxes)

        plt.show()
