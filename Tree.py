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

    def isLast(self):
        if self.up == None and self.down == None:
            return True
        return False

    def isCorrupted(self):
        if (self.up == None and self.down != None) or (self.up != None and self.down == None):
            return True
        return False

    def __str__(self):
        ret = str(self.underlying_price) + " :"
        if not self.isLast() and not self.isCorrupted():
            ret += "Up: " + str(self.up.underlying_price) + " | Down: " + str(self.down.underlying_price)
            ret += str(self.up)
            ret += str(self.down)
        else:
            ret += " - \n - "
        return ret