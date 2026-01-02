import requests
from time import sleep
import numpy as np

s = requests.Session()
s.headers.update({'X-API-key': 'G4C31V41'})

u_case = 'http://localhost:9999/v1/case'
u_book = 'http://localhost:9999/v1/securities/book'
u_securities = 'http://localhost:9999/v1/securities'
u_tas = 'http://localhost:9999/v1/securities/tas'
u_orders = 'http://localhost:9999/v1/orders'
u_news = 'http://localhost:9999/v1/news'
u_cancel = 'http://localhost:9999/v1/commands/cancel'
u_lease = 'http://localhost:9999/v1/leases'


gross_limit = 100000
net_limit = 50000

error_margin = 1.10

##################### HELPER FUNCTIONS #####################

def get_tick():
    resp = s.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick'], case['status']
  
  
def get_news(eps_estimates,ownership_estimates, eps):
    resp = s.get ('http://localhost:9999/v1/news', params = {'limit': 50}) # default limit is 20
    if resp.ok:
        news_query = resp.json()
        
        for i in news_query[::-1]: # iterating backwards through the list, news items are ordered newest to oldest         

            if i['headline'].find("TP") > -1: #First line being TP
    
                if i['headline'].find("Analyst") > -1: 
                    
                    if i['headline'].find("#1") > -1: #
                        eps_estimates[0, 0] = float(i['body'][i['body'].find("Q1:") + 5 : i['body'].find("Q1:") + 9 ])
                        eps_estimates[0, 1] = float(i['body'][i['body'].find("Q2:") + 5 : i['body'].find("Q2:") + 9 ])
                        eps_estimates[0, 2] = float(i['body'][i['body'].find("Q3:") + 5 : i['body'].find("Q3:") + 9 ])
                        eps_estimates[0, 3] = float(i['body'][i['body'].find("Q4:") + 5 : i['body'].find("Q4:") + 9 ])
                        
                    if i['headline'].find("#2") > -1:
                        eps_estimates[0, 1] = float(i['body'][i['body'].find("Q2:") + 5 : i['body'].find("Q2:") + 9 ])
                        eps_estimates[0, 2] = float(i['body'][i['body'].find("Q3:") + 5 : i['body'].find("Q3:") + 9 ])
                        eps_estimates[0, 3] = float(i['body'][i['body'].find("Q4:") + 5 : i['body'].find("Q4:") + 9 ])

                    if i['headline'].find("#3") > -1:
                        eps_estimates[0, 2] = float(i['body'][i['body'].find("Q3:") + 5 : i['body'].find("Q3:") + 9 ])
                        eps_estimates[0, 3] = float(i['body'][i['body'].find("Q4:") + 5 : i['body'].find("Q4:") + 9 ])

                    if i['headline'].find("#4") > -1:
                        eps_estimates[0, 3] = float(i['body'][i['body'].find("Q4:") + 5 : i['body'].find("Q4:") + 9 ])
                    
                if i['headline'].find("institutional") > -1:
                    
                    if i['headline'].find("Q1") > -1:
                        ownership_estimates[0, 0] = float(i['body'][i['body'].find("%") - 5 : i['body'].find("%")])                    
                    
                    if i['headline'].find("Q2") > -1:
                        ownership_estimates[0, 1] = float(i['body'][i['body'].find("%") - 5 : i['body'].find("%")])                    

                    if i['headline'].find("Q3") > -1:
                        ownership_estimates[0, 2] = float(i['body'][i['body'].find("%") - 5 : i['body'].find("%")])                                                            

                    if i['headline'].find("Q4") > -1:
                        ownership_estimates[0, 3] = float(i['body'][i['body'].find("%") - 5 : i['body'].find("%")])                                    
                
            if i['headline'].find("AS") > -1: #Second line being AS
                
                if i['headline'].find("Analyst") > -1:
                    
                    if i['headline'].find("#1") > -1:
                        eps_estimates[1, 0] = float(i['body'][i['body'].find("Q1:") + 5 : i['body'].find("Q1:") + 9 ])
                        eps_estimates[1, 1] = float(i['body'][i['body'].find("Q2:") + 5 : i['body'].find("Q2:") + 9 ])
                        eps_estimates[1, 2] = float(i['body'][i['body'].find("Q3:") + 5 : i['body'].find("Q3:") + 9 ])
                        eps_estimates[1, 3] = float(i['body'][i['body'].find("Q4:") + 5 : i['body'].find("Q4:") + 9 ])
                        
                    if i['headline'].find("#2") > -1:
                        eps_estimates[1, 1] = float(i['body'][i['body'].find("Q2:") + 5 : i['body'].find("Q2:") + 9 ])
                        eps_estimates[1, 2] = float(i['body'][i['body'].find("Q3:") + 5 : i['body'].find("Q3:") + 9 ])
                        eps_estimates[1, 3] = float(i['body'][i['body'].find("Q4:") + 5 : i['body'].find("Q4:") + 9 ])

                    if i['headline'].find("#3") > -1:
                        eps_estimates[1, 2] = float(i['body'][i['body'].find("Q3:") + 5 : i['body'].find("Q3:") + 9 ])
                        eps_estimates[1, 3] = float(i['body'][i['body'].find("Q4:") + 5 : i['body'].find("Q4:") + 9 ])

                    if i['headline'].find("#4") > -1:
                        eps_estimates[1, 3] = float(i['body'][i['body'].find("Q4:") + 5 : i['body'].find("Q4:") + 9 ])
                    
                if i['headline'].find("institutional") > -1:
                    
                    if i['headline'].find("Q1") > -1:
                        ownership_estimates[1, 0] = float(i['body'][i['body'].find("%") - 5 : i['body'].find("%")])                    
                    
                    if i['headline'].find("Q2") > -1:
                        ownership_estimates[1, 1] = float(i['body'][i['body'].find("%") - 5 : i['body'].find("%")])                    

                    if i['headline'].find("Q3") > -1:
                        ownership_estimates[1, 2] = float(i['body'][i['body'].find("%") - 5 : i['body'].find("%")])                                                            

                    if i['headline'].find("Q4") > -1:
                        ownership_estimates[1, 3] = float(i['body'][i['body'].find("%") - 5 : i['body'].find("%")])                                                    
                
            if i['headline'].find("BA") > -1: #Third line being BA
                
                if i['headline'].find("Analyst") > -1:
                    
                    if i['headline'].find("#1") > -1:
                        eps_estimates[2, 0] = float(i['body'][i['body'].find("Q1:") + 5 : i['body'].find("Q1:") + 9 ])
                        eps_estimates[2, 1] = float(i['body'][i['body'].find("Q2:") + 5 : i['body'].find("Q2:") + 9 ])
                        eps_estimates[2, 2] = float(i['body'][i['body'].find("Q3:") + 5 : i['body'].find("Q3:") + 9 ])
                        eps_estimates[2, 3] = float(i['body'][i['body'].find("Q4:") + 5 : i['body'].find("Q4:") + 9 ])
                        
                    if i['headline'].find("#2") > -1:
                        eps_estimates[2, 1] = float(i['body'][i['body'].find("Q2:") + 5 : i['body'].find("Q2:") + 9 ])
                        eps_estimates[2, 2] = float(i['body'][i['body'].find("Q3:") + 5 : i['body'].find("Q3:") + 9 ])
                        eps_estimates[2, 3] = float(i['body'][i['body'].find("Q4:") + 5 : i['body'].find("Q4:") + 9 ])

                    if i['headline'].find("#3") > -1:
                        eps_estimates[2, 2] = float(i['body'][i['body'].find("Q3:") + 5 : i['body'].find("Q3:") + 9 ])
                        eps_estimates[2, 3] = float(i['body'][i['body'].find("Q4:") + 5 : i['body'].find("Q4:") + 9 ])

                    if i['headline'].find("#4") > -1:
                        eps_estimates[2, 3] = float(i['body'][i['body'].find("Q4:") + 5 : i['body'].find("Q4:") + 9 ])
                    
                if i['headline'].find("institutional") > -1:
                    
                    if i['headline'].find("Q1") > -1:
                        ownership_estimates[2, 0] = float(i['body'][i['body'].find("%") - 5 : i['body'].find("%")])                    
                    
                    if i['headline'].find("Q2") > -1:
                        ownership_estimates[2, 1] = float(i['body'][i['body'].find("%") - 5 : i['body'].find("%")])                    

                    if i['headline'].find("Q3") > -1:
                        ownership_estimates[2, 2] = float(i['body'][i['body'].find("%") - 5 : i['body'].find("%")])                                                            

                    if i['headline'].find("Q4") > -1:
                        ownership_estimates[2, 3] = float(i['body'][i['body'].find("%") - 5 : i['body'].find("%")])                                                    
                
            if i['headline'].find("Earnings release") > -1:
                                    
                if i['headline'].find("Q1") > -1:
                    eps[0, 0] = float(i['body'][i['body'].find("TP Q1:") + 32 : i['body'].find("TP Q1:") + 36 ])
                    eps[1, 0] = float(i['body'][i['body'].find("AS Q1:") + 32 : i['body'].find("AS Q1:") + 36 ])
                    eps[2, 0] = float(i['body'][i['body'].find("BA Q1:") + 32 : i['body'].find("BA Q1:") + 36 ])
                    
                if i['headline'].find("Q2") > -1:
                    eps[0, 1] = float(i['body'][i['body'].find("TP Q2:") + 32 : i['body'].find("TP Q2:") + 36 ])
                    eps[1, 1] = float(i['body'][i['body'].find("AS Q2:") + 32 : i['body'].find("AS Q2:") + 36 ])
                    eps[2, 1] = float(i['body'][i['body'].find("BA Q2:") + 32 : i['body'].find("BA Q2:") + 36 ])

                if i['headline'].find("Q3") > -1:
                    eps[0, 2] = float(i['body'][i['body'].find("TP Q3:") + 32 : i['body'].find("TP Q3:") + 36 ])
                    eps[1, 2] = float(i['body'][i['body'].find("AS Q3:") + 32 : i['body'].find("AS Q3:") + 36 ])
                    eps[2, 2] = float(i['body'][i['body'].find("BA Q3:") + 32 : i['body'].find("BA Q3:") + 36 ])

                if i['headline'].find("Q4") > -1:
                    eps[0, 3] = float(i['body'][i['body'].find("TP Q4:") + 32 : i['body'].find("TP Q4:") + 36 ])
                    eps[1, 3] = float(i['body'][i['body'].find("AS Q4:") + 32 : i['body'].find("AS Q4:") + 36 ])
                    eps[2, 3] = float(i['body'][i['body'].find("BA Q4:") + 32 : i['body'].find("BA Q4:") + 36 ])
                                
        return eps_estimates, ownership_estimates, eps   
