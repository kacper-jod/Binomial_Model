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
        number_of_layers = self.max_maturity / self.delta_T

        queue = [self.starting_node]
        
        while len(queue) > 0:
            #print("Queue size: ", len(queue))
            active_node = queue.pop(0)
            #print("Generating tree node: ", active_node.underlying_price)
            if active_node.layer >= number_of_layers:
                continue
            up_node = Node(active_node.underlying_price * self.up, layer=active_node.layer + 1)
            down_node = Node(active_node.underlying_price * self.down, layer=active_node.layer + 1)
            active_node.setUp(up_node)
            active_node.setDown(down_node)
            queue.append(up_node)
            queue.append(down_node)

    def priceOption(self, option, node = None):
        if node == None:
            node = self.starting_node
        if node.up == None and node.down == None:
            return option.value(node.underlying_price)
        if node.up == None or node.down == None:
            raise Exception("Node with only one child missing")
        
        return np.exp(-self.risk_free_rate * self.delta_T) * \
            (self.p * self.priceOption(option,node.up) + (1-self.p) * self.priceOption(option,node.down))
        
