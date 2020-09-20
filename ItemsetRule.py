class Itemset:
    """Helper class used to describe each node in the tree."""

    def __init__(self, parent=None, itemset=None):
        self.parent = parent
        self.children = None
        self.X = itemset
        self.support = 0

    def getParent(self):
        return self.parent

    def addChildren(self, children=None):
        self.children = children

    def getChildren(self):
        return self.children

    def getSiblings(self):
        return self.parent.children

    def getItemset(self):
        return self.X

    def addSupport(self, support):
        self.support = support

    def getSupport(self):
        return self.support

    def delChild(self, child):
        self.children.remove(child)

    def __str__(self):
        return str(self.X)


class Rule:
    """Helper class used to describe an association rule."""

    def __init__(self, X, Y, sup, conf, supx, supy, D):
        self.X = X
        self.Y = Y
        self.sup = sup
        self.conf = conf
        self.D = D
        self.rsup = self.sup / self.D
        self.rsupx = supx / self.D
        self.rsupy = supy / self.D
        self.lift = self.conf / self.rsupy
        self.leverage = self.rsup - self.rsupx * self.rsupy
        self.itemsTotal = len(self.X) + len(self.Y)

    def setParam(self, sup, conf):
        self.sup = sup
        self.conf = conf

    def __str__(self):
        return "Rule: " + str(self.X) + " --> " + str(self.Y) + " Support: " + str(self.sup) \
               + " Condifence: " + str(self.conf) + " Lift: " + str(self.lift) + " Leverage: " + str(self.leverage)
