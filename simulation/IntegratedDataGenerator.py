from OrderBook.OrderBook import OrderBook
from data_generator.HestonModel import HestonModel
from data_generator.JumpDiffusionModel import JumpDiffusionModel
from data_generator.RegimeSwitchingModel import RegimeSwitchingModel
from data_generator.VarianceGammaModel import VarianceGammaModel
import random
import numpy as np
import pandas as pd

class IntegratedDataGenerator:
    def __init__(self, model_type, **kwargs):
        """
        Initialize the Integrated Data Generator with the specified model.
        
        Parameters:
        - model_type: 'heston', 'jumpdiffusion', 'regimeswitching', or 'variancegamma'
        - kwargs: Parameters required for the chosen model and simulation, including:
            'S0', 'V0' (for Heston),
            'mu', 'kappa', 'theta', 'sigma_v', 'rho' (for Heston),
            'lambda_jump', 'jump_mean', 'jump_std' (for JumpDiffusion),
            'regimes', 'transition_matrix' (for RegimeSwitching),
            'nu' (for VarianceGamma),
            'dt', 'T', 'tick_size', 'initial_depth', 'max_volume', 
            'price_step', 'spread_limit', 'depth_levels'
        """
        self.model_type = model_type.lower()
        self._validate_params(kwargs)
        
        # Initialize the chosen model
        self.model = self._initialize_model(self.model_type, **kwargs)
        
        # Order book parameters with default values
        self.order_book = OrderBook()
        self.initial_depth = kwargs.get('initial_depth', 5)
        self.max_volume = kwargs.get('max_volume', 100)
        self.price_step = kwargs.get('price_step', 0.01)
        self.spread_limit = kwargs.get('spread_limit', 0.05)
        self.depth_levels = kwargs.get('depth_levels', 5)
        self.tick_size = kwargs['tick_size']

    def _validate_params(self, params):
        """
        Validate input parameters to ensure all required parameters are present and valid.
        """
        required_common = ['tick_size', 'initial_depth', 'max_volume', 
                           'price_step', 'spread_limit', 'depth_levels']
        for param in required_common:
            if param not in params:
                raise ValueError(f"Missing common parameter '{param}'")
            if not isinstance(params[param], (int, float)) or params[param] <= 0:
                raise ValueError(f"Parameter '{param}' must be a positive number")
        
        if 'dt' not in params or 'T' not in params:
            raise ValueError("Missing 'dt' or 'T' parameter for simulation time settings")
        if not isinstance(params['dt'], (int, float)) or params['dt'] <= 0:
            raise ValueError("Parameter 'dt' must be a positive number")
        if not isinstance(params['T'], (int, float)) or params['T'] <= 0:
            raise ValueError("Parameter 'T' must be a positive number")

    def _initialize_model(self, model_type, **kwargs):
        """
        Initialize the selected financial model with the provided parameters.
        """
        if model_type == 'heston':
            required_params = ['S0', 'V0', 'mu', 'kappa', 'theta', 'sigma_v', 'rho', 'dt', 'T', 'tick_size']
            for param in required_params:
                if param not in kwargs:
                    raise ValueError(f"Missing parameter '{param}' for HestonModel")
            return HestonModel(
                S0=kwargs['S0'], V0=kwargs['V0'], mu=kwargs['mu'],
                kappa=kwargs['kappa'], theta=kwargs['theta'],
                sigma_v=kwargs['sigma_v'], rho=kwargs['rho'],
                dt=kwargs['dt'], T=kwargs['T'], tick_size=kwargs['tick_size']
            )
        elif model_type == 'jumpdiffusion':
            required_params = ['S0', 'mu', 'sigma', 'lambda_jump', 'jump_mean', 'jump_std', 'T', 'dt', 'tick_size']
            for param in required_params:
                if param not in kwargs:
                    raise ValueError(f"Missing parameter '{param}' for JumpDiffusionModel")
            return JumpDiffusionModel(
                S0=kwargs['S0'], mu=kwargs['mu'], sigma=kwargs['sigma'],
                lambda_jump=kwargs['lambda_jump'], jump_mean=kwargs['jump_mean'],
                jump_std=kwargs['jump_std'], T=kwargs['T'], dt=kwargs['dt'],
                tick_size=kwargs['tick_size']
            )
        elif model_type == 'regimeswitching':
            required_params = ['S0', 'regimes', 'transition_matrix', 'dt', 'T', 'tick_size']
            for param in required_params:
                if param not in kwargs:
                    raise ValueError(f"Missing parameter '{param}' for RegimeSwitchingModel")
            return RegimeSwitchingModel(
                S0=kwargs['S0'],
                regimes=kwargs['regimes'],
                transition_matrix=kwargs['transition_matrix'],
                dt=kwargs['dt'],
                T=kwargs['T'],
                tick_size=kwargs['tick_size']
            )
        elif model_type == 'variancegamma':
            required_params = ['S0', 'mu', 'sigma', 'nu', 'dt', 'T', 'tick_size']
            for param in required_params:
                if param not in kwargs:
                    raise ValueError(f"Missing parameter '{param}' for VarianceGammaModel")
            return VarianceGammaModel(
                S0=kwargs['S0'], mu=kwargs['mu'], sigma=kwargs['sigma'],
                nu=kwargs['nu'], dt=kwargs['dt'], T=kwargs['T'], tick_size=kwargs['tick_size']
            )
        else:
            raise ValueError("Invalid model_type. Choose 'heston', 'jumpdiffusion', 'regimeswitching', or 'variancegamma'")

    def initialize_order_book(self):
        """
        Initialize the order book around the initial price S0 with random volumes,
        ensuring all prices align with the tick size and maintaining initial depth.
        """
        start_price = self.model.round_to_tick(self.model.S0)

        # Create initial bids below S0
        for i in range(1, self.initial_depth + 1):
            bid_price = self.model.round_to_tick(start_price - self.price_step * i)
            bid_size = random.uniform(1, self.max_volume)
            self.order_book.add_bid(bid_price, bid_size)

        # Create initial asks above S0
        for i in range(1, self.initial_depth + 1):
            ask_price = self.model.round_to_tick(start_price + self.price_step * i)
            ask_size = random.uniform(1, self.max_volume)
            self.order_book.add_ask(ask_price, ask_size)

    def update_order_book(self, current_price):
        """
        Update the order book given the new price from the chosen model,
        ensuring all new orders align with the tick size and maintaining market depth.
        """
        # Remove stale bids outside the spread limit
        for bid_price in list(self.order_book.bid_volume.keys()):
            if (current_price - bid_price) > self.spread_limit:
                self.order_book.remove_bid(bid_price, self.order_book.bid_volume[bid_price])

        # Remove stale asks outside the spread limit
        for ask_price in list(self.order_book.ask_volume.keys()):
            if (ask_price - current_price) > self.spread_limit:
                self.order_book.remove_ask(ask_price, self.order_book.ask_volume[ask_price])

        # Maintain depth by adding new bids if needed
        current_bids = sorted(self.order_book.bid_volume.keys(), reverse=True)
        new_bid_index = len(current_bids) + 1  # Start indexing for new bids
        while len(current_bids) < self.depth_levels:
            new_bid_price = self.model.round_to_tick(current_price - self.price_step * new_bid_index)
            # Ensure the new bid price is unique and not already in the bid_volume
            if new_bid_price not in self.order_book.bid_volume:
                bid_size = random.uniform(1, self.max_volume)
                self.order_book.add_bid(new_bid_price, bid_size)
                current_bids = sorted(self.order_book.bid_volume.keys(), reverse=True)
            # Increment the index for the next bid price calculation
            new_bid_index += 1

            # Maintain depth by adding new asks if needed
        current_asks = sorted(self.order_book.ask_volume.keys())
        new_ask_index = len(current_asks) + 1  # Start indexing for new asks
        while len(current_asks) < self.depth_levels:
            new_ask_price = self.model.round_to_tick(current_price + self.price_step * new_ask_index)
            # Ensure the new ask price is unique and not already in the ask_volume
            if new_ask_price not in self.order_book.ask_volume:
                ask_size = random.uniform(1, self.max_volume)
                self.order_book.add_ask(new_ask_price, ask_size)
                current_asks = sorted(self.order_book.ask_volume.keys())
            # Increment the index for the next ask price calculation
            new_ask_index += 1


        # Ensure that we have at least depth_levels of bids and asks within spread limits
        # Remove bids that are above current price or violate spread limit
        for bid_price in list(self.order_book.bid_volume.keys()):
            if bid_price > current_price or (current_price - bid_price) > self.spread_limit:
                self.order_book.remove_bid(bid_price, self.order_book.bid_volume[bid_price])

        # Remove asks that are below current price or violate spread limit
        for ask_price in list(self.order_book.ask_volume.keys()):
            if ask_price < current_price or (ask_price - current_price) > self.spread_limit:
                self.order_book.remove_ask(ask_price, self.order_book.ask_volume[ask_price])

            # After removals, ensure depth_levels are maintained
        # Re-add if necessary

        # Maintain bids
        current_bids = sorted(self.order_book.bid_volume.keys(), reverse=True)
        new_bid_index = len(current_bids) + 1
        while len(current_bids) < self.depth_levels:
            new_bid_price = self.model.round_to_tick(current_price - self.price_step * new_bid_index)
            # Ensure the new bid price is unique
            if new_bid_price not in self.order_book.bid_volume:
                bid_size = random.uniform(1, self.max_volume)
                self.order_book.add_bid(new_bid_price, bid_size)
                current_bids = sorted(self.order_book.bid_volume.keys(), reverse=True)
            # Increment the index for the next bid price
            new_bid_index += 1

        # Maintain asks
        current_asks = sorted(self.order_book.ask_volume.keys())
        new_ask_index = len(current_asks) + 1
        while len(current_asks) < self.depth_levels:
            new_ask_price = self.model.round_to_tick(current_price + self.price_step * new_ask_index)
            # Ensure the new ask price is unique
            if new_ask_price not in self.order_book.ask_volume:
                ask_size = random.uniform(1, self.max_volume)
                self.order_book.add_ask(new_ask_price, ask_size)
                current_asks = sorted(self.order_book.ask_volume.keys())
            # Increment the index for the next ask price
            new_ask_index += 1


    def run_simulation(self):
        """
        Run the selected model simulation and update the order book at each step.
        Return a DataFrame with time, price, variance (if applicable), and multiple levels of bids/asks.
        """
        # Generate price (and variance if Heston) data from the selected model
        price_data = self.model.generate()

        # Initialize the order book
        self.initialize_order_book()

        snapshots = []

        for idx, row in price_data.iterrows():
            current_price = row['Price']
            current_time = row['Time']
            current_variance = row.get('Variance', None)  # Only Heston has Variance

            # Update the order book for the new price
            self.update_order_book(current_price)

            # Get multiple levels from the order book
            depth = self.order_book.get_market_depth(levels=self.depth_levels)
            bid_levels = depth['bids']
            ask_levels = depth['asks']

            # Prepare snapshot dictionary
            snapshot = {
                'Time': current_time,
                'Price': current_price,
                'Variance': current_variance
            }

            # Record bid levels
            for i, (bp, bs) in enumerate(bid_levels, start=1):
                snapshot[f'BidPrice_{i}'] = bp
                snapshot[f'BidSize_{i}'] = bs

            # If fewer than depth_levels exist, fill remaining levels with None
            for i in range(len(bid_levels) + 1, self.depth_levels + 1):
                snapshot[f'BidPrice_{i}'] = None
                snapshot[f'BidSize_{i}'] = None

            # Record ask levels
            for i, (ap, asz) in enumerate(ask_levels, start=1):
                snapshot[f'AskPrice_{i}'] = ap
                snapshot[f'AskSize_{i}'] = asz

            # If fewer than depth_levels exist, fill remaining ask levels with None
            for i in range(len(ask_levels) + 1, self.depth_levels + 1):
                snapshot[f'AskPrice_{i}'] = None
                snapshot[f'AskSize_{i}'] = None

            # Calculate bid-ask spread if top levels exist
            if bid_levels and ask_levels:
                snapshot['BidAskSpread'] = ask_levels[0][0] - bid_levels[0][0]
            else:
                snapshot['BidAskSpread'] = None

            snapshots.append(snapshot)

        return pd.DataFrame(snapshots)
