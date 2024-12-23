import random

def increase_trend(orderbook, change_percentage=0.05):
    bids = orderbook['bids']
    asks = orderbook['asks']
    
    # Remove lower bids and add higher bids
    num_to_remove = int(len(bids) * change_percentage)
    bids = bids[num_to_remove:]
    new_high_bids = [(price * (1 + random.uniform(0, change_percentage)), size) 
                     for price, size in bids[-num_to_remove:]]
    bids.extend(new_high_bids)
    
    # Remove lower asks and add higher asks
    num_to_remove = int(len(asks) * change_percentage)
    asks = asks[num_to_remove:]
    new_high_asks = [(price * (1 + random.uniform(0, change_percentage)), size) 
                     for price, size in asks[-num_to_remove:]]
    asks.extend(new_high_asks)
    
    # Sort the updated orderbook
    return {
        'bids': sorted(bids, key=lambda x: x[0], reverse=True),
        'asks': sorted(asks, key=lambda x: x[0])
    }

def decrease_trend(orderbook, change_percentage=0.05):
    bids = orderbook['bids']
    asks = orderbook['asks']
    
    # Remove higher bids and add lower bids
    num_to_remove = int(len(bids) * change_percentage)
    bids = bids[:-num_to_remove]
    new_low_bids = [(price * (1 - random.uniform(0, change_percentage)), size) 
                    for price, size in bids[:num_to_remove]]
    bids.extend(new_low_bids)
    
    # Remove higher asks and add lower asks
    num_to_remove = int(len(asks) * change_percentage)
    asks = asks[:-num_to_remove]
    new_low_asks = [(price * (1 - random.uniform(0, change_percentage)), size) 
                    for price, size in asks[:num_to_remove]]
    asks.extend(new_low_asks)
    
    # Sort the updated orderbook
    return {
        'bids': sorted(bids, key=lambda x: x[0], reverse=True),
        'asks': sorted(asks, key=lambda x: x[0])
    }