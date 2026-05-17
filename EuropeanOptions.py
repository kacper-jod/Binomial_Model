import numpy as np

class EuropeanCallOption:
    def __init__(self, Strike, Maturity):
        self.Strike = Strike
        self.Maturity = Maturity
    def value(self, BasePrice):
        return max(BasePrice - self.Strike, 0)
    
class EuropeanPutOption:
    def __init__(self, Strike, Maturity):
        self.Strike = Strike
        self.Maturity = Maturity
    def value(self, BasePrice):
        return max(self.Strike - BasePrice, 0)
    
    