import EuropeanOptions

class MarketModel:
    def __init__(self, SpotPrice, up, down, risk_free_rate, delta_T, max_maturity):
        self.SpotPrice = SpotPrice
        self.up = up
        self.down = down
        self.risk_free_rate = risk_free_rate
        self.delta_T = delta_T
        self.max_maturity = max_maturity
    def priceOption(self, option):
        pass # tutaj będzie wywołanie funkcji z EuropeanOptions, która wyliczy cenę opcji na podstawie parametrów modelu rynkowego i opcji 
    def generatePriceTree(self):
        pass # tutaj będzie wygenerowanie drzewa cenowego na podstawie parametrów modelu rynkowego