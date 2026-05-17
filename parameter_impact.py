import numpy as np
import matplotlib.pyplot as plt
from binomial import european_option_binomial

# Initialize baseline parameters
baseline = {
    'S0': 50,
    'K': 48,
    'T': 2,
    'r': 0.02,
    'sigma': 0.3,
    'dt': 1 / 12
}

# Initialize parameter grids

grids = {
    'S0': np.arange(30, 71, 2),
    'K': np.arange(30, 71, 2),
    'T': np.arange(0.25, 5.1, 0.25),
    'sigma': np.arange(0.05, 0.8, 0.05),
    'r': np.arange(0, 0.15, 0.01)
}

def analyze_param_impact(param_name, grid_values, base_params):
    """
    Analyzes and plots the impact of a single parameter on Call and Put prices.
    Returns the parameter grid along with lists of Call and Put prices.
    """
    call_prices = []
    put_prices = []

    current_params = base_params.copy()

    for val in grid_values:
        current_params[param_name] = val

        c_price = european_option_binomial(
            S0=current_params['S0'],
            K=current_params['K'],
            T=current_params['T'],
            r=current_params['r'],
            sigma=current_params['sigma'],
            dt=current_params['dt'],
            option_type="call"
        )
        p_price = european_option_binomial(
            S0=current_params['S0'],
            K=current_params['K'],
            T=current_params['T'],
            r=current_params['r'],
            sigma=current_params['sigma'],
            dt=current_params['dt'],
            option_type="put"
        )

        call_prices.append(c_price)
        put_prices.append(p_price)

    # Plotting code setup
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(f'Impact of {param_name} on Option Prices')

    # Call Plot
    axs[0].plot(grid_values, call_prices, color='blue', label='Call')
    axs[0].set_title(f'Call')
    axs[0].set_xlabel(param_name)
    axs[0].set_ylabel('Price')
    axs[0].grid(True)

    # Put Plot
    axs[1].plot(grid_values, put_prices, color='red', label='Put')
    axs[1].set_title(f'Put')
    axs[1].set_xlabel(param_name)
    axs[1].set_ylabel('Price')
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

    return call_prices, put_prices, grid_values

for param, grid in grids.items():
    analyze_param_impact(param, grid, baseline)


