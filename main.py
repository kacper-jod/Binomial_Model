import numpy as np
from EuropeanOptions import *
from MarketModel import MarketModel

BinomialMarketModel = MarketModel(SpotPrice=50, up=1.1, down=0.9, risk_free_rate=0.02, delta_T=1/12, max_maturity=2)

EuropeanCallOption = EuropeanCallOption(Strike=48, Maturity=2)

MarketModel.priceOption(EuropeanCallOption)




S0 = 50
K = 48
T = 2
sigma = 0.3
r = 0.02
dt = 1 / 12


call = european_option_binomial(S0, K, T, r, sigma, dt, "call")
put = european_option_binomial(S0, K, T, r, sigma, dt, "put")

print("European Call:", call)
print("European Put :", put)

# sprawdzenie wyników parytetem put - call

print("\nCall-put parity:")
print("C - P =", call - put)
print("S0 - K*exp(-rT) =", S0 - K * np.exp(-r * T))
print("Difference =", abs((call - put) - (S0 - K * np.exp(-r * T))))