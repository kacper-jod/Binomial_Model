import numpy as np

class MarketModel:
    def __init__(self, SpotPrice, up, down, risk_free_rate, delta_T, max_maturity):
        self.SpotPrice = SpotPrice
        self.up = up
        self.down = down
        self.risk_free_rate = risk_free_rate
        self.delta_T = delta_T
        self.max_maturity = max_maturity
        self.p = (np.exp(self.risk_free_rate * self.delta_T) - self.down) / (self.up - self.down)
        self.steps = int(max_maturity / delta_T)

    def generate_terminal_prices(self):
        prices = []

        for i in range(self.steps + 1):
            price = self.SpotPrice * (self.up ** (self.steps - i)) * (self.down ** i)
            prices.append(price)

    def priceOption(self, option):
        terminal_prices = self.generate_terminal_prices()

        # dla kazdej koncowej ceny policz wartosc opcji
        values = np.array([option.value(price) for price in terminal_prices])

        for step in range(self.steps - 1, -1, -1):
            new_values = np.zeros(step + 1)

            for i in range(step + 1):
                new_values[i] = np.exp(-self.risk_free_rate * self.delta_T) * (
                    self.p * values[i] + (1 - self.p) * values[i + 1]
                )

            values = new_values

        return values[0]
        
