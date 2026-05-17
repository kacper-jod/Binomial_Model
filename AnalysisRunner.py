import numpy as np
import matplotlib.pyplot as plt
from MarketModel import MarketModel
from EuropeanOptions import EuropeanCallOption, EuropeanPutOption

class AnalysisRunner:
    def __init__(self, baseline):
        self.baseline = baseline

    def create_model(self, params):
        u = np.exp(params['sigma'] * np.sqrt(params['dt']))
        d = np.exp(-params['sigma'] * np.sqrt(params['dt']))

        return MarketModel(
            SpotPrice=params['S0'],
            up=u,
            down=d,
            risk_free_rate=params['r'],
            delta_T=params['dt'],
            max_maturity=params['T']
        )

    def get_all_prices(self, params):
        model = self.create_model(params)

        options = { #only european options for now
            'Euro Call': EuropeanCallOption(Strike=params['K'], Maturity=params['T']),
            'Euro Put': EuropeanPutOption(Strike=params['K'], Maturity=params['T']),
            # (...)
        }

        return {name: model.priceOption(opt) for name, opt in options.items()}

    def run_parameter_impact(self, param_name, values, output_plot = False):
        results = {'Euro Call': [], 'Euro Put': []} # also only european options for now

        for val in values:
            current_params = self.baseline.copy()
            current_params[param_name] = val
            prices = self.get_all_prices(current_params)

            for key in results.keys():
                results[key].append(prices[key])

        if output_plot:
            plt.figure(figsize=(10, 6))
            for name, prices in results.items():
                plt.plot(values, prices, label=name)
            plt.title(f'Impact of {param_name} on option prices')
            plt.xlabel(f'{param_name}')
            plt.ylabel('Option Price')
            plt.legend()
            plt.grid(True)
            plt.show()

        return results

