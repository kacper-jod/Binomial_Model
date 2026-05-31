import numpy as np
from EuropeanOptions import *
from AmericanOptions import *
from MarketModel import MarketModel
from AnalysisRunner import AnalysisRunner
from DrawTree import *
from Hedge import *

S0 = 20
K = 21
T = .8
sigma = 0.3
r = 0.12
dt = 1 / 4  #changed from 1/12, its too much for now, we have too big tree

BinomialMarketModel = MarketModel(SpotPrice = S0, 
                                  up = 1.1,#np.exp(sigma * np.sqrt(dt)),
                                  down = .9,#np.exp((-1) * sigma * np.sqrt(dt)),
                                  risk_free_rate = r,
                                  delta_T = dt, 
                                  max_maturity = T )

# draw_horizontal_tree(array_to_tree(BinomialMarketModel))

E_Call = EuropeanCallOption(Strike = K, Maturity = T)
E_Put = EuropeanPutOption(Strike = K, Maturity = T)

A_Call = AmericanCallOption(Strike = K, Maturity = T)
A_Put = AmericanPutOption(Strike = K, Maturity = T)

E_Call_Value = BinomialMarketModel.priceOption(E_Call)
E_Put_Value = BinomialMarketModel.priceOption(E_Put)

A_Call_Value = BinomialMarketModel.priceOption(A_Call)
A_Put_Value = BinomialMarketModel.priceOption(A_Put)

# print(BinomialMarketModel.starting_node)

print("European Call:", E_Call_Value)
print("European Put :", E_Put_Value)

print("American Call:", A_Call_Value)
print("American Put :", A_Put_Value)

# sprawdzenie wyników parytetem put - call

print("\nCall-put parity:")
print("C - P =", E_Call_Value - E_Put_Value)
print("S0 - K*exp(-rT) =", S0 - K * np.exp(-r * T))
print("Difference =", abs((E_Call_Value - E_Put_Value) - (S0 - K * np.exp(-r * T))))

# Rysuj drzewa z informacjami o early exercise
A_Call_values, A_Call_exercise = A_Call.generateOptionValueTree(BinomialMarketModel)
#A_Put_values, A_Put_exercise = A_Put.generateOptionValueTree(BinomialMarketModel)

print(array_to_layers(A_Call_values, BinomialMarketModel))
print(A_Call_exercise)

##draw_horizontal_tree(array_to_layers(BinomialMarketModel), type='Euro Call', Strike = K)
draw_horizontal_tree(
    array_to_layers(A_Call_values, BinomialMarketModel),
    array_to_layers(A_Call_exercise, BinomialMarketModel),
    array_to_layers(BinomialMarketModel.tree, BinomialMarketModel))
#draw_horizontal_tree(
#    array_to_layers(A_Put_values, BinomialMarketModel),
#    array_to_layers(A_Put_exercise, BinomialMarketModel),
#    array_to_layers(BinomialMarketModel.tree, BinomialMarketModel))

hedge_test = Hedge(BinomialMarketModel, A_Call)
print(hedge_test.generate_hedging_portfolios()[1].delta, hedge_test.generate_hedging_portfolios()[1].alpha)



# analiza cen dla zmieniających się parametrów

baseline = {
    'S0': S0, 'K': K, 'T': T,
    'r': r, 'sigma': sigma, 'dt': dt
}

#runner = AnalysisRunner(baseline)
#
#print("Baseline Prices:", runner.get_all_prices(baseline))
#
#density_of_points = 10 # greater is denser
#
#grids = {
#    'S0': np.arange(0, 100, 2 / density_of_points),
#    'K': np.arange(30, 71, 2 / density_of_points),
#    'sigma': np.arange(0.05, 2, 0.05 / density_of_points),
#    'T': np.arange(0.25, 10, 0.25 / density_of_points)
#}
#
#for param, values in grids.items():
#    print(f'analysing impact of {param} on the option price...')
#    data = runner.run_parameter_impact(param, values, output_plot = True, check_inequalities=True)
#
#baseline = {
#    'S0': S0, 'K': K, 'T': T,
#    'r': r, 'sigma': sigma, 'dt': dt
#}
#
#grids = {
#    'S0': np.arange(0, 100, 2),
#    'r': np.arange(0.0, 1, 0.01)
#}
#
#runner = AnalysisRunner(baseline)
#
#runner.plot_surface(grids, 'S0', 'r', 'Put Diff')
#

