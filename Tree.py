class Node:
    def __init__(self, underlying_price, layer):
        self.underlying_price = underlying_price
        self.layer = layer
        self.up = None
        self.down = None
    def setUp(self, node):
        self.up = node
    def setDown(self, node):
        self.down = node