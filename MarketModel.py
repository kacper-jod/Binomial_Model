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
        # Layer X , Number Y --> Up: X+1, Y     Down: X+1, Y+1
        self.number_of_layers = int(self.max_maturity / self.delta_T)
        self.tree = np.zeros(self.number_of_layers * (self.number_of_layers+1) // 2 + 1)

<<<<<<< HEAD
        self.generateArrayPriceTree()

    def getTreeId(self, layer, number_of_elem):
        return ((layer-1)*layer//2 + 1) + (number_of_elem - 1)\
            
    def getTreeNodeValue(self, layer, number_of_elem):
        id = self.getTreeId(layer, number_of_elem)
        return self.tree[id]
    
    def setTreeNodeValue(self, layer, number_of_elem, value):
        id = self.getTreeId(layer, number_of_elem)
        self.tree[id] = value

    def printTree(self):
        for layer in range(1,self.number_of_layers+1):
            for numb in range(1,layer+1):
                print(self.getTreeNodeValue(layer,numb),end="   ")
            print("\n")

    def generateArrayPriceTree(self):
        # Generate recombining tree
        self.setTreeNodeValue(1,1,self.SpotPrice)

        for layer_number in range(2,self.number_of_layers + 1):
            self.setTreeNodeValue(layer_number,1,
                                  self.getTreeNodeValue(layer_number-1,1) * self.up)
            
            for element_number in range(2,layer_number+1):
                self.setTreeNodeValue(layer_number,element_number,
                                      self.getTreeNodeValue(layer_number-1,element_number-1) * self.down)

    def priceOption(self,option,layer=1,number_of_elem=1):
        # set last layer
        option_value_tree = np.zeros_like(self.tree)
        for el_numb in range(1,self.number_of_layers + 1):
            option_value_tree[self.getTreeId(self.number_of_layers, el_numb)] = \
                option.value(self.getTreeNodeValue(self.number_of_layers, el_numb))
        
        #set rest of the layers
        for layer in range(self.number_of_layers - 1, 0, -1):
            for el_numb in range(1, layer + 1):
                option_value_tree[self.getTreeId(layer,el_numb)] = \
                    np.exp(-self.risk_free_rate * self.delta_T) * \
                        (self.p * option_value_tree[self.getTreeId(layer+1,el_numb)] + \
                        (1-self.p) * option_value_tree[self.getTreeId(layer+1,el_numb+1)])
=======
    def priceOption(self, option):
        return option.priceOnMarket(self)
>>>>>>> 0fd0e63 (Added basic American Option logic - seems not to work for now)
        
        return option_value_tree[self.getTreeId(1,1)]