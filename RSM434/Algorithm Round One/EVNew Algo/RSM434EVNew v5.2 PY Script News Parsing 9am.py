import requests
from time import sleep
import numpy as np

s = requests.Session()
s.headers.update({'X-API-key': 'pythontraining'})

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

            if i['headline'].find("TP") > -1:
    
                if i['headline'].find("Analyst") > -1:
                    
                    if i['headline'].find("#1") > -1:
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
                
            if i['headline'].find("AS") > -1:
                
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
                
            if i['headline'].find("BA") > -1:
                
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

def main():
    
    tick, status = get_tick()
    
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
        
        print("--- TP Valuation ---")
        print (TP_val)
        print("--- AS Valuation --")
        print(AS_val)
        print("--- BA Valuation ---")
        print(BA_val)
        
        # ADD trading logic - price below valuation = buy; price above valuation = sell
        # MOdify the valuation -> the sample valuation is the average/midpoint - early on this can be wildly inaccurate
        # 1) Take the midpoint and add an error term (based on quarters left in the case) valuation +/- 20% or $5
        # 2) calculate a min and max valuation, factoring in institutional ownership could be part of min or max depending on DDM valuation
        
        
        
        
        sleep(0.5)
        tick, status = get_tick()
    
if __name__ == '__main__':
    main()

    



