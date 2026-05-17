import numpy as np
from binomial import european_option_binomial


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