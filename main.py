import numpy as np
from EuropeanOptions import *
from MarketModel import MarketModel

S0 = 50
K = 48
T = 2
sigma = 0.3
r = 0.02
dt = 1 / 4 #changed from 1/12, its too much for now, we have too big tree

BinomialMarketModel = MarketModel(SpotPrice = S0, 
                                  up = np.exp(sigma * np.sqrt(dt)),
                                  down = np.exp((-1) * sigma * np.sqrt(dt)), 
                                  risk_free_rate = r,
                                  delta_T = dt, 
                                  max_maturity = T )

E_Call = EuropeanCallOption(Strike = K, Maturity = T)
E_Put = EuropeanPutOption(Strike = K, Maturity = T)

E_Call_Value = BinomialMarketModel.priceOption(E_Call)
E_Put_Value = BinomialMarketModel.priceOption(E_Put)

# print(BinomialMarketModel.starting_node)

print("European Call:", E_Call_Value)
print("European Put :", E_Put_Value)

# sprawdzenie wyników parytetem put - call

print("\nCall-put parity:")
print("C - P =", E_Call_Value - E_Put_Value)
print("S0 - K*exp(-rT) =", S0 - K * np.exp(-r * T))
print("Difference =", abs((E_Call_Value - E_Put_Value) - (S0 - K * np.exp(-r * T))))