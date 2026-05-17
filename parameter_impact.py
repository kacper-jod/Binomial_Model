import numpy as np
import matplotlib.pyplot as plt
from MarketModel import MarketModel
from EuropeanOptions import EuropeanCallOption, EuropeanPutOption

baseline = {
    'S0': 50.0,
    'K': 48.0,
    'T': 2.0,
    'r': 0.02,
    'sigma': 0.3,
    'dt': 1 / 4
}

grids = {
    'S0': np.arange(30, 71, 2),
    'K': np.arange(30, 71, 2),
    'T': np.arange(0.25, 4.26, 0.25),
    'sigma': np.arange(0.05, 0.8, 0.05),
    'r': np.arange(0, 0.15, 0.01)
}

def analyze_param_impact(param_name, grid_values, base_params):
    call_prices = []
    put_prices = []

    current_params = base_params.copy()

    for val in grid_values:
        print(val)
        current_params[param_name] = val

        u = np.exp(current_params['sigma'] * np.sqrt(current_params['dt']))
        d = np.exp(-current_params['sigma'] * np.sqrt(current_params['dt']))

        model = MarketModel(
            SpotPrice=current_params['S0'],
            up=u,
            down=d,
            risk_free_rate=current_params['r'],
            delta_T=current_params['dt'],
            max_maturity=current_params['T']
        )

        call_option = EuropeanCallOption(Strike=current_params['K'], Maturity=current_params['T'])
        put_option = EuropeanPutOption(Strike=current_params['K'], Maturity=current_params['T'])

        c_price = model.priceOption(call_option)
        p_price = model.priceOption(put_option)

        call_prices.append(c_price)
        put_prices.append(p_price)

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(f'Analiza wrażliwości: Wpływ parametru "{param_name}" na ceny opcji')

    axs[0].plot(grid_values, call_prices, color='blue', label='Call')
    axs[0].set_title(f'Opcja Europejska Call')
    axs[0].set_xlabel(param_name)
    axs[0].set_ylabel('Cena Opcji')
    axs[0].grid(True)

    axs[1].plot(grid_values, put_prices, color='red', label='Put')
    axs[1].set_title(f'Opcja Europejska Put')
    axs[1].set_xlabel(param_name)
    axs[1].set_ylabel('Cena Opcji')
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

    return call_prices, put_prices, grid_values

for param, grid in grids.items():
    analyze_param_impact(param, grid, baseline)