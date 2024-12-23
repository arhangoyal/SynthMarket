import numpy as np
import pandas as pd
from .BaseGenerator import BaseGenerator

class HestonModel(BaseGenerator):
    def __init__(self, S0, V0, mu, kappa, theta, sigma_v, rho, dt, T, tick_size=0.01):
        """
        Initialize the Heston model parameters with tick size support.
        
        Parameters:
        - S0: Initial stock price
        - V0: Initial variance
        - mu: Drift (market trend, can represent bull/bear market)
        - kappa: Speed of mean reversion for variance
        - theta: Long-term mean of variance
        - sigma_v: Volatility of volatility
        - rho: Correlation between stock price and variance
        - dt: Time step size (e.g., 1/252 for daily data)
        - T: Total simulation time (in years)
        - tick_size: Minimum tick size for the stock price (default 0.01 USD)
        """
        if tick_size < 0.01:
            raise ValueError("Tick size must be at least 0.01 USD")
        
        self.S0 = S0
        self.V0 = V0
        self.mu = mu
        self.kappa = kappa
        self.theta = theta
        self.sigma_v = sigma_v
        self.rho = rho
        self.dt = dt
        self.T = T
        self.N = int(T / dt)  # Total number of time steps
        self.tick_size = tick_size

    def round_to_tick(self, price):
        """
        Round the price to the nearest tick size.
        """
        return round(price / self.tick_size) * self.tick_size

    def generate(self):
        """
        Generate stock prices using the Heston model with tick size restrictions.
        """
        # Initialize stock price array
        S = np.zeros(self.N)
        V = np.zeros(self.N)
        S[0], V[0] = self.round_to_tick(self.S0), self.V0

        epsilon = 1e-8  # Stability floor for variance
        min_change = 0.01 * self.tick_size  # Minimum change in price

        for t in range(1, self.N):
            # Correlated Brownian motions
            Z1, Z2 = np.random.normal(size=2)
            W_S = Z1
            W_V = self.rho * Z1 + np.sqrt(1 - self.rho**2) * Z2
            
            # Variance Dynamics: Update variance (V_t)
            scaled_sigma_v = self.sigma_v * np.sqrt(self.dt)
            V[t] = max(V[t-1] + self.kappa * (self.theta - V[t-1]) * self.dt + 
                       scaled_sigma_v * np.sqrt(max(V[t-1], epsilon)) * W_V, epsilon)
            
            # Stock Price Dynamics: Update stock price (S_t)
            scaled_mu = (self.mu - 0.5 * V[t-1]) * self.dt
            scaled_volatility = np.sqrt(max(V[t-1], epsilon)) * np.sqrt(self.dt)
            new_price = S[t-1] * np.exp(scaled_mu + scaled_volatility * W_S)

            # Ensure minimum change in price
            if abs(new_price - S[t-1]) < min_change:
                new_price += np.random.normal(0, min_change)

            # Apply tick size restriction
            S[t] = self.round_to_tick(new_price)

        return pd.DataFrame({'Time': np.linspace(0, self.T, self.N), 'Price': S, 'Variance': V})
