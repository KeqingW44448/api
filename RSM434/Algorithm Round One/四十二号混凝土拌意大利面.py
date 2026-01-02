import requests
from time import sleep
import numpy as np

# Initialize session and headers
s = requests.Session()
s.headers.update({'X-API-key': 'SLN7VDMW'})  # Make sure you use YOUR API Key

# Global variables
MAX_LONG_EXPOSURE_NET = 25000
MAX_SHORT_EXPOSURE_NET = -25000
MAX_EXPOSURE_GROSS = 450000
ORDER_LIMIT = 20000


# API endpoints

u_case = 'http://localhost:9999/v1/case'
u_book = 'http://localhost:9999/v1/securities/book'
u_securities = 'http://localhost:9999/v1/securities'
u_tas = 'http://localhost:9999/v1/securities/tas'
u_orders = 'http://localhost:9999/v1/orders'
u_news = 'http://localhost:9999/v1/news'
u_cancel = 'http://localhost:9999/v1/commands/cancel'
u_lease = 'http://localhost:9999/v1/leases'

##################### HELPER FUNCTIONS #####################

def get_tick():
    """Get the current tick and market status."""
    resp = s.get(u_case)
    if resp.ok:
        case = resp.json()
        return case['tick'], case['status']

def get_bid_ask(ticker):
    """Get the best bid and ask prices for a given ticker."""
    payload = {'ticker': ticker}
    resp = s.get(u_book, params=payload)
    if resp.ok:
        book = resp.json()
        bid_side_book = book['bids']
        ask_side_book = book['asks']
        
        bid_prices_book = [item["price"] for item in bid_side_book]
        ask_prices_book = [item['price'] for item in ask_side_book]
        
        best_bid_price = bid_prices_book[0]
        best_ask_price = ask_prices_book[0]
  
        return best_bid_price, best_ask_price

def get_position():
    """Get the gross and net positions."""
    resp = s.get(u_securities)
    if resp.ok:
        book = resp.json()
        gross_position = abs(book[1]['position']) + abs(book[2]['position']) + 2 * abs(book[3]['position'])
        net_position = book[1]['position'] + book[2]['position'] + 2 * book[3]['position']
        return gross_position, net_position

def get_open_orders(ticker):
    """Get open buy and sell orders for a given ticker."""
    payload = {'ticker': ticker}
    resp = s.get(u_orders, params=payload)
    if resp.ok:
        orders = resp.json()
        buy_orders = [item for item in orders if item["action"] == "BUY"]
        sell_orders = [item for item in orders if item["action"] == "SELL"]
        return buy_orders, sell_orders

def get_order_status(order_id):
    """Get the status of a specific order."""
    resp = s.get(u_orders + '/' + str(order_id))
    if resp.ok:
        order = resp.json()
        return order['status']

def get_ticker_position(ticker):
    """Get the position for a specific ticker."""
    resp = s.get(u_securities)
    if resp.ok:
        securities = resp.json()
        for item in securities:
            if item['ticker'] == ticker:
                return item['position']

def get_index_position():
    """Get the position of the index."""
    return s.get(u_securities).json()[3]['position']

def time_for_clearance(current_tick, next_tick):
    if current_tick >= next_tick:
        return True
    
    
        
    
    


##################### MAIN LOGIC #####################

