import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class HestonModel:
    def __init__(self, S0, V0, mu, kappa, theta, sigma_v, rho, dt, T):
        """
        Initialize the Heston model parameters.
        
        Parameters:
        - S0: Initial stock price
        - V0: Initial variance
        - mu: Drift (market trend, can represent bull/bear market)
        - kappa: Speed of mean reversion for variance
        - theta: Long-term mean of variance
        - sigma_v: Volatility of volatility
        - rho: Correlation between stock price and variance
        - dt: Time step size
        - T: Total simulation time (in years)
        """
        self.S0 = S0
        self.V0 = V0
        self.mu = mu
        self.kappa = kappa
        self.theta = theta
        self.sigma_v = sigma_v
        self.rho = rho
        self.dt = dt
        self.N = int(T / dt)  # Total number of time steps

    def generate(self):
        """
        Generate stock prices using the Heston model.
        """
        # Initialize arrays for stock price (S) and variance (V)
        S = np.zeros(self.N)
        V = np.zeros(self.N)
        S[0], V[0] = self.S0, self.V0

        for t in range(1, self.N):
            # Correlated Brownian motions
            Z1, Z2 = np.random.normal(size=2)
            W_S = Z1
            W_V = self.rho * Z1 + np.sqrt(1 - self.rho**2) * Z2
            
            # Update variance (V_t)
            V[t] = V[t-1] + self.kappa * (self.theta - V[t-1]) * self.dt + self.sigma_v * np.sqrt(max(V[t-1], 0)) * np.sqrt(self.dt) * W_V
            V[t] = max(V[t], 0)  # Ensure variance is non-negative
            
            # Update stock price (S_t)
            S[t] = S[t-1] * np.exp((self.mu - 0.5 * V[t-1]) * self.dt + np.sqrt(max(V[t-1], 0)) * np.sqrt(self.dt) * W_S)

        return pd.DataFrame({'Time': np.linspace(0, self.N * self.dt, self.N), 'Price': S, 'Variance': V})

    def save_to_file(self, filename, data):
        """
        Save generated data to a file.
        
        Parameters:
        - filename: Name of the file to save (e.g., 'data.csv')
        - data: DataFrame containing the generated stock price and variance
        """
        data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    @staticmethod
    def plot_data(filename):
        """
        Plot the stock price and variance from a CSV file.
        
        Parameters:
        - filename: Name of the CSV file containing the data
        """
        # Load data from CSV
        data = pd.read_csv(filename)
        
        # Plot stock price
        plt.figure(figsize=(12, 6))
        plt.plot(data['Time'], data['Price'], label='Stock Price', lw=2)
        plt.title('Stock Price Simulation (Heston Model)', fontsize=16)
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Stock Price', fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.show()
        
        # Plot variance
        plt.figure(figsize=(12, 6))
        plt.plot(data['Time'], data['Variance'], label='Variance', color='orange', lw=2)
        plt.title('Variance Simulation (Heston Model)', fontsize=16)
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Variance', fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.show()
