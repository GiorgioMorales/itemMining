from Dataset import Dataset


class Itemset:
    """Helper class used to describe each node in the tree."""

    def __init__(self, parent=None, itemset=None):
        self.parent = parent
        self.children = None
        self.X = itemset
        self.support = 0

    def addChildren(self, children=None):
        self.children = children

    def getChildren(self):
        return self.children

    def getSiblings(self):
        return self.parent.children  # ... \X

    def getItemset(self):
        return self.X


class ItemMining:
    """Main class used for Itemset Mining. Zaki and Meira book, Chapter 8."""

    def __init__(self, addr, minSup=3, minConf=0.5):
        self.table = Dataset(addr)
        self.root = Itemset()
        self.minSup = minSup
        self.minConf = minConf

    def runApriori(self):
        frequent = []
        k = 1
        c = {k: list([el] for el in self.table.columns)}
        while c[k]:
            support = Dataset.computeSupport(c[k], self.table)
            newLayer = []
            for i in range(len(c[k])):
                if support[i] >= self.minSup:
                    frequent.append(c[k][i])
                    newLayer.append(c[k][i])
            k += 1
            c[k] = self.extendPrefixTree(newLayer)
        return frequent

    def extendPrefixTree(self, c):
        return self.table

    def associationRules(self):
        return self.table

    def rankRules(self):
        return self.table


if __name__ == '__main__':
    table = ItemMining("addr//txn_by_dept.csv", minSup=3, minConf=0.5)
