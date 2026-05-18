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
        self.starting_node = Node(self.SpotPrice, layer=0)

        self.generatePriceTree()

    def generatePriceTree(self):
        number_of_layers = int(self.max_maturity / self.delta_T)

        array_of_previous_nodes = [self.starting_node]

        for layer in range(1,number_of_layers + 1):
            array_of_new_nodes = []

            for i in range(layer+1):
                array_of_new_nodes.append(Node(0,layer))
            
            for id in range(layer):
                array_of_previous_nodes[id].setUp(array_of_new_nodes[id])
                array_of_new_nodes[id].underlying_price = array_of_previous_nodes[id].underlying_price * self.up
                array_of_previous_nodes[id].setDown(array_of_new_nodes[id+1])
                array_of_new_nodes[id+1].underlying_price = array_of_previous_nodes[id].underlying_price * self.down

            array_of_previous_nodes = array_of_new_nodes

    def priceOption(self, option, node = None):
        if node == None:
            node = self.starting_node
        if node.up == None and node.down == None:
            return option.value(node.underlying_price)
        if node.up == None or node.down == None:
            raise Exception("Node with only one child missing")
        
        return np.exp(-self.risk_free_rate * self.delta_T) * \
            (self.p * self.priceOption(option,node.up) + (1-self.p) * self.priceOption(option,node.down))
        
