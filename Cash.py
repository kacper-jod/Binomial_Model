import numpy as np

class Cash:
    def __init__(self, market):
        self.market = market

    def grow(self, amount, dt):
        return amount * np.exp(self.market.r * dt)

    def discount(self, amount, dt):
        return amount * np.exp(-self.market.r * dt)