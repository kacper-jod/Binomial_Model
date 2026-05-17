import numpy as np
from EuropeanOptions import *
from MarketModel import MarketModel

S0 = 50
K = 48
T = 2
sigma = 0.3
r = 0.02
dt = 1 / 12


BinomialMarketModel = MarketModel(SpotPrice = 50, 
                                  up = np.exp(sigma * np.sqrt(dt)),
                                  down = np.exp((-1) * sigma * np.sqrt(dt)), 
                                  risk_free_rate = 0.02,
                                  delta_T = 1 / 12, 
                                  max_maturity = 2 )

E_Call = EuropeanCallOption(Strike = 48, Maturity = 2)
E_Put = EuropeanPutOption(Strike = 48, Maturity = 2)

E_Call_Value = BinomialMarketModel.priceOption(E_Call)
E_Put_Value = BinomialMarketModel.priceOption(E_Put)

print("European Call:", E_Call_Value)
print("European Put :", E_Put_Value)

# sprawdzenie wyników parytetem put - call

print("\nCall-put parity:")
print("C - P =", E_Call_Value - E_Put_Value)
print("S0 - K*exp(-rT) =", S0 - K * np.exp(-r * T))
print("Difference =", abs((E_Call_Value - E_Put_Value) - (S0 - K * np.exp(-r * T))))