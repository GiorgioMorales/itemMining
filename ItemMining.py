from Dataset import Dataset


class Itemset:
    """Helper class used to describe each node in the tree."""

    def __init__(self, parent=None, itemset=None):
        self.parent = parent
        self.children = None
        self.X = itemset

    def addChildren(self, children=None):
        self.children = children

    def getChildren(self):
        return self.children

    def getSiblings(self):
        return self.parent.children  # ... \X


class ItemMining:
    """Main class used for Itemset Mining. Zaki and Meira book, Chapter 8."""

    def __init__(self, addr, minSup=3, minConf=0.5):
        self.table = Dataset(addr)
        self.root = []
        self.minSup = minSup
        self.minConf = minConf

    def runApriori(self):
        return self.table

    def extendPrefixTree(self):
        return self.table

    def associationRules(self):
        return self.table

    def rankRules(self):
        return self.table


if __name__ == '__main__':
    table = ItemMining("addr//txn_by_dept.csv", minSup=3, minConf=0.5)
