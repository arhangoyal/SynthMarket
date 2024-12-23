import argparse
from .IntegratedDataGenerator import IntegratedDataGenerator
import matplotlib.pyplot as plt
import pandas as pd
import os
import json


# Helper function to parse JSON strings
def parse_json(value):
    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        raise argparse.ArgumentTypeError(f"Invalid JSON format: {e}")


def simulator():

    # Define command-line arguments
    parser = argparse.ArgumentParser(description='Run Synthetic Market Data Simulation')
    parser.add_argument('--model', type=str, choices=['heston', 'jumpdiffusion', 'regimeswitching', 'variancegamma'], required=True,
                        help='Choose the model to use: heston, jumpdiffusion, regimeswitching, or variancegamma')
    parser.add_argument('--S0', type=float, default=100.0, help='Initial stock price')
    parser.add_argument('--V0', type=float, default=0.04, help='Initial variance (Heston only)')
    parser.add_argument('--mu', type=float, default=0.05, help='Drift (market trend)')
    parser.add_argument('--kappa', type=float, default=1.5, help='Speed of mean reversion (Heston only)')
    parser.add_argument('--theta', type=float, default=0.04, help='Long-term variance mean (Heston only)')
    parser.add_argument('--sigma_v', type=float, default=0.3, help='Volatility of volatility (Heston only)')
    parser.add_argument('--rho', type=float, default=-0.5, help='Correlation between price and variance (Heston only)')
    parser.add_argument('--sigma', type=float, default=0.2, help='Volatility of stock price')
    parser.add_argument('--lambda_jump', type=float, default=0.1, help='Jump intensity (Jump Diffusion only)')
    parser.add_argument('--jump_mean', type=float, default=0.0, help='Mean jump size (Jump Diffusion only)')
    parser.add_argument('--jump_std', type=float, default=0.02, help='Jump size standard deviation (Jump Diffusion only)')
    parser.add_argument('--nu', type=float, default=0.1, help='Variance rate for Variance Gamma model (VarianceGamma only)')
    parser.add_argument('--dt', type=float, default=1/252, help='Time step size')
    parser.add_argument('--T', type=float, default=1.0, help='Total simulation time in years')
    parser.add_argument('--regimes', type=parse_json, default='{"bull": {"mu": 0.07, "sigma": 0.15}, "bear": {"mu": -0.02, "sigma": 0.25}}',
                        help=""" Dictionary of regimes and their parameters in JSON format (Regime-Switching only). Example usage: \--regimes '{"bull": {"mu": 0.10, "sigma": 0.25}, "bear": {"mu": -0.05, "sigma": 0.35}}' """)
    parser.add_argument('--transition_matrix', type=parse_json, default='[[0.9, 0.1], [0.2, 0.8]]',
                        help=""" Transition matrix for regime-switching model in JSON format (Regime-Switching only). Example usage: \--transition_matrix '[[0.85, 0.15], [0.25, 0.75]]' """)
    parser.add_argument('--initial_depth', type=int, default=5, help='Number of levels on each side of the order book')
    parser.add_argument('--max_volume', type=float, default=100.0, help='Max volume for generated orders')
    parser.add_argument('--price_step', type=float, default=0.01, help='Price increment for bids and asks')
    parser.add_argument('--spread_limit', type=float, default=0.05, help='Max distance to remove stale orders')
    parser.add_argument('--depth_levels', type=int, default=5, help='Number of order book levels to record')
    parser.add_argument('--tick_size', type=float, default=0.01, help='Tick size for price updates')

    args = parser.parse_args()

    # Ensure the simulation output directory exists
    output_dir = "simulation_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare parameters based on selected model
    if args.model == 'heston':
        print("Running Heston Model")
        params = {
            'S0': args.S0,
            'V0': args.V0,
            'mu': args.mu,
            'kappa': args.kappa,
            'theta': args.theta,
            'sigma_v': args.sigma_v,
            'rho': args.rho,
            'dt': args.dt,
            'T': args.T,
            'tick_size': args.tick_size,
            'initial_depth': args.initial_depth,
            'max_volume': args.max_volume,
            'price_step': args.price_step,
            'spread_limit': args.spread_limit,
            'depth_levels': args.depth_levels
        }
    elif args.model == 'jumpdiffusion':
        print("Running Jump Diffusion Model")
        params = {
            'S0': args.S0,
            'mu': args.mu,
            'sigma': args.sigma,
            'lambda_jump': args.lambda_jump,
            'jump_mean': args.jump_mean,
            'jump_std': args.jump_std,
            'T': args.T,
            'dt': args.dt,
            'tick_size': args.tick_size,
            'initial_depth': args.initial_depth,
            'max_volume': args.max_volume,
            'price_step': args.price_step,
            'spread_limit': args.spread_limit,
            'depth_levels': args.depth_levels
        }
    elif args.model == 'regimeswitching':
        print("Running Regime Switching Model")
        params = {
            'S0': args.S0,
            'regimes': args.regimes,
            'transition_matrix': args.transition_matrix,
            'dt': args.dt,
            'T': args.T,
            'tick_size': args.tick_size,
            'initial_depth': args.initial_depth,
            'max_volume': args.max_volume,
            'price_step': args.price_step,
            'spread_limit': args.spread_limit,
            'depth_levels': args.depth_levels
        }
    elif args.model == 'variancegamma':
        print("Running Variance Gamma Model")
        params = {
            'S0': args.S0,
            'mu': args.mu,
            'sigma': args.sigma,
            'nu': args.nu,
            'T': args.T,
            'dt': args.dt,
            'tick_size': args.tick_size,
            'initial_depth': args.initial_depth,
            'max_volume': args.max_volume,
            'price_step': args.price_step,
            'spread_limit': args.spread_limit,
            'depth_levels': args.depth_levels
        }

    # Create an instance of the integrated data generator with the chosen model
    generator = IntegratedDataGenerator(
        model_type=args.model,
        **params
    )

    # Run the simulation and get the output DataFrame
    result = generator.run_simulation()

    # Save the result to a CSV file
    output_filename = os.path.join(output_dir, f'simulation_output_{args.model}.csv')
    result.to_csv(output_filename, index=False)
    print(f"Simulation completed. Results saved to {output_filename}")

    # Plotting the Results
    plot_simulation_results(result, args.model, output_dir)


