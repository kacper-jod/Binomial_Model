import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from MarketModel import MarketModel
from EuropeanOptions import EuropeanCallOption, EuropeanPutOption
from AmericanOptions import AmericanCallOption, AmericanPutOption


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

        options = {
            'Euro Call': EuropeanCallOption(Strike=params['K'], Maturity=params['T']),
            'Euro Put': EuropeanPutOption(Strike=params['K'], Maturity=params['T']),
            'American Call': AmericanCallOption(Strike=params['K'], Maturity=params['T']),
            'American Put': AmericanPutOption(Strike=params['K'], Maturity=params['T']),
        }

        return {name: model.priceOption(opt) for name, opt in options.items()}

    def run_parameter_impact(self, param_name, values, output_plot = False):
        results = {'Euro Call': [], 'Euro Put': [], 'American Call': [], 'American Put': []}

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

    def plot_volatility_maturity_surface(self, values, option_type):
        if 'T' not in values.keys():
            raise ValueError('please provide maturity grid')
        if 'sigma' not in values.keys():
            raise ValueError('please provide volatility grid')

        prices = np.zeros([len(values['T']), len(values['sigma'])])
        for i, T in enumerate(values['T']):
            for j, sigma in enumerate(values['sigma']):
                params = self.baseline.copy()
                params['T'] = T
                params['sigma'] = sigma

                market = self.create_model(params)

                if option_type == 'Euro Call':
                    option = EuropeanCallOption(Strike=params['K'], Maturity=params['T'])
                elif option_type == 'Euro Put':
                    option = EuropeanPutOption(Strike=params['K'], Maturity=params['T'])
                elif option_type == 'American Call':
                    option = AmericanCallOption(Strike=params['K'], Maturity=params['T'])
                elif option_type == 'American Put':
                    option = AmericanPutOption(Strike=params['K'], Maturity=params['T'])
                else:
                    raise ValueError('please provide existing option type')

                prices[i, j] = market.priceOption(option)

        fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
        X, Y = np.meshgrid(values['sigma'], values['T'])
        ax.plot_surface(X, Y, prices, cmap=cm.cividis)

        plt.show()


