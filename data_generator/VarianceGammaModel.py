import numpy as np
import pandas as pd
from .BaseGenerator import BaseGenerator

class VarianceGammaModel(BaseGenerator):
    def __init__(self, S0, mu, sigma, nu, dt, T, tick_size=0.01):
        """
        Initialize the Variance Gamma model parameters.

        Parameters:
        - S0: Initial stock price
        - mu: Drift (expected return rate)
        - sigma: Volatility of returns
        - nu: Variance rate of the Gamma process
        - dt: Time step size
        - T: Total simulation time (in years)
        - tick_size: Minimum tick size for stock price updates
        """
        if nu <= 0:
            raise ValueError("The 'nu' parameter must be positive and non-zero.")
        self.S0 = S0
        self.mu = mu
        self.sigma = sigma
        self.nu = nu
        self.dt = dt
        self.T = T
        self.N = int(T / dt)  # Total number of time steps
        self.tick_size = tick_size

        if self.tick_size < 0.01:
            raise ValueError("Tick size must be at least 0.01 USD")
    
    def round_to_tick(self, price):
        """
        Round the price to the nearest tick size.
        """
        return round(price / self.tick_size) * self.tick_size

    def generate(self):
        """
        Generate stock prices using the Variance Gamma model.
        """
        # Initialize stock price array
        S = np.zeros(self.N)
        S[0] = self.round_to_tick(self.S0)

        # Generate Gamma increments
        gamma_increments = np.random.gamma(shape=self.dt / self.nu, scale=self.nu, size=self.N - 1)

        # Generate Brownian motion increments evaluated at Gamma times
        W_gamma = np.random.normal(loc=0, scale=1, size=self.N - 1)

        # Minimum threshold for price change
        min_change = 0.01 * self.tick_size

        # Simulate the price path
        for t in range(1, self.N):
            drift_term = (self.mu - 0.5 * self.sigma**2) * gamma_increments[t - 1]
            diffusion_term = self.sigma * np.sqrt(self.dt) * W_gamma[t - 1]
            new_price = S[t - 1] * np.exp(drift_term + diffusion_term)

            # Ensure minimum change in price
            if abs(new_price - S[t - 1]) < min_change:
                new_price += np.random.normal(0, min_change)

            S[t] = self.round_to_tick(new_price)

        # Create DataFrame for output
        return pd.DataFrame({
            'Time': np.linspace(0, self.T, self.N),
            'Price': S
        })