def get_position():
    resp = s.get (u_securities)
    gross_position = 0
    net_position = 0
    if resp.ok:
        book = resp.json()
        for i in book:
            gross_position += abs(i['position'])
            net_position += i['position']
        return gross_position, net_position    

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
        
        best_bid_price, best_ask_price = None, None
        
        if len(bid_prices_book) > 0:
            best_bid_price = bid_prices_book[0]
        if len(ask_prices_book) > 0:
            best_ask_price = ask_prices_book[0]
  
        return best_bid_price, best_ask_price    

def get_last(ticker):
    payload = {'ticker': ticker}
    resp = s.get(u_securities, params=payload)
    if resp.ok:
        sec = resp.json()
        last = sec[0]['last']
        return last
    
def fire_sale(ticker):
    securities = s.get(u_securities, params = {'ticker':ticker}).json()
    position = securities[0]['position']
    if position > 0.0: #Dump long position if the underlaying ticker has positive position
        resp = s.post(u_orders, params = {'ticker': ticker, 'type': 'MARKET', 'quantity': abs(position), 'action': 'SELL'})
        #print(str(item['ticker']) + ' long Position Exploded, short dumping')
    elif position < 0.0: #Dump short position if the underlaying ticker has negative position
        resp = s.post(u_orders, params = {'ticker': ticker, 'type': 'MARKET', 'quantity': abs(position), 'action': 'BUY'})
        #print(str(item['ticker']) + ' short Position Exploded, long dumping')

