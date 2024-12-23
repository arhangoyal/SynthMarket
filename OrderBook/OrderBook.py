from collections import defaultdict

class OrderBook:
    def __init__(self):
        # Aggregated volumes by price for bids and asks
        self.bid_volume = defaultdict(float)
        self.ask_volume = defaultdict(float)

    def add_bid(self, price, size):
        self.bid_volume[price] += size

    def add_ask(self, price, size):
        self.ask_volume[price] += size

    def remove_bid(self, price, size):
        if price in self.bid_volume:
            self.bid_volume[price] -= size
            if self.bid_volume[price] <= 0:
                del self.bid_volume[price]

    def remove_ask(self, price, size):
        if price in self.ask_volume:
            self.ask_volume[price] -= size
            if self.ask_volume[price] <= 0:
                del self.ask_volume[price]

    def get_best_bid(self):
        """Return the best (highest) bid price and its volume."""
        if not self.bid_volume:
            return None, 0
        best_price = max(self.bid_volume.keys())
        return best_price, self.bid_volume[best_price]

    def get_best_ask(self):
        """Return the best (lowest) ask price and its volume."""
        if not self.ask_volume:
            return None, 0
        best_price = min(self.ask_volume.keys())
        return best_price, self.ask_volume[best_price]

    def get_bid_ask_spread(self):
        best_bid, _ = self.get_best_bid()
        best_ask, _ = self.get_best_ask()
        if best_bid is not None and best_ask is not None:
            return best_ask - best_bid
        return None

    def get_market_depth(self, levels=5):
        """
        Return the top N bids and asks. 
        Bids: Sorted descending by price.
        Asks: Sorted ascending by price.
        """
        # Top N bids
        sorted_bids = sorted(self.bid_volume.items(), key=lambda x: x[0], reverse=True)[:levels]
        # Top N asks
        sorted_asks = sorted(self.ask_volume.items(), key=lambda x: x[0])[:levels]
        return {
            'bids': sorted_bids,
            'asks': sorted_asks
        }

    def __str__(self):
        sorted_bids = sorted(self.bid_volume.items(), key=lambda x: x[0], reverse=True)
        sorted_asks = sorted(self.ask_volume.items(), key=lambda x: x[0])
        return f"Bids (price:volume): {sorted_bids}\nAsks (price:volume): {sorted_asks}"
