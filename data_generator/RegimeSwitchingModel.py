import numpy as np
import pandas as pd
from .BaseGenerator import BaseGenerator

class RegimeSwitchingModel(BaseGenerator):

    def __init__(self, S0, regimes, transition_matrix, dt, T, tick_size=0.01):
        """
        Initialize the Regime-Switching model parameters.

        Parameters:
        - S0: Initial stock price
        - regimes: Dictionary of regimes with parameters (e.g., {'bull': {'mu': 0.05, 'sigma': 0.2}})
        - transition_matrix: Markov transition matrix (e.g., [[0.9, 0.1], [0.2, 0.8]])
        - dt: Time step size (e.g., 1/252 for daily data)
        - T: Total simulation time (in years)
        - tick_size: Minimum tick size for the stock price (default 0.01 USD)
        """
        self.S0 = S0
        self.regimes = regimes
        self.transition_matrix = np.array(transition_matrix)
        self.dt = dt
        self.T = T
        self.N = int(T / dt)  # Total number of time steps
        self.num_regimes = len(regimes)
        self.regime_names = list(regimes.keys())
        self.tick_size = tick_size

        # Ensure the transition matrix is valid
        if not np.allclose(self.transition_matrix.sum(axis=1), 1):
            raise ValueError("Each row of the transition matrix must sum to 1.")

        # Ensure tick size is valid
        if self.tick_size < 0.01:
            raise ValueError("Tick size must be at least 0.01 USD")


    def round_to_tick(self, price):
        """
        Round the price to the nearest tick size.
        """
        return round(price / self.tick_size) * self.tick_size

    def generate(self):
        """
        Generate stock prices using the Regime-Switching model with tick size support.
        """
        S = np.zeros(self.N)
        S[0] = self.round_to_tick(self.S0)
        regimes = np.zeros(self.N, dtype=int)

        # Initialize first regime randomly
        current_regime = np.random.choice(self.num_regimes)
        regimes[0] = current_regime

        for t in range(1, self.N):
            # Determine the next regime using the transition matrix
            current_regime = np.random.choice(
                self.num_regimes, p=self.transition_matrix[current_regime]
            )
            regimes[t] = current_regime

            # Get parameters for the current regime
            regime_name = self.regime_names[current_regime]
            mu = self.regimes[regime_name]['mu']
            sigma = self.regimes[regime_name]['sigma']

            # Update stock price
            dW = np.random.normal() * np.sqrt(self.dt)
            new_price = S[t-1] * np.exp((mu - 0.5 * sigma**2) * self.dt + sigma * dW)
            S[t] = self.round_to_tick(new_price)

        return pd.DataFrame({
            'Time': np.linspace(0, self.T, self.N),
            'Price': S,
            'Regime': [self.regime_names[r] for r in regimes]
        })