def main():
    # Initialization
    tick, status = get_tick()
    ticker_list = ['RGLD', 'RFIN', 'INDX']
    market_prices = np.array([0., 0., 0., 0., 0., 0.]).reshape(3, 2)
    
    # Acquire leases for ETF creation and redemption
    resp = s.post(u_lease, params={'ticker': 'ETF-Creation'})
    resp = s.post(u_lease, params={'ticker': 'ETF-Redemption'})
    lease_id_create = s.get(u_lease).json()[0]['id']
    lease_id_redempt = s.get(u_lease).json()[1]['id']
    
    
    lease_tick_c = s.get(u_lease).json()[0]['start_lease_tick']
    lease_tick_r = s.get(u_lease).json()[1]['start_lease_tick']
    
    # Initialize variables
    Volume = 7500
    special_Volume = 50000    
    price_difference = 0.15
    basic_difference = 0.03
    up_catch = 0.0 #0.025
    down_catch = 0.0 #0.0625
    
    

    while status == 'ACTIVE':
        # Update market prices
        for i in range(3):
            ticker_symbol = ticker_list[i]
            market_prices[i, 0], market_prices[i, 1] = get_bid_ask(ticker_symbol)
        
        RGLD_ask = market_prices[0, 1]
        RGLD_bid = market_prices[0, 0]
        RFIN_ask = market_prices[1, 1]
        RFIN_bid = market_prices[1, 0]
        ETF_ask = market_prices[2, 1]
        ETF_bid = market_prices[2, 0]
        
        
        # Check gross and net positions
        gross_position, net_position = get_position()
        
        if gross_position < MAX_EXPOSURE_GROSS and MAX_SHORT_EXPOSURE_NET < net_position < MAX_LONG_EXPOSURE_NET:
            # Check for arbitrage opportunities
            if (RFIN_ask + RGLD_ask + price_difference) < ETF_bid or (RFIN_bid + RGLD_bid) > (ETF_ask + price_difference):
                
                if (RFIN_ask + RGLD_ask) < ETF_bid:
                    print("ETF OVERPRICED BIG TIME at spread of " + str(ETF_bid - (RFIN_ask + RGLD_ask)))
                    resp = s.post(u_orders, params={'ticker': 'RGLD', 'type': 'MARKET', 'quantity': special_Volume, 'action': 'BUY'})
                    resp = s.post(u_orders, params={'ticker': 'INDX', 'type': 'MARKET', 'quantity': special_Volume, 'action': 'SELL'})
                    resp = s.post(u_orders, params={'ticker': 'RFIN', 'type': 'MARKET', 'quantity': special_Volume, 'action': 'BUY'})
                
                elif (RFIN_bid + RGLD_bid) + 0.0375 > (ETF_ask):
                    print("ETF UNDERPRICED BIG TIME at spread of " + str(ETF_bid - (RFIN_ask + RGLD_ask)))
                    resp = s.post(u_orders, params={'ticker': 'RGLD', 'type': 'MARKET', 'quantity': special_Volume, 'action': 'SELL'})
                    resp = s.post(u_orders, params={'ticker': 'INDX', 'type': 'MARKET', 'quantity': special_Volume, 'action': 'BUY'})
                    resp = s.post(u_orders, params={'ticker': 'RFIN', 'type': 'MARKET', 'quantity': special_Volume, 'action': 'SELL'})

            else:
                
                if (RFIN_ask + RGLD_ask + basic_difference) < ETF_bid:
                    print("ETF OVERPRICED at spread of " + str(ETF_bid - (RFIN_ask + RGLD_ask)))
                    resp = s.post(u_orders, params={'ticker': 'RGLD', 'type': 'MARKET', 'quantity': Volume, 'action': 'BUY'})
                    resp = s.post(u_orders, params={'ticker': 'INDX', 'type': 'MARKET', 'quantity': Volume, 'action': 'SELL'})
                    resp = s.post(u_orders, params={'ticker': 'RFIN', 'type': 'MARKET', 'quantity': Volume, 'action': 'BUY'})
                
                elif (RFIN_bid + RGLD_bid) + 0.0375 > (ETF_ask + basic_difference):
                    print("ETF UNDERPRICED at spread of " + str(ETF_bid - (RFIN_ask + RGLD_ask)))
                    resp = s.post(u_orders, params={'ticker': 'RGLD', 'type': 'MARKET', 'quantity': Volume, 'action': 'SELL'})
                    resp = s.post(u_orders, params={'ticker': 'INDX', 'type': 'MARKET', 'quantity': Volume, 'action': 'BUY'})
                    resp = s.post(u_orders, params={'ticker': 'RFIN', 'type': 'MARKET', 'quantity': Volume, 'action': 'SELL'})
                    
        # else:
        #     if get_index_position() > 0:
        #         s.post(f'{u_lease}/{lease_id_redempt}', params={'from1': 'INDX', 'quantity1': 100000, 'from2': 'CAD', 'quantity2': 100000 * 0.0375})
        #         sleep(0.8)
        #         s.post(f'{u_lease}/{lease_id_redempt}', params={'from1': 'INDX', 'quantity1': 100000, 'from2': 'CAD', 'quantity2': 100000 * 0.0375})
        #         sleep(0.8)
        #     elif get_index_position() < 0:
        #         s.post(f'{u_lease}/{lease_id_create}', params={'from1': 'RGLD', 'quantity1': 100000, 'from2': 'RFIN', 'quantity2': 100000})
        #         sleep(0.8)
        #         s.post(f'{u_lease}/{lease_id_create}', params={'from1': 'RGLD', 'quantity1': 100000, 'from2': 'RFIN', 'quantity2': 100000})
        #         sleep(0.8)
    
        if time_for_clearance(tick, lease_tick_r):
            #print("triggered lv1")
            if get_index_position() > 0:
                #print("triggered lv2" + str(get_index_position()))
                s.post(f'{u_lease}/{lease_id_redempt}', params={'from1': 'INDX', 'quantity1': get_index_position(), 'from2': 'CAD', 'quantity2': get_index_position() * 0.0375})
                lease_tick_r = s.get(u_lease).json()[1]['next_lease_tick']
            #else:
                #print("time for redempt, but position not positive")
            
        if time_for_clearance(tick, lease_tick_c):
            if get_index_position() < 0:
                #print("triggered lv2 elif" + str(get_index_position()))
                s.post(f'{u_lease}/{lease_id_create}', params={'from1': 'RGLD', 'quantity1': abs(get_index_position()), 'from2': 'RFIN', 'quantity2': abs(get_index_position())})
                
                lease_tick_c = s.get(u_lease).json()[0]['next_lease_tick']
            #else:
                #print("time for create, but position not negative")
        
        sleep(0.3)
        
        # Update tick and status
        tick, status = get_tick()
if __name__ == '__main__':
    main()

