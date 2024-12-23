# Data Generator

The `data_generator/` folder contains implementations of different stock price data generation models. These models simulate realistic financial market data for testing trading strategies, algorithms, or other market analysis tools.
 <br>
To run any testing script within data_generator: `python -m data_generator.<name of testing script>`. 
Example: `python -m data_generator.test_models`

## **Contents**
- **BaseGenerator**: Abstract base class defining a common interface for all data generators.
- **HestonModelTickSupported**: Stochastic volatility model for simulating stock prices with time-varying volatility.
- **JumpDiffusionModelTickSupported**: Stock price model incorporating both continuous randomness and sudden jumps to mimic real-world price behavior.
- **RegimeSwitchingModel**: Simulates stock prices under different market regimes, such as bull and bear markets.
- **VarianceGammaModel**: Extends the Geometric Brownian Motion (GBM) model to incorporate skewness and kurtosis in return distributions.

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
The [`HestonModelTickSupported`](HestonModelTickSupported.py) simulates stock prices using the Heston stochastic volatility model. It captures the dynamics of both stock prices and time-varying volatility, reflecting real-world market conditions like volatility clustering and the leverage effect.

**Key Features:**
- Generates stock price and variance over time.
- Parameters for mean reversion, volatility of volatility, and correlation between price and variance.

**Equations:**

1. **Stock Price Dynamics**:
   $$dS_t = \mu S_t \, dt + \sqrt{V_t} S_t \, dW_t^S$$
   - $S_t$: Stock price at time $t$.
   - $\mu$: Drift (expected return rate).
   - $V_t$: Stochastic variance.
   - $W_t^S$: Brownian motion driving the stock price.
2. **Variance Dynamics**:
   $$dV_t = \kappa (\theta - V_t) \, dt + \sigma_v \sqrt{V_t} \, dW_t^V$$
   - $V_t$: Variance at time $t$.
   - $\kappa$: Speed of mean reversion.
   - $\theta$: Long-term mean variance.
   - $\sigma_v$: Volatility of the stock price.
   - $W_t^V$: Brownian motion driving the variance.
3. **Correlation**:
   The two Brownian motions $W_t^S$ and $W_t^V$ are correlated:
   $$dW_t^S \cdot dW_t^V = \rho \, dt$$
   - $\rho$: Correlation coefficient between the stock price and variance.


### **2. JumpDiffusionModel**
The [`JumpDiffusionModelTickSupported`](JumpDiffusionModelTickSupported.py) extends the Geometric Brownian Motion (GBM) model by adding jump components to simulate sudden, large price movements (e.g., due to news or market shocks).

**Key Features:**
- Combines continuous random fluctuations with discrete jumps.
- Parameters for jump intensity, jump size mean, and jump size standard deviation.

**Equations:**
1. **Stock Price Dynamics**:
   $$dS_t = \mu S_t \, dt + \sigma S_t \, dW_t + S_t J_t$$
   - $S_t$: Stock price at time $t$.
   - $\mu$: Drift (expected return rate).
   - $\sigma$: Volatility of the stock price.
   - $W_t$: Brownian motion driving the continuous randomness.
   - $J_t$: Jump term.
2. **Jump Term ($J_t$)**:
   The jump component is modeled as:
   $$J_t = N_t \cdot Y$$
   - $N_t$: Poisson process determining the number of jumps.
   - $Y$: Jump size, typically drawn from a normal distribution:
     $Y \sim \mathcal{N}(jump_mean, jump_std)$
3. **Poisson Process**:
   The number of jumps in a time interval $dt$ follows a Poisson distribution:
   $$P(N_t = k) = \frac{(\lambda \cdot dt)^k e^{-\lambda \cdot dt}}{k!}$$
   - $\lambda$: Average number of jumps per unit time.


### **3. RegimeSwitchingModel**
The [`RegimeSwitchingModel`](RegimeSwitchingModel.py) simulates stock prices under different market regimes, such as bull and bear markets. This model uses a Markov process to switch between regimes, each with its own drift and volatility, allowing for more realistic simulation of long-term market behavior.

**Key Features:**
- Simulates market conditions with distinct regimes (e.g., stable, volatile).
- Uses a Markov transition matrix to model regime changes.
- Customizable regime-specific parameters, such as drift and volatility.

**Equations:**
1. **Stock Price Dynamics** (within a regime $r_t$):
   $$dS_t = \mu_{r_t} S_t \, dt + \sigma_{r_t} S_t \, dW_t$$
   - $S_t$: Stock price at time $t$.
   - $\mu_{r_t}$: Drift in regime $r_t$ (expected return rate).
   - $\sigma_{r_t}$: Volatility in regime $r_t$.
   - $W_t$: Brownian motion driving the price fluctuations.

3. **Regime Switching**:
   Regime transitions are governed by a Markov process:
   $$P(r_t = j \,|\, r_{t-1} = i) = p_{ij}$$
   - $P(r_t = j \,|\, r_{t-1} = i)$: Probability of switching from regime $i$ to regime $j$.
   - The probabilities are defined in the Markov **transition matrix**:
     $$
     \mathbf{P} =
     \begin{bmatrix}
     p_{11} & p_{12} & \cdots & p_{1n} \\
     p_{21} & p_{22} & \cdots & p_{2n} \\
     \vdots & \vdots & \ddots & \vdots \\
     p_{n1} & p_{n2} & \cdots & p_{nn}
     \end{bmatrix}
     $$

**Example Parameters**:
- **Regimes**:
  - `bull`: $\mu = 0.07$, $\sigma = 0.15$
  - `bear`: $\mu = -0.02$, $\sigma = 0.25$
- **Transition Matrix**:
  $$
  \mathbf{P} =
  \begin{bmatrix}
  0.9 & 0.1 \\
  0.2 & 0.8
  \end{bmatrix}
  $$
  - $P(\text{bull} \to \text{bull}) = 0.9$
  - $P(\text{bull} \to \text{bear}) = 0.1$
  - $P(\text{bear} \to \text{bull}) = 0.2$
  - $P(\text{bear} \to \text{bear}) = 0.8$

This model is particularly useful for simulating markets with structural shifts or long-term trends, providing a more comprehensive view of potential price trajectories.


### **4. VarianceGammaModel**
The [`VarianceGammaModel`](VarianceGammaModel.py) extends the Geometric Brownian Motion (GBM) model by introducing a Gamma process to model stochastic time changes, allowing for skewness and kurtosis in return distributions.

**Key Features:**
- Captures fat tails (extreme events) and asymmetry in return distributions.
- Parameters for variance rate, drift, and volatility.
- Flexible model for options pricing and financial market analysis.

**Equations:**
1. **Stock Price Dynamics**:
   $$S_t = S_0 \exp \left( (\mu - 0.5 \sigma^2) \nu + \sigma W_{\Gamma_t} \right)$$
   - $S_t$: Stock price at time $t$.
   - $\mu$: Drift (expected return rate).
   - $\sigma$: Volatility of returns.
   - $\nu$: Variance rate (rate of time scaling by the Gamma process).
   - $W_{\Gamma_t}$: Brownian motion evaluated at the Gamma process.

2. **Gamma Process**:
   The time increments are modeled using a Gamma distribution:
   $$\Gamma_t \sim \text{Gamma}(\nu t, \nu)$$
   - $\nu$: Variance rate of the Gamma process.
