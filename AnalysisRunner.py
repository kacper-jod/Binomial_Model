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

    def run_parameter_impact(self, param_name, values, output_plot=False, check_inequalities=False):
        results = {'Euro Call': [], 'Euro Put': [], 'American Call': [], 'American Put': []}

        # Comprehensive analytical boundaries dictionary
        bounds = {
            'Euro Call LB': [],  # max(0, S0 - K * e^(-rT))
            'Euro Put LB': [],  # max(0, K * e^(-rT) - S0)
            'Euro Put UB': [],  # K * e^(-rT)
            'American Put LB': [],  # max(0, K - S0)
            'American Put UB': []  # K
        }

        for val in values:
            current_params = self.baseline.copy()
            current_params[param_name] = val
            prices = self.get_all_prices(current_params)

            for key in results.keys():
                results[key].append(prices[key])

            if check_inequalities:
                S0 = current_params['S0']
                K = current_params['K']
                r = current_params['r']
                T = current_params['T']

                discount_factor = np.exp(-r * T)

                # Lower and Upper bounds extraction
                bounds['Euro Call LB'].append(max(0, S0 - K * discount_factor))
                bounds['Euro Put LB'].append(max(0, K * discount_factor - S0))
                bounds['Euro Put UB'].append(K * discount_factor)
                bounds['American Put LB'].append(max(0, K - S0))
                bounds['American Put UB'].append(K)

        if output_plot:
            plt.figure(figsize=(12, 8))

            # 1. Plot calculated numerical model prices (solid lines)
            plt.plot(values, results['Euro Call'], label='Euro Call (Model)', color='blue', lw=2)
            plt.plot(values, results['Euro Put'], label='Euro Put (Model)', color='orange', lw=2)
            plt.plot(values, results['American Call'], label='American Call (Model)', color='cyan', lw=1.5,
                     linestyle='-')
            plt.plot(values, results['American Put'], label='American Put (Model)', color='magenta', lw=1.5,
                     linestyle='-')

            # 2. Plot inequality theoretical bounds (dashed/dotted lines)
            if check_inequalities:
                # Call Bounds
                plt.plot(values, bounds['Euro Call LB'], ':', color='darkblue',
                         label='Euro Call Lower Bound ($max(0, S_0 - Ke^{-rT})$)', alpha=0.7)

                # Put Bounds
                plt.plot(values, bounds['Euro Put LB'], ':', color='chocolate',
                         label='Euro Put Lower Bound ($max(0, Ke^{-rT} - S_0)$)', alpha=0.7)
                plt.plot(values, bounds['Euro Put UB'], '--', color='orange',
                         label='Euro Put Upper Bound ($Ke^{-rT}$)', alpha=0.5)

                plt.plot(values, bounds['American Put LB'], '-.', color='darkred',
                         label='American Put Lower Bound ($max(0, K - S_0)$)', alpha=0.7)
                plt.plot(values, bounds['American Put UB'], '--', color='red',
                         label='American Put Upper Bound ($K$)', alpha=0.5)

            # Construct dynamic baseline parameter subtitle (excluding the parameter on the X-axis)
            baseline_info = ", ".join([f"{k}={v}" for k, v in self.baseline.items() if k != param_name])
            full_title = f'Parameter Impact: {param_name} (with Boundary Constraints)\nBaseline: {baseline_info}'

            plt.title(full_title, fontsize=12, pad=15)
            plt.xlabel(f'{param_name}', fontsize=11)
            plt.ylabel('Option Price', fontsize=11)
            plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", frameon=True, facecolor='white')
            plt.grid(True, linestyle=':', alpha=0.5)
            plt.tight_layout()
            plt.show()

        return results

    def plot_surface(self, values, param1_name, param2_name, option_type):
        param1_values = values[param1_name]
        param2_values = values[param2_name]

        prices = np.zeros([len(param2_values), len(param1_values)])

        for i, p2 in enumerate(param2_values):
            for j, p1 in enumerate(param1_values):
                params = self.baseline.copy()
                params[param1_name] = p1
                params[param2_name] = p2

                market = self.create_model(params)

                if option_type == 'Euro Call':
                    option = EuropeanCallOption(Strike=params['K'], Maturity=params['T'])
                elif option_type == 'Euro Put':
                    option = EuropeanPutOption(Strike=params['K'], Maturity=params['T'])
                elif option_type == 'American Call':
                    option = AmericanCallOption(Strike=params['K'], Maturity=params['T'])
                elif option_type == 'American Put':
                    option = AmericanPutOption(Strike=params['K'], Maturity=params['T'])
                elif option_type == 'Call Diff':
                    optionA = AmericanCallOption(Strike=params['K'], Maturity=params['T'])
                    optionE = EuropeanCallOption(Strike=params['K'], Maturity=params['T'])
                elif option_type == 'Put Diff':
                    optionA = AmericanPutOption(Strike=params['K'], Maturity=params['T'])
                    optionE = EuropeanPutOption(Strike=params['K'], Maturity=params['T'])

                else:
                    raise ValueError('please provide existing option type')

                if option_type not in ("Call Diff", "Put Diff"):
                    prices[i, j] = market.priceOption(option)
                else:
                    prices[i, j] = market.priceOption(optionA) - market.priceOption(optionE)
        # Tworzenie wykresu 3D
        fig, ax = plt.subplots(subplot_kw={'projection': '3d'}, figsize=(10, 7))

        # X odpowiada kolumnom (param1), Y odpowiada wierszom (param2)
        X, Y = np.meshgrid(param1_values, param2_values)
        surf = ax.plot_surface(X, Y, prices, cmap=cm.cividis, edgecolor='black')
        #ax.view_init(elev=0, azim = 30)
        # Dynamiczne podpisywanie osi bezpośrednio z nazw kluczy w słowniku
        ax.set_xlabel(param1_name, fontsize=11, labelpad=10)
        ax.set_ylabel(param2_name, fontsize=11, labelpad=10)
        ax.set_zlabel(f'Price ({option_type})', fontsize=11, labelpad=10)

        ax.set_title(f'Option Price Surface: {option_type}', fontsize=14, pad=20)
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1)

        plt.tight_layout()
        plt.show()
