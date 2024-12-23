import numpy as np
import pandas as pd
from .BaseGenerator import BaseGenerator

class JumpDiffusionModel(BaseGenerator):
    def __init__(self, S0, mu, sigma, lambda_jump, jump_mean, jump_std, T, dt, tick_size=0.01):
        """
        Initialize the Jump Diffusion model parameters with tick size support.
        
        Parameters:
        - S0: Initial stock price
        - mu: Drift (expected return rate)
        - sigma: Volatility of the stock price
        - lambda_jump: Jump intensity (average number of jumps per year)
        - jump_mean: Mean of the jump size (in log space)
        - jump_std: Standard deviation of the jump size (in log space)
        - T: Total simulation time (in years)
        - dt: Time step size (e.g., 1/252 for daily data)
        - tick_size: Minimum tick size for the stock price (default 0.01 USD)
        """
        if tick_size < 0.01:
            raise ValueError("Tick size must be at least 0.01 USD")
        
        self.S0 = S0
        self.mu = mu
        self.sigma = sigma
        self.lambda_jump = lambda_jump
        self.jump_mean = jump_mean
        self.jump_std = jump_std
        self.T = T
        self.dt = dt
        self.N = int(T / dt)  # Total number of time steps
        self.tick_size = tick_size

    def round_to_tick(self, price):
        """
        Round the price to the nearest tick size.
        """
        return round(price / self.tick_size) * self.tick_size

    def generate(self):
        """
        Generate stock prices using the Jump Diffusion model with tick size restrictions.
        """
        # Initialize stock price array
        S = np.zeros(self.N)
        S[0] = self.round_to_tick(self.S0)

        # Calculate Poisson parameter for jump occurrences
        lambda_dt = self.lambda_jump * self.dt

        # Minimum price change threshold
        min_change = 0.01 * self.tick_size

        for t in range(1, self.N):
            # Generate Brownian motion term (scaled for time step)
            Z = np.random.normal()
            scaled_volatility = self.sigma * np.sqrt(self.dt)
            dW = Z * scaled_volatility

            # Generate jump component
            N_jumps = np.random.poisson(lambda_dt)  # Number of jumps in this time step
            jump = np.sum(np.random.normal(self.jump_mean, self.jump_std, N_jumps))  # Total jump size

            # Update stock price
            scaled_drift = (self.mu - 0.5 * self.sigma**2) * self.dt
            new_price = S[t-1] * np.exp(scaled_drift + dW + jump)

            # Ensure minimum change in price
            if abs(new_price - S[t-1]) < min_change:
                new_price += np.random.normal(0, min_change)

            # Apply tick size restriction
            S[t] = self.round_to_tick(new_price)

        return pd.DataFrame({'Time': np.linspace(0, self.T, self.N), 'Price': S})
