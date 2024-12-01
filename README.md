# group_09_project <br> \<market-simulator-generator> <br> Adaptive Synthetic Data Generation for Algorithm Testing in Financial Markets

Testing trading algorithms in financial markets requires data that represents realistic and diverse market conditions. However, relying on historical data has limitations: it is often expensive, biased, and inflexible for evolving algorithm needs. Synthetic data provides an alternative, but traditional methods lack adaptability and realism.

```Python version: 3.9.6```


## Data Generator

The [`data_generator/`](data_generator/) folder contains implementations of different stock price data generation models. These models simulate realistic financial market data for testing trading strategies, algorithms, or other market analysis tools.

Mathematical and usage details for each model are outlined in [data_generator/README.md](data_generator/README.md).

### **Contents**
- [**BaseGenerator**](data_generator/BaseGenerator.py): Abstract base class defining a common interface for all data generators.
- [**HestonModel**](data_generator/HestonModel.py): Stochastic volatility model for simulating stock prices with time-varying volatility.
- [**JumpDiffusionModel**](data_generator/JumpDiffusionModel.py): Stock price model incorporating both continuous randomness and sudden jumps to mimic real-world price behavior.
