import numpy as np

def european_option_binomial(S0, K, T, r, sigma, dt, option_type = "call"):
    N = int(T/dt) # liczba okresów

    u = np.exp(sigma * np.sqrt(dt))
    d = np.exp(-sigma * np.sqrt(dt))

    p = (np.exp(r * dt) - d) / (u - d)

    S_T = np.zeros(N + 1) # końcowe wierzchołki drzewa, czyli wszystkie możliwe S_T

    for i in range(N + 1):
        S_T[i] = S0 * (u ** (N - i)) * (d ** i)

    if option_type == "call":
        V = np.maximum(S_T - K, 0)
    else:
        V = np.maximum(K - S_T, 0)

    for step in range(N - 1, -1, -1): # cofamy się w lewo po drzewie aż do początkowego wierzchołka
        V_prev = np.zeros(step + 1) # wartości w poprzednim okresie

        for i in range(step + 1):
            V_prev[i] = np.exp(-r * dt) * (p * V[i] + (1 - p) * V[i + 1]) # wzór z wykładu

        V = V_prev # przepinka na wcześniejszy okres

    return V[0]
