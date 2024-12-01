# Data Generator

The `data_generator/` folder contains implementations of different stock price data generation models. These models simulate realistic financial market data for testing trading strategies, algorithms, or other market analysis tools.

## **Contents**
- **BaseGenerator**: Abstract base class defining a common interface for all data generators.
- **HestonModel**: Stochastic volatility model for simulating stock prices with time-varying volatility.
- **JumpDiffusionModel**: Stock price model incorporating both continuous randomness and sudden jumps to mimic real-world price behavior.

---

## **Models Overview**

### **Abstract Class: BaseGenerator**
The [`BaseGenerator`](BaseGenerator.py) class serves as an abstract base class for all data generation models. It provides:
- A common interface for all models.
- Shared methods for saving and visualizing generated data.

**Key Features:**
- `generate()`: Abstract method that must be implemented by subclasses to generate data.
- `save_to_file(filename, data)`: Saves the generated data to the `generated_data/` folder, creating the folder if it doesn't exist.
- `plot_data(data, columns, title)`: Visualizes specified columns from the generated data.

---

### **1. HestonModel**
The [`HestonModel`](HestonModel.py) simulates stock prices using the Heston stochastic volatility model. It captures the dynamics of both stock prices and time-varying volatility, reflecting real-world market conditions like volatility clustering and the leverage effect.

**Key Features:**
- Generates stock price and variance over time.
- Parameters for mean reversion, volatility of volatility, and correlation between price and variance.

**Equations:**

1. **Stock Price Dynamics**:
   $dS_t = \mu S_t \, dt + \sqrt{V_t} S_t \, dW_t^S$
   - $S_t$: Stock price at time $t$.
   - $\mu$: Drift (expected return rate).
   - $V_t$: Stochastic variance.
   - $W_t^S$: Brownian motion driving the stock price.
2. **Variance Dynamics**:
   $$
   dV_t = \kappa (\theta - V_t) \, dt + \sigma_v \sqrt{V_t} \, dW_t^V
   $$
   - $V_t$: Variance at time $t$.
   - $\kappa$: Speed of mean reversion.
   - $\theta$: Long-term mean variance.
   - $\sigma_v$: Volatility of volatility.
   - $W_t^V$: Brownian motion driving the variance.
3. **Correlation**:
   The two Brownian motions $W_t^S$ and $W_t^V$ are correlated:
   $$
   dW_t^S \cdot dW_t^V = \rho \, dt
   $$
   - $\rho$: Correlation coefficient between the stock price and variance.


### **2. JumpDiffusionModel**
The [`JumpDiffusionModel`](JumpDiffusionModel.py) extends the Geometric Brownian Motion (GBM) model by adding jump components to simulate sudden, large price movements (e.g., due to news or market shocks).

**Key Features:**
- Combines continuous random fluctuations with discrete jumps.
- Parameters for jump intensity, jump size mean, and jump size standard deviation.

**Equations:**
1. **Stock Price Dynamics**:
   $$
   dS_t = \mu S_t \, dt + \sigma S_t \, dW_t + S_t J_t
   $$
   - $S_t$: Stock price at time $t$.
   - $\mu$: Drift (expected return rate).
   - $\sigma$: Volatility of the stock price.
   - $W_t$: Brownian motion driving the continuous randomness.
   - $J_t$: Jump term.
2. **Jump Term ($J_t$)**:
   The jump component is modeled as:
   $$
   J_t = N_t \cdot Y
   $$
   - $N_t$: Poisson process determining the number of jumps.
   - $Y$: Jump size, typically drawn from a normal distribution:
     $$
     Y \sim \mathcal{N}(\text{jump\_mean}, \text{jump\_std})
     $$
3. **Poisson Process**:
   The number of jumps in a time interval $dt$ follows a Poisson distribution:
   $$
   P(N_t = k) = \frac{(\lambda \cdot dt)^k e^{-\lambda \cdot dt}}{k!}
   $$
   - $\lambda$: Average number of jumps per unit time.
