import requests
from time import sleep
import numpy as np

s = requests.Session()
s.headers.update({'X-API-key': 'G4C31V41'}) # Make sure you use YOUR API Key

# global variables
MAX_LONG_EXPOSURE_NET = 25000
MAX_SHORT_EXPOSURE_NET = -25000
MAX_EXPOSURE_GROSS = 500000
ORDER_LIMIT = 5000

u_case = 'http://localhost:9999/v1/case'
u_book = 'http://localhost:9999/v1/securities/book'
u_securities = 'http://localhost:9999/v1/securities'
u_tas = 'http://localhost:9999/v1/securities/tas'
u_orders = 'http://localhost:9999/v1/orders'
u_news = 'http://localhost:9999/v1/news'
u_cancel = 'http://localhost:9999/v1/commands/cancel'
u_lease = 'http://localhost:9999/v1/leases'

##################### CONSTANTS & INITIAL #####################

def get_tick():   
    resp = s.get(u_case)
    if resp.ok:
        case = resp.json()
        return case['tick'], case['status']


def get_bid_ask(ticker):
    payload = {'ticker': ticker}
    resp = s.get (u_book, params = payload)
    if resp.ok:
        book = resp.json()
        bid_side_book = book['bids']
        ask_side_book = book['asks']
        
        bid_prices_book = [item["price"] for item in bid_side_book]
        ask_prices_book = [item['price'] for item in ask_side_book]
        
        best_bid_price = bid_prices_book[0]
        best_ask_price = ask_prices_book[0]
  
        return best_bid_price, best_ask_price

def get_time_sales(ticker):
    payload = {'ticker': ticker}
    resp = s.get (u_tas, params = payload)
    if resp.ok:
        book = resp.json()
        time_sales_book = [item["quantity"] for item in book]
        return time_sales_book

def get_position():
    resp = s.get (u_securities)
    if resp.ok:
        book = resp.json()
        gross_position = abs(book[1]['position']) + abs(book[2]['position']) + 2 * abs(book[3]['position'])
        net_position = book[1]['position'] + book[2]['position'] + 2 * book[3]['position']
        return gross_position, net_position

def get_open_orders(ticker):
    payload = {'ticker': ticker}
    resp = s.get (u_orders, params = payload)
    if resp.ok:
        orders = resp.json()
        buy_orders = [item for item in orders if item["action"] == "BUY"]
        sell_orders = [item for item in orders if item["action"] == "SELL"]
        return buy_orders, sell_orders

def get_order_status(order_id):
    resp = s.get (u_orders + '/' + str(order_id))
    if resp.ok:
        order = resp.json()
        return order['status']
    
##################### Default Functions #####################
    
def get_book(ticker):
    payload = {'ticker': ticker}
    resp = s.get (u_book, params = payload)
    if resp.ok:
        book = resp.json()
        return book

def get_ticker_position(ticker):
    resp = s.get(u_securities)
    if resp.ok:
        securities = resp.json()
        for item in securities:
            if item['ticker'] == ticker:
                return item['position']
    
def get_index_position():
    return s.get(u_securities).json()[3]['position']
    
def order_iceberg_reveal(ticker,side):
    book = get_book(ticker)
    bid_side_book = book['bids']
    ask_side_book = book['asks']
    
    bid_q_book = [item['quantity'] - item['quantity_filled'] for item in bid_side_book]
    ask_q_book = [item['quantity'] - item['quantity_filled'] for item in ask_side_book]
    
    if side == 'BID':
        ib = 0
        for item in bid_q_book:
            if get_ticker_position(ticker) - item > 0:
                ib += 1
            else:
                return ib
    
    elif side == 'ASK':
        ab = 0
        for item in ask_q_book:
            if get_ticker_position(ticker) - item > 0:
                ab += 1
            else:
                return ab

def price_iceberg_reveal(ticker,order): #未完成です、まだまだ進行中
    book = get_book(ticker)
    bid_side_book = book['bids']
    ask_side_book = book['asks']
    
    bid_prices_book = [item["price"] for item in bid_side_book]
    ask_prices_book = [item['price'] for item in ask_side_book]
    
    if order == 'BID':
        for i in range(len(bid_prices_book)):
            if i > 0 and bid_prices_book[i] != bid_prices_book[0]:
                return i, bid_prices_book[i]
        
    
