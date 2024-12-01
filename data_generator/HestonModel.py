import numpy as np
import pandas as pd
from BaseGenerator import BaseGenerator

class HestonModel(BaseGenerator):
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
        self.T = T
        self.N = int(T / dt)  # Total number of time steps

    def generate(self):
        """
        Generate stock prices using the Heston model.
        """
        # Initialize stock price array
        S = np.zeros(self.N)
        V = np.zeros(self.N)
        S[0], V[0] = self.S0, self.V0

        epsilon = 1e-8  # Stability floor for variance
        for t in range(1, self.N):
            # Correlated Brownian motions to create correlated noise for W_t^S and W_t^V
            #   - W_t^S: Stock Price Brownian Motion captures the randomness in the stock price movement and introduces unpredictable fluctuations modulated by sqrt(variance)
            #   - W_t^V: Variance Brownian Motion drives the randomness in the variance process and introduced random changes into variance
            Z1, Z2 = np.random.normal(size=2)
            W_S = Z1
            W_V = self.rho * Z1 + np.sqrt(1 - self.rho**2) * Z2
            
            # Variance Dynamics: Update variance (V_t)
            V[t] = max(V[t-1] + self.kappa * (self.theta - V[t-1]) * self.dt + 
                       self.sigma_v * np.sqrt(max(V[t-1], epsilon)) * np.sqrt(self.dt) * W_V, epsilon)
            
            # Stock Price Dynamics: Update stock price (S_t)
            S[t] = S[t-1] * np.exp((self.mu - 0.5 * V[t-1]) * self.dt + 
                                   np.sqrt(max(V[t-1], epsilon)) * np.sqrt(self.dt) * W_S)

        return pd.DataFrame({'Time': np.linspace(0, self.T, self.N), 'Price': S, 'Variance': V})