def plot_simulation_results(df: pd.DataFrame, model: str, output_dir: str):
    """
    Generate plots based on the simulation results.

    Parameters:
    - df: pandas DataFrame containing simulation data.
    - model: The model type ('heston', 'jumpdiffusion', 'regimeswitching', or 'variancegamma').
    - output_dir: Directory to save the plots.
    """
    # Set up the plotting style
    plt.style.use('seaborn-v0_8-darkgrid')

    # Plot Time vs Price
    plt.figure(figsize=(12, 6))
    plt.plot(df['Time'], df['Price'], label='Price', color='blue')
    plt.title('Simulated Stock Price Over Time')
    plt.xlabel('Time (Years)')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'price_over_time.png')
    plt.savefig(output_file)
    plt.show()
    print(f"Price plot saved to {output_file}")

    # If Heston Model, plot Time vs Variance
    if model.lower() == 'heston' and 'Variance' in df.columns:
        plt.figure(figsize=(12, 6))
        plt.plot(df['Time'], df['Variance'], label='Variance', color='orange')
        plt.title('Simulated Variance Over Time (Heston Model)')
        plt.xlabel('Time (Years)')
        plt.ylabel('Variance')
        plt.legend()
        plt.tight_layout()
        output_file = os.path.join(output_dir, 'variance_over_time.png')
        plt.savefig(output_file)
        plt.show()
        print(f"Variance plot saved to {output_file}")

    # Plot Bid-Ask Spread Over Time
    if 'BidAskSpread' in df.columns:
        plt.figure(figsize=(12, 6))
        plt.plot(df['Time'], df['BidAskSpread'], label='Bid-Ask Spread', color='green')
        plt.title('Bid-Ask Spread Over Time')
        plt.xlabel('Time (Years)')
        plt.ylabel('Spread')
        plt.legend()
        plt.tight_layout()
        output_file = os.path.join(output_dir, 'bid_ask_spread_over_time.png')
        plt.savefig(output_file)
        plt.show()
        print(f"Bid-Ask spread plot saved to {output_file}")

    # Plot Market Depth at Final Time Step
    final_snapshot = df.iloc[-1]
    bid_prices = [final_snapshot.get(f'BidPrice_{i}', None) for i in range(1, 6)]
    bid_sizes = [final_snapshot.get(f'BidSize_{i}', None) for i in range(1, 6)]
    ask_prices = [final_snapshot.get(f'AskPrice_{i}', None) for i in range(1, 6)]
    ask_sizes = [final_snapshot.get(f'AskSize_{i}', None) for i in range(1, 6)]

    plt.figure(figsize=(10, 6))
    plt.barh(bid_prices, bid_sizes, color='red', label='Bids')
    plt.barh(ask_prices, ask_sizes, color='cyan', label='Asks')
    plt.title('Market Depth at Final Time Step')
    plt.xlabel('Volume')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'market_depth_final.png')
    plt.savefig(output_file)
    plt.show()
    print(f"Market depth plot saved to {output_file}")


if __name__ == "__main__":
    simulator()
