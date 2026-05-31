from DrawTree import array_to_layers
import numpy as np
from Portfolio import Portfolio
from Cash import Cash

class Hedge:
    def __init__(self, market, option):
        self.market = market
        self.option = option
        self.tree = [0]

    def generate_hedging_portfolios(self):
        option_values = self.option.generateOptionValueTree(self.market)[0]
        option_prices = self.market.tree

        cash = Cash(self.market)

        for layer in range(1, self.market.number_of_layers):
            for el_numb in range(1, layer + 1):
                el_numb = el_numb + sum(range(layer))
                el_up = el_numb + layer
                el_down = el_numb + layer + 1
                growth_factor = np.exp(self.market.risk_free_rate * self.market.delta_T)

                system_matrix = np.array([[option_prices[el_up],
                                           growth_factor],
                                          [option_prices[el_down],
                                           growth_factor]])

                system_vector = np.array([option_values[el_up], option_values[el_down]])

                delta, alpha = np.linalg.solve(system_matrix, system_vector)

                self.tree.append(Portfolio(cash_asset=cash, delta=delta, alpha=alpha))

        return self.tree
