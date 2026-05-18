import numpy as np

class AmericanCallOption:
    def __init__(self, Strike, Maturity):
        self.Strike = Strike
        self.Maturity = Maturity

    def payoffAtPoint(self, BasePrice):
        return max(BasePrice - self.Strike, 0)
    
    def priceOnMarket(self, market, node = None):
        if node == None:
            node = market.starting_node

        if node.isLast():
            return self.payoffAtPoint(node.underlying_price)
        
        if node.isCorrupted():
            raise Exception("Node with only one child missing")
        
        return max(
            np.exp(-market.risk_free_rate * market.delta_T) * \
            (market.p * self.priceOnMarket(market,node.up) + (1-market.p) * self.priceOnMarket(market,node.down)),
            self.payoffAtPoint(node.underlying_price))
    
class AmericanPutOption:
    def __init__(self, Strike, Maturity):
        self.Strike = Strike
        self.Maturity = Maturity

    def payoffAtPoint(self, BasePrice):
        return max(self.Strike - BasePrice, 0)
    
    def priceOnMarket(self, market, node = None):
        if node == None:
            node = market.starting_node

        if node.isLast():
            return self.payoffAtPoint(node.underlying_price)
        
        if node.isCorrupted():
            raise Exception("Node with only one child missing")
        
        return max(
            np.exp(-market.risk_free_rate * market.delta_T) * \
            (market.p * self.priceOnMarket(market,node.up) + (1-market.p) * self.priceOnMarket(market,node.down)),
            self.payoffAtPoint(node.underlying_price))
    
    