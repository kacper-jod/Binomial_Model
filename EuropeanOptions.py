import numpy as np

class EuropeanCallOption:
    def __init__(self, Strike, Maturity):
        self.Strike = Strike
        self.Maturity = Maturity
    def value(self, BasePrice):
        return max(BasePrice - self.Strike, 0)
    
    def generateOptionValueTree(self, market_model):
        #set last layer
        option_value_tree = np.zeros_like(market_model.tree)
        exercise_tree = np.zeros_like(market_model.tree)  # 1 = early exercise (intrinsic), 0 = continuation value
        for el_numb in range(1,market_model.number_of_layers + 1):
            option_value_tree[market_model.getTreeId(market_model.number_of_layers, el_numb)] = \
                self.value(market_model.getTreeNodeValue(market_model.number_of_layers, el_numb))
            exercise_tree[market_model.getTreeId(market_model.number_of_layers, el_numb)] = 1  # At maturity, always intrinsic
        
        #set rest of the layers
        for layer in range(market_model.number_of_layers - 1, 0, -1):
            for el_numb in range(1, layer + 1):
                option_value_tree[market_model.getTreeId(layer,el_numb)] = \
                    np.exp(-market_model.risk_free_rate * market_model.delta_T) * \
                        (market_model.p * option_value_tree[market_model.getTreeId(layer+1,el_numb)] + \
                        (1-market_model.p) * option_value_tree[market_model.getTreeId(layer+1,el_numb+1)])
        return option_value_tree, exercise_tree


class EuropeanPutOption:
    def __init__(self, Strike, Maturity):
        self.Strike = Strike
        self.Maturity = Maturity
    def value(self, BasePrice):
        return max(self.Strike - BasePrice, 0)
    
    def generateOptionValueTree(self, market_model):
        #set last layer
        option_value_tree = np.zeros_like(market_model.tree)
        exercise_tree = np.zeros_like(market_model.tree)  # 1 = early exercise (intrinsic), 0 = continuation value
        for el_numb in range(1,market_model.number_of_layers + 1):
            option_value_tree[market_model.getTreeId(market_model.number_of_layers, el_numb)] = \
                self.value(market_model.getTreeNodeValue(market_model.number_of_layers, el_numb))
            exercise_tree[market_model.getTreeId(market_model.number_of_layers, el_numb)] = 1  # At maturity, always intrinsic
        
        #set rest of the layers
        for layer in range(market_model.number_of_layers - 1, 0, -1):
            for el_numb in range(1, layer + 1):
                option_value_tree[market_model.getTreeId(layer,el_numb)] = \
                    np.exp(-market_model.risk_free_rate * market_model.delta_T) * \
                        (market_model.p * option_value_tree[market_model.getTreeId(layer+1,el_numb)] + \
                        (1-market_model.p) * option_value_tree[market_model.getTreeId(layer+1,el_numb+1)])
        return option_value_tree, exercise_tree
                

    
    