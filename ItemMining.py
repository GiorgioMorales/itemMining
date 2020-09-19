from Dataset import Dataset
import datetime


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
        return self.parent.children  # ... \X

    def getItemset(self):
        return self.X

    def addSupport(self, support):
        self.support = support

    def getSupport(self):
        return self.support

    def delChild(self, child):
        self.children.remove(child)


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
        c = {k: self.root}
        c[k].addChildren([Itemset(c[k], [x]) for x in self.table.getTable().columns])
        k += 1
        c[k] = c[k - 1].getChildren()
        while c[k]:
            print(k)
            for i in c[k]:
                a = datetime.datetime.now()
                sup = self.table.computeSupport(i.getItemset())
                b = datetime.datetime.now()
                tt = b - a
                print(tt.microseconds/1000)
                if sup >= self.minSup:
                    frequent.append(i.getItemset())
                    i.addSupport(sup)
                else:
                    i.getParent().delChild(i)
            k += 1
            c[k] = self.extendPrefixTree(c[k - 1])
        return frequent

    def extendPrefixTree(self, c):
        for a in c:
            for b in a.getSiblings()[a.getSiblings().index(a) + 1:]:
                temp = list(set(a.getItemset() + b.getItemset()))
                if a.getSupport() < self.minSup or b.getSupport() < self.minSup:
                    temp = None
                if temp:
                    if a.getChildren():
                        t = a.getChildren()
                        t.append(Itemset(a, temp))
                        a.addChildren(t)
                    else:
                        a.addChildren([Itemset(a, temp)])
            if not a.getChildren():
                temp = a.getParent()
                temp.delChild(a)
                while temp.getChildren() == [] and temp.getItemset() is not None:
                    t = temp.getParent()
                    t.delChild(temp)
                    temp = t
        return self.nextlayer(c)

    def nextlayer(self, c):
        layer = []
        for a in c:
            if not a.getChildren() is None:
                layer += a.getChildren()
        return layer

    def associationRules(self):
        return self.table

    def rankRules(self):
        return self.table


if __name__ == '__main__':
    table = ItemMining("Dataset/txn_by_dept.csv", minSup=3, minConf=0.5)
    fset = table.runApriori()
    print(fset)
