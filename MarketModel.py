from Tree import Node
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
        
        # Layer from 1 to number of layers, number of element from 1 to layer_number
        self.number_of_layers = int(self.max_maturity / self.delta_T)
        self.tree = np.zeros(self.number_of_layers * (self.number_of_layers+1) / 2)

        self.generateArrayPriceTree()

    def getTreeNodeValue(self, layer, number):
        id = ((layer-1)*layer/2 + 1) + (number - 1)
        return self.tree[id]
    
    def setTreeNodeValue(self, layer, number, value):
        id = ((layer-1)*layer/2 + 1) + (number - 1)
        self.tree[id] = value

    def generateArrayPriceTree(self):
        # Generate recombining tree
        self.setTreeNodeValue(1,1,self.SpotPrice)

        for layer_number in range(2,self.number_of_layers + 1):
            self.setTreeNodeValue(layer_number,1,
                                  self.getTreeNodeValue(layer_number-1,1) * self.up)
            
            for element_number in range(2,layer_number+1):
                self.setTreeNodeValue(layer_number,element_number,
                                      self.getTreeNodeValue(layer_number-1,element_number-1) * self.down)

    def priceOption(self, option, node = None):
        if node == None:
            node = self.starting_node
        if node.up == None and node.down == None:
            return option.value(node.underlying_price)
        if node.up == None or node.down == None:
            raise Exception("Node with only one child missing")
        
        return np.exp(-self.risk_free_rate * self.delta_T) * \
            (self.p * self.priceOption(option,node.up) + (1-self.p) * self.priceOption(option,node.down))
        
