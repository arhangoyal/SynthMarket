import numpy as np
import pandas as pd
from BaseGenerator import BaseGenerator

class JumpDiffusionModel(BaseGenerator):
    def __init__(self, S0, mu, sigma, lambda_jump, jump_mean, jump_std, T, dt):
        """
        Initialize the Jump Diffusion model parameters.
        
        Parameters:
        - S0: Initial stock price
        - mu: Drift (expected return rate)
        - sigma: Volatility of the stock price
        - lambda_jump: Jump intensity (average number of jumps per year)
        - jump_mean: Mean of the jump size (in log space)
        - jump_std: Standard deviation of the jump size (in log space)
        - T: Total simulation time (in years)
        - dt: Time step size (e.g., 1/252 for daily data)
        """
        self.S0 = S0
        self.mu = mu
        self.sigma = sigma
        self.lambda_jump = lambda_jump
        self.jump_mean = jump_mean
        self.jump_std = jump_std
        self.T = T
        self.dt = dt
        self.N = int(T / dt)  # Total number of time steps

    def generate(self):
        """
        Generate stock prices using the Jump Diffusion model.
        """
        # Initialize stock price array
        S = np.zeros(self.N)
        S[0] = self.S0

        # Calculate Poisson parameter for jump occurrences
        lambda_dt = self.lambda_jump * self.dt

        for t in range(1, self.N):
            # Generate Brownian motion term
            Z = np.random.normal()
            dW = Z * np.sqrt(self.dt)

            # Generate jump component
            N_jumps = np.random.poisson(lambda_dt)  # Number of jumps in this time step
            jump = np.sum(np.random.normal(self.jump_mean, self.jump_std, N_jumps))  # Total jump size

            # Update stock price
            S[t] = S[t-1] * np.exp((self.mu - 0.5 * self.sigma**2) * self.dt + 
                                   self.sigma * dW + jump)

        return pd.DataFrame({'Time': np.linspace(0, self.T, self.N), 'Price': S})
