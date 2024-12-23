from .HestonModel import HestonModel
from .JumpDiffusionModel import JumpDiffusionModel
from .HestonModelTickSupported import HestonModelTickSupported
from .RegimeSwitchingModel import RegimeSwitchingModel
from .VarianceGammaModel import VarianceGammaModel

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



    # Initialize HestonModelTickSupported with parameters
    heston_model_tick_supported = HestonModelTickSupported(
        S0=100,  # Initial stock price
        V0=0.04,  # Initial variance
        mu=0.05,  # Drift
        kappa=2,  # Speed of mean reversion
        theta=0.04,  # Long-term mean variance
        sigma_v=0.3,  # Volatility of volatility
        rho=-0.7,  # Correlation
        dt=1/252,  # Time step size for daily data
        T=1,  # Total simulation time (1 year)
        tick_size=0.01  # Minimum tick size in USD
    )

    # Generate data
    data = heston_model_tick_supported.generate()

    # Save to file
    heston_model_tick_supported.save_to_file("heston_tick_supported_data.csv", data)

    # Plot data
    heston_model_tick_supported.plot_data(data, ['Price'], "Heston Model with Tick Size")
    # heston_model_tick_supported.plot_data(data, ['Price', 'Variance'], "Heston Model with Tick Size")



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



    # Test Regime Switching Model
    # Define regimes
    regimes = {
        'bull': {'mu': 0.07, 'sigma': 0.15},  # Bull market
        'bear': {'mu': -0.02, 'sigma': 0.25}  # Bear market
    }

    # Transition matrix (bull -> bull: 90%, bull -> bear: 10%; bear -> bear: 80%, bear -> bull: 20%)
    transition_matrix = [
        [0.9, 0.1],  # From bull
        [0.2, 0.8]   # From bear
    ]

    # Initialize model
    model = RegimeSwitchingModel(
        S0=100,  # Initial stock price
        regimes=regimes,
        transition_matrix=transition_matrix,
        dt=1/252,  # Daily time step
        T=2,  # Total time (2 years)
        tick_size=0.05  # Tick size of 5 cents
    )

    data = model.generate()
    model.save_to_file("regime_switching_tick_data.csv", data)
    model.plot_data(data, ["Price"], "Regime-Switching Model with Tick Size", tick_size=0.05, initial_price=100)



    # Test Variance Gamma Model
    # Initialize the Variance Gamma Model
    vg_model = VarianceGammaModel(
        S0=100,     # Initial stock price
        mu=0.05,    # Drift (expected return rate)
        sigma=0.2,  # Volatility of returns
        nu=0.1,     # Variance rate of the Gamma process
        dt=1/252,   # Daily time step
        T=1,        # Total simulation time (1 year)
        tick_size=0.01  # Tick size of 1 cent
    )
    data = vg_model.generate()
    vg_model.save_to_file("variance_gamma_data.csv", data)
    vg_model.plot_data(data, columns=['Price'], title="Variance Gamma Model Simulation")


