import unittest
from OrderBook.OrderBook import OrderBook  # Assuming the OrderBook class is in a file named orderbook.py

class TestOrderBook(unittest.TestCase):

    def setUp(self):
        self.ob = OrderBook()

    def test_add_bid(self):
        self.ob.add_bid(100, 10)
        self.assertEqual(self.ob.bids, [(100, 10)])
        self.assertEqual(self.ob.bid_volume[100], 10)

    def test_add_ask(self):
        self.ob.add_ask(101, 15)
        self.assertEqual(self.ob.asks, [(101, 15)])
        self.assertEqual(self.ob.ask_volume[101], 15)

    def test_remove_bid(self):
        self.ob.add_bid(100, 10)
        self.ob.remove_bid(100, 10)
        self.assertEqual(self.ob.bids, [])
        self.assertEqual(self.ob.bid_volume[100], 0)

    def test_remove_ask(self):
        self.ob.add_ask(101, 15)
        self.ob.remove_ask(101, 15)
        self.assertEqual(self.ob.asks, [])
        self.assertEqual(self.ob.ask_volume[101], 0)

    def test_sort_orders(self):
        self.ob.add_bid(100, 10)
        self.ob.add_bid(102, 5)
        self.ob.add_bid(101, 7)
        self.assertEqual(self.ob.bids, [(102, 5), (101, 7), (100, 10)])

        self.ob.add_ask(103, 8)
        self.ob.add_ask(105, 12)
        self.ob.add_ask(104, 6)
        self.assertEqual(self.ob.asks, [(103, 8), (104, 6), (105, 12)])

    def test_get_bid_ask_spread(self):
        self.ob.add_bid(100, 10)
        self.ob.add_ask(102, 15)
        self.assertEqual(self.ob.get_bid_ask_spread(), 2)

    def test_get_market_depth(self):
        self.ob.add_bid(100, 10)
        self.ob.add_bid(99, 15)
        self.ob.add_ask(101, 12)
        self.ob.add_ask(102, 8)
        depth = self.ob.get_market_depth(2)
        self.assertEqual(depth['bids'], [(100, 10), (99, 15)])
        self.assertEqual(depth['asks'], [(101, 12), (102, 8)])

    def test_increase_trend(self):
        self.ob.add_bid(100, 10)
        self.ob.add_bid(99, 15)
        self.ob.add_ask(101, 12)
        self.ob.add_ask(102, 8)
        initial_best_bid = self.ob.bids[0][0]
        initial_best_ask = self.ob.asks[0][0]
        self.ob.increase_trend()
        self.assertGreater(self.ob.bids[0][0], initial_best_bid)
        self.assertGreater(self.ob.asks[0][0], initial_best_ask)

    def test_decrease_trend(self):
        self.ob.add_bid(100, 10)
        self.ob.add_bid(99, 15)
        self.ob.add_ask(101, 12)
        self.ob.add_ask(102, 8)
        initial_best_bid = self.ob.bids[0][0]
        initial_best_ask = self.ob.asks[0][0]
        self.ob.decrease_trend()
        self.assertLess(self.ob.bids[0][0], initial_best_bid)
        self.assertLess(self.ob.asks[0][0], initial_best_ask)

if __name__ == '__main__':
    unittest.main()