def clearance():
    securities = s.get(u_securities).json()
    gross, net = get_position()
    resp = s.post(u_cancel, params = {'all': 1})
    if gross > 0:
        for item in securities:
            position = item['position']
            if position > 0.0: #Dump long position if the underlaying ticker has positive position
                resp = s.post(u_orders, params = {'ticker': item['ticker'], 'type': 'MARKET', 'quantity': abs(position), 'action': 'SELL'})
                print(str(item['ticker']) + ' long Position Exploded, short dumping')
            elif position < 0.0: #Dump short position if the underlaying ticker has negative position
                resp = s.post(u_orders, params = {'ticker': item['ticker'], 'type': 'MARKET', 'quantity': abs(position), 'action': 'BUY'})
                print(str(item['ticker']) + ' short Position Exploded, long dumping')
                
def is_overlimit():
    gross, net = get_position()
    if abs(gross) > gross_limit or abs(net) > net_limit:
        return True
    else:
        return False

def over_protection(glimit, nlimit):
    securities = s.get(u_securities).json()
    gross, net = get_position()
    gross_threshold = gross / glimit
    net_threshold = abs(net) / nlimit
    
    if net_threshold > 0.95 or gross_threshold > 0.95: #If the total position reaches 95% of the limit
        #resp = s.post(u_cancel, params = {'all': 1})
        for item in securities:
            position = item['position']
            if position > 0.0: #Dump long position if the underlaying ticker has positive position
                resp = s.post(u_orders, params = {'ticker': item['ticker'], 'type': 'MARKET', 'quantity': abs(position) * 0.3, 'action': 'SELL'})
                print(str(item['ticker']) + ' long Position Exploded, short dumping')
            elif position < 0.0: #Dump short position if the underlaying ticker has negative position
                resp = s.post(u_orders, params = {'ticker': item['ticker'], 'type': 'MARKET', 'quantity': abs(position) * 0.3, 'action': 'BUY'})
                print(str(item['ticker']) + ' short Position Exploded, long dumping')

