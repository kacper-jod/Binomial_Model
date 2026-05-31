class Portfolio:
    def __init__(self, cash_asset, delta=0, alpha=0):
        self.cash = cash_asset
        self.delta = delta
        self.alpha = alpha

    def get_value_at_start(self, stock_price):
        return self.delta * stock_price + self.alpha

    def get_value_at_end(self, stock_price, dt):
        share_value = self.delta * stock_price
        cash_value = self.cash.grow(self.alpha, dt)
        return share_value + cash_value