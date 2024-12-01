from HestonModel import HestonModel
from JumpDiffusionModel import JumpDiffusionModel

if __name__ == "__main__":

    # Test Heston Model
    heston = HestonModel(
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
    heston_data = heston.generate()
    heston.save_to_file("heston_data.csv", heston_data)
    heston.plot_data(heston_data, ['Price'], "Heston Model Simulation")
    # heston.plot_data(heston_data, ['Price', 'Variance'], "Heston Model Simulation")


    # Test Jump Diffusion Model
    jump_diffusion = JumpDiffusionModel(
        S0=100,  # Initial stock price
        mu=0.05,  # Drift
        sigma=0.2,  # Volatility
        lambda_jump=1,  # Average 1 jump per year
        jump_mean=0.02,  # Mean jump size (2% in log space)
        jump_std=0.1,  # Standard deviation of jump size
        T=1,  # Total simulation time (1 year)
        dt=1/252  # Time step (daily data)
    )
    jump_data = jump_diffusion.generate()
    jump_diffusion.save_to_file("jump_diffusion_data.csv", jump_data)
    jump_diffusion.plot_data(jump_data, ['Price'], "Jump Diffusion Model Simulation")