def main():
    
    tick, status = get_tick()
    
    ticker_list = ['TP', 'AS', 'BA']
    
    ipr = np.array([False, False, False, False, False, False])
    ipr = ipr.reshape(2,3)
    
    execution = np.array([True, True, True, True, True, True, True, True, True, True, True, True])
    execution = execution.reshape(3,4)
    
    eps_estimates = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    eps_estimates = eps_estimates.reshape(3,4)
    
    ownership_estimates = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    ownership_estimates = ownership_estimates.reshape(3,4)
    
    eps = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    eps = eps.reshape(3,4)
    
    eps_val = np.array([0.40, 0.33, 0.33, 0.37, 0.35, 0.45, 0.50, 0.25, 0.15, 0.50, 0.60, 0.25])
    eps_val = eps_val.reshape(3,4)
    
    own_val = np.array([50.0, 50.0, 50.0])
    own_val = own_val.reshape(3,1)
    
    valuation = [0.0, 0.0, 0.0]
    
    while status == "ACTIVE":
            
        eps_estimates, ownership_estimates, eps = get_news(eps_estimates, ownership_estimates, eps)
        
        print("--- EPS Estimates ---")
        print(eps_estimates)
        print("--- Ownership Estimates ---")
        print(ownership_estimates)
        print("--- EPS ---")
        print(eps)
        
        for i in range(3):
            for j in range (4):
                if eps_estimates[i, j] != 0:
                    eps_val[i, j] = eps_estimates[i, j]
                if ownership_estimates[i, j] != 0:
                    own_val[i, 0] = ownership_estimates[i, j]
                if eps[i, j] != 0:
                    eps_val[i, j] = eps[i, j]
                    
        print("--- EPS for Valuation ---")
        print(eps_val)
        print("--- Ownership for Valuation ---")
        print(own_val)

        TP_eps = eps_val.sum(axis = 1)[0]
        TP_g = (TP_eps / 1.43) - 1
        TP_div = TP_eps * 0.80
        TP_DDM = ((TP_div * (1 + TP_g)) / (0.05 - TP_g)) * (1 - ((1 + TP_g) / (1 + 0.05))**5 ) + ((TP_div * ((1 + TP_g)**5) * (1 + 0.02)) / (0.05 - 0.02)) / (1 + 0.05)**5
        TP_pe = TP_eps * 12
        TP_val = (own_val[0, 0] / 100) * TP_DDM + (1 - (own_val[0,0] / 100)) * TP_pe
 
        AS_eps = eps_val.sum(axis = 1)[1]
        AS_g = (AS_eps / 1.55) - 1
        AS_div = AS_eps * 0.50
        AS_DDM = ((AS_div * (1 + AS_g)) / (0.075 - AS_g)) * (1 - ((1 + AS_g) / (1 + 0.075))**5 ) + ((AS_div * ((1 + AS_g)**5) * (1 + 0.02)) / (0.075 - 0.02)) / (1 + 0.075)**5
        AS_pe = AS_eps * 16
        AS_val = (own_val[1, 0] / 100) * AS_DDM + (1 - (own_val[1,0] / 100)) * AS_pe
        
        BA_eps = eps_val.sum(axis = 1)[2]
        BA_g = (BA_eps / 1.50) - 1
        BA_pe_inst = 20 * (1 + BA_g) * BA_eps
        BA_pe_retail = BA_eps * 20
        BA_val = (own_val[2, 0] / 100) * BA_pe_inst + (1 - (own_val[2,0] / 100)) * BA_pe_retail
        
        valuation = [TP_val, AS_val, BA_val]
        
        print("--- TP Valuation ---")
        print (TP_val)
        print("--- AS Valuation --")
        print(AS_val)
        print("--- BA Valuation ---")
        print(BA_val)
        
        if any(valuation) != 0:
            for i in range(3):
                last = get_last(ticker_list[i])
                bid, ask = get_bid_ask(ticker_list[i])
                if bid is not None and ask is not None:
                    if last <= valuation[i] * error_margin and last >= valuation[i] / error_margin:
                        fire_sale(ticker_list[i])
                        continue
                    if bid > valuation[i] * error_margin and not is_overlimit():
                        if ipr[1,i]:
                            fire_sale(ticker_list[i])
                            ipr[1,i] = False
                        ipr[0,i] = True
                        resp = s.post(u_orders, params={'ticker': ticker_list[i], 'type': 'MARKET', 'quantity': 200, 'action': 'SELL'})
                    elif ask < valuation[i] / error_margin and not is_overlimit():
                        if ipr[0,i]:
                            fire_sale(ticker_list[i])
                            ipr[0,i] = False
                        ipr[1,i] = True
                        resp = s.post(u_orders, params={'ticker': ticker_list[i], 'type': 'MARKET', 'quantity': 200, 'action': 'BUY'})
                else:
                    continue
                
        print("--- Execution Status ---")
        print(ipr)
        
        # if tick >= 60: 
        #     if execution[0,0] or execution[1,0] or execution[2,0]:
        #         for i in range(3):
        #             bid, ask = get_bid_ask(ticker_list[i])
        #             if bid == None or ask == None:
        #                 continue
        #             if bid < valuation[i] * error_margin and ask > valuation[i] / error_margin:
        #                 fire_sale(ticker_list[i])
        #                 execution[i, 0] = False
        #                 continue
        #             if bid > valuation[i] * error_margin:
        #                 resp = s.post(u_orders, params={'ticker': ticker_list[i], 'type': 'MARKET', 'quantity': 200, 'action': 'SELL'})
        #             elif ask < valuation[i] / error_margin:
        #                 resp = s.post(u_orders, params={'ticker': ticker_list[i], 'type': 'MARKET', 'quantity': 200, 'action': 'BUY'})
            
        # if tick >= 120:
        #     execution[0,0], execution[1,0], execution[2,0] = False, False, False
        #     if execution[0,1] or execution[1,1] or execution[2,1]:
        #         for i in range(3):
        #             bid, ask = get_bid_ask(ticker_list[i])
        #             if bid == None or ask == None:
        #                 continue
        #             if bid < valuation[i] * error_margin and ask > valuation[i] / error_margin:
        #                 fire_sale(ticker_list[i])
        #                 execution[i, 1] = False
        #                 continue
        #             if bid > valuation[i] * error_margin:
        #                 resp = s.post(u_orders, params={'ticker': ticker_list[i], 'type': 'MARKET', 'quantity': 200, 'action': 'SELL'})
        #             elif ask < valuation[i] / error_margin:
        #                 resp = s.post(u_orders, params={'ticker': ticker_list[i], 'type': 'MARKET', 'quantity': 200, 'action': 'BUY'})
        
        # if tick >= 180: 
        #     execution[0,1], execution[1,1], execution[2,1] = False, False, False
        #     if execution[0,2] or execution[1,2] or execution[2,2]:
        #         for i in range(3):
        #             bid, ask = get_bid_ask(ticker_list[i])
        #             if bid == None or ask == None:
        #                 continue
        #             if bid < valuation[i] * error_margin and ask > valuation[i] / error_margin:
        #                 fire_sale(ticker_list[i])
        #                 execution[i, 2] = False
        #                 continue
        #             if bid > valuation[i] * error_margin:
        #                 resp = s.post(u_orders, params={'ticker': ticker_list[i], 'type': 'MARKET', 'quantity': 200, 'action': 'SELL'})
        #             elif ask < valuation[i] / error_margin:
        #                 resp = s.post(u_orders, params={'ticker': ticker_list[i], 'type': 'MARKET', 'quantity': 200, 'action': 'BUY'})

        # if tick >= 240:
        #     execution[0,2], execution[1,2], execution[2,2] = False, False, False
        #     if execution[0,3] or execution[1,3] or execution[2,3]:
        #         for i in range(3):
        #             bid, ask = get_bid_ask(ticker_list[i])
        #             if bid == None or ask == None:
        #                 continue
        #             if bid < valuation[i] * error_margin and ask > valuation[i] / error_margin:
        #                 fire_sale(ticker_list[i])
        #                 execution[i, 3] = False
        #                 continue
        #             if bid > valuation[i] * error_margin:
        #                 resp = s.post(u_orders, params={'ticker': ticker_list[i], 'type': 'MARKET', 'quantity': 200, 'action': 'SELL'})
        #             elif ask < valuation[i] / error_margin:
        #                 resp = s.post(u_orders, params={'ticker': ticker_list[i], 'type': 'MARKET', 'quantity': 200, 'action': 'BUY'})
        
        #print("--- Execution progress ---")
        #print(execution)
        
        over_protection(100000, 50000)
        # ADD trading logic - price below valuation = buy; price above valuation = sell
        # MOdify the valuation -> the sample valuation is the average/midpoint - early on this can be wildly inaccurate
        # 1) Take the midpoint and add an error term (based on quarters left in the case) valuation +/- 20% or $5
        # 2) calculate a min and max valuation, factoring in institutional ownership could be part of min or max depending on DDM valuation
        
        
        
        
        sleep(1.5)
        tick, status = get_tick()
    
if __name__ == '__main__':
    main()

    