def position_clearance():
    securities = s.get(u_securities).json()
    

##################### Original Functions #####################

def main():
    #Initiation
    tick, status = get_tick()
    ticker_list = ['RGLD','RFIN','INDX']
    market_prices = np.array([0.,0.,0.,0.,0.,0.]) 
    market_prices = market_prices.reshape(3,2)
    resp = s.post(u_lease, params = {'ticker': 'ETF-Creation'})
    resp = s.post(u_lease, params = {'ticker': 'ETF-Redemption'})
    lease_id_create = s.get(u_lease).json()[0]['id']
    lease_id_redempt = s.get(u_lease).json()[1]['id']
    

    while status == 'ACTIVE':
        for i in range(3):
            
            ticker_symbol = ticker_list[i]
            market_prices[i,0], market_prices[i,1] = get_bid_ask(ticker_symbol)
        
        gross_position, net_position = get_position()
        
        if gross_position < MAX_EXPOSURE_GROSS and net_position > MAX_SHORT_EXPOSURE_NET and net_position < MAX_LONG_EXPOSURE_NET:
            
            if market_prices[0, 0] + market_prices[1, 0] > market_prices[2, 1]: 
                resp = s.post(u_orders, params = {'ticker': 'RGLD', 'type': 'MARKET', 'quantity': ORDER_LIMIT, 'price': market_prices[0, 1], 'action': 'SELL'})
                resp = s.post(u_orders, params = {'ticker': 'RFIN', 'type': 'MARKET', 'quantity': ORDER_LIMIT, 'price': market_prices[1, 1], 'action': 'SELL'})
                resp = s.post(u_orders, params = {'ticker': 'INDX', 'type': 'MARKET', 'quantity': ORDER_LIMIT, 'price': market_prices[2, 0], 'action': 'BUY'})
                resp = s.post('http://localhost:9999/v1/leases/' + str(lease_id_redempt), params = {'from1':'INDX', 'quantity1': ORDER_LIMIT, 'from2': 'CAD', 'quantity2': ORDER_LIMIT * 0.0375})
            
            if market_prices[0, 1] + market_prices[1, 1] < market_prices[2, 0]: 
                resp = s.post(u_orders, params = {'ticker': 'RGLD', 'type': 'MARKET', 'quantity': ORDER_LIMIT, 'price': market_prices[0, 0], 'action': 'BUY'})
                resp = s.post(u_orders, params = {'ticker': 'RFIN', 'type': 'MARKET', 'quantity': ORDER_LIMIT, 'price': market_prices[1, 0], 'action': 'BUY'})
                resp = s.post(u_orders, params = {'ticker': 'INDX', 'type': 'MARKET', 'quantity': ORDER_LIMIT, 'price': market_prices[2, 1], 'action': 'SELL'})
                resp = s.post('http://localhost:9999/v1/leases/' + str(lease_id_create), params = {'from1':'RGLD', 'quantity1': ORDER_LIMIT, 'from2': 'RFIN', 'quantity2': ORDER_LIMIT})
            sleep(0.8) 
        
        else:
            if get_index_position() > 0:
                resp = s.post('http://localhost:9999/v1/leases/' + str(lease_id_redempt), params = {'from1':'INDX', 'quantity1': 100000, 'from2': 'CAD', 'quantity2': 100000 * 0.0375})
                sleep(0.8) 
                resp = s.post('http://localhost:9999/v1/leases/' + str(lease_id_redempt), params = {'from1':'INDX', 'quantity1': 100000, 'from2': 'CAD', 'quantity2': 100000 * 0.0375})
                sleep(0.8) 
            if get_index_position() < 0:
                resp = s.post('http://localhost:9999/v1/leases/' + str(lease_id_create), params = {'from1':'RGLD', 'quantity1': 100000, 'from2': 'RFIN', 'quantity2': 100000})
                sleep(0.8) 
                resp = s.post('http://localhost:9999/v1/leases/' + str(lease_id_create), params = {'from1':'RGLD', 'quantity1': 100000, 'from2': 'RFIN', 'quantity2': 100000})
                sleep(0.8) 
            
        tick, status = get_tick()

if __name__ == '__main__':
    main()



