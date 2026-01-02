import requests
from time import sleep

s = requests.Session()
s.headers.update({'X-API-key': 'VHXVRO0J'}) # Dektop

MAX_LONG_EXPOSURE = 25000
MAX_SHORT_EXPOSURE = 25000
ORDER_LIMIT = 4000

def get_tick():
    resp = s.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick'], case['status']

def get_bid_ask(ticker):
    payload = {'ticker': ticker}
    resp = s.get ('http://localhost:9999/v1/securities/book', params = payload)
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
    payload = {'ticker': ticker, 'limit': 1}
    resp = s.get ('http://localhost:9999/v1/securities/tas', params = payload)
    if resp.ok:
        book = resp.json()
        time_sales_book = [item["quantity"] for item in book]
        return time_sales_book

def get_gross_position():
    resp = s.get ('http://localhost:9999/v1/securities')
    if resp.ok:
        book = resp.json()
        return abs(book[0]['position']) + abs(book[1]['position']) + abs(book[2]['position'])
#        return book[0]['position'] + book[1]['position'] + book[2]['position']

def get_net_position():
    resp = s.get ('http://localhost:9999/v1/securities')
    if resp.ok:
        book = resp.json()
        return book[0]['position'] + book[1]['position'] + book[2]['position']

def get_ticker_position(ticker):
    resp = s.get('http://localhost:9999/v1/securities')
    if resp.ok:
        book = resp.json()
        position = [item for item in book if item['ticker'] == ticker]
        return position

def get_open_orders(ticker):
    payload = {'ticker': ticker}
    resp = s.get ('http://localhost:9999/v1/orders', params = payload)
    if resp.ok:
        orders = resp.json()
        buy_orders = [item for item in orders if item["action"] == "BUY"]
        sell_orders = [item for item in orders if item["action"] == "SELL"]
        return buy_orders, sell_orders

def get_order_status(order_id):
    resp = s.get ('http://localhost:9999/v1/orders' + '/' + str(order_id))
    if resp.ok:
        order = resp.json()
        return order['status']
    
def check_momentum(ticker):
    payload = {'ticker': ticker}
    resp = s.get('http://localhost:9999/v1/securities/book', params = payload)
    if resp.ok:
        trend = None
        book = resp.json()
        bid_side_book = book['bids']
        ask_side_book = book['asks']
        if len(bid_side_book) > len(ask_side_book) + 10:
            trend = 'Up'
        elif len (bid_side_book) + 10 < len(ask_side_book):
            trend = 'Down'
    return trend
            

def main():
    tick, status = get_tick()
    ticker_list = ['CNR', 'AC']

    while status == 'ACTIVE':        

        for i in range(2):
            
            ticker_symbol = ticker_list[i]
            net_position = get_net_position() # modify to include net positions
            gross_position = get_gross_position()
            position = get_ticker_position(ticker_symbol)[0]['position']
            best_bid_price, best_ask_price = get_bid_ask(ticker_symbol)
            
            if position > 0: # Checking for long position and selling to neutralize position
                 resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': position, 'price': best_ask_price, 'action': 'SELL'})
            
            
            if position < 0: # Checking for short position and buying to neutralize position
                resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': abs(position), 'price': best_bid_price, 'action': 'BUY'})
            sleep(0.25)
            
      
            best_bid_price, best_ask_price = get_bid_ask(ticker_symbol)
            
            if gross_position < (MAX_LONG_EXPOSURE - ORDER_LIMIT) and net_position < 20000: # testing against net limits, but gross limit hit first, check against gross limit
                # Check NET positions; is less than 21000
                resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': ORDER_LIMIT, 'price': best_bid_price - 0.01, 'action': 'BUY'})
                
            if gross_position < (MAX_SHORT_EXPOSURE - ORDER_LIMIT) and net_position > -20000: # comparing gross position to gross limit; change greater than sign to less than sign
                resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': ORDER_LIMIT, 'price': best_ask_price + 0.01, 'action': 'SELL'})
              
                
                


            sleep(0.25) 

            s.post('http://localhost:9999/v1/commands/cancel', params = {'ticker': ticker_symbol})

        tick, status = get_tick()

if __name__ == '__main__':
    main()


# if check_momentum(ticker_symbol) == 'Up':
#     best_bid_price, best_ask_price = get_bid_ask(ticker_symbol)
#     
#     if gross_position < (MAX_LONG_EXPOSURE - 5000) and net_position < 20000: # testing against net limits, but gross limit hit first, check against gross limit
#         # Check NET positions; is less than 21000
##         resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': 5000, 'price': best_bid_price, 'action': 'BUY'})
#         
#     if gross_position < (MAX_SHORT_EXPOSURE - 5000) and net_position > -20000: # comparing gross position to gross limit; change greater than sign to less than sign
#         resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': 4000, 'price': best_ask_price + 0.05, 'action': 'SELL'})
# 
# elif check_momentum(ticker_symbol) == 'Down':
#     best_bid_price, best_ask_price = get_bid_ask(ticker_symbol)
#     
#     if gross_position < (MAX_LONG_EXPOSURE - 5000) and net_position < 20000: # testing against net limits, but gross limit hit first, check against gross limit
#         # Check NET positions; is less than 21000
#         resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': 4000, 'price': best_bid_price - 0.03, 'action': 'BUY'})
 #        
 #    if gross_position < (MAX_SHORT_EXPOSURE - 5000) and net_position > -20000: # comparing gross position to gross limit; change greater than sign to less than sign
 #        resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': 5000, 'price': best_ask_price + 0.05, 'action': 'SELL'})
# 
# else:      
