from HestonModel import HestonModel

if __name__ == "__main__":
    # Initialize Heston model with parameters
    model = HestonModel(
        S0=100,  # Initial stock price
        V0=0.04,  # Initial variance
        mu=0.05,  # Drift (adjust for bull/bear market)
        kappa=2,  # Speed of mean reversion
        theta=0.04,  # Long-term variance
        sigma_v=0.3,  # Volatility of volatility
        rho=-0.7,  # Correlation between price and variance
        dt=1/252,  # Time step (daily data for 1 year)
        T=1  # Total simulation time (1 year)
    )

    # Generate data
    data = model.generate()

    # Save to file
    filename = "heston_data.csv"
    model.save_to_file(filename, data)

    # Plot the data from the CSV file
    model.plot_data(filename)
