from .HestonModel import HestonModel

'''
Generates stock price data for 1 day with updates every 30 seconds.
'''


if __name__ == "__main__":
    
    # Initialize HestonModelTickSupported with parameters
    heston_model_tick_supported = HestonModel(
        S0=100,  # Initial stock price
        V0=0.04,  # Initial variance
        mu=0.05,  # Drift
        kappa=2,  # Speed of mean reversion
        theta=0.04,  # Long-term mean variance
        sigma_v=0.3,  # Volatility of volatility
        rho=-0.7,  # Correlation
        dt=1 / (24 * 60 * 2),  # Time step size (30 seconds as fraction of a day)
        T=1,  # Total simulation time (1 day)
        tick_size=0.01  # Minimum tick size in USD
    )

    data = heston_model_tick_supported.generate()
    data['Time'] *= 24  # Convert time to hours
    heston_model_tick_supported.save_to_file("heston_tick_supported_30s_data.csv", data)
    heston_model_tick_supported.plot_data(data, ['Price'], "Heston Model with Tick Size at 30-Second Intervals",
                                          tick_size=0.01, initial_price=100)
