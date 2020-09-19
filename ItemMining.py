from Dataset import Dataset
import itertools


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

    def __init__(self, X, Y, sup, conf):
        self.X = X
        self.Y = Y
        self.sup = sup
        self.conf = conf

    def setParam(self, sup, conf):
        self.sup = sup
        self.conf = conf

    def __str__(self):
        return "Rule: " + str(self.X) + " --> " + str(self.Y) + " Support: " + str(self.sup) \
               + " Condifence: " + str(self.conf)


def nextlayer(c):
    layer = []
    for a in c:
        if not a.getChildren() is None:
            layer += a.getChildren()
    return layer


def subsets(A, m):
    """Returns all subsets of list A with at least m elements"""
    sub = []
    for i in range(m, len(A)):
        sub = sub + list(itertools.combinations(A, i))
    return sub


class ItemMining:
    """Main class used for Itemset Mining. Zaki and Meira book, Chapter 8."""

    def __init__(self, addr, minSup=3, minConf=0.5):
        self.table = Dataset(addr)
        self.root = Itemset()
        self.minSup = minSup
        self.minConf = minConf

    def setMinSup(self, minSup):
        self.minSup = minSup

    def setMinConf(self, minConf):
        self.minConf = minConf

    def runApriori(self):
        frequent = []
        k = 1
        c = {k: self.root}
        c[k].addChildren([Itemset(c[k], [x]) for x in self.table.getTable().columns])
        k += 1
        c[k] = c[k - 1].getChildren()
        while c[k]:
            for i in c[k]:
                sup = self.table.computeSupport(i.getItemset())
                if sup >= self.minSup:
                    frequent.append(i)
                    i.addSupport(sup)
                else:
                    i.getParent().delChild(i)
                    if i in c[k]:
                        c[k].remove(i)
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
        return nextlayer(c)

    def associationRules(self):
        """Generate a list of association rules given a list of frequent itemsets and a minimum confidence parameter"""
        rules = []
        frequent = self.runApriori()
        for z in frequent:
            supZ = z.getSupport()  # Uses the support that was previously calculated
            z = z.getItemset()
            if len(z) >= 2:
                A = subsets(z, 1)  # Set of antecedents is initialized using all the nonempty subsets of z
                while len(A) > 0:
                    X = list(A[-1])  # Start from the last itemset because it has more elements
                    A = A[0:-1]  # A<-A/X
                    c = supZ / self.table.computeSupport(X)  # Computes confidence
                    if c >= self.minConf:
                        rules.append(Rule(X, list(set(z) - set(X)), supZ, c))  # creates the Rule (X->Z\X, sup(Z), c)
                    else:
                        # Remove all subsets of X from A
                        A = list(set(A) - set(subsets(X, 1)))

        return rules

    def rankRules(self):
        return self.table


if __name__ == '__main__':
    table = ItemMining("Dataset/txn_by_dept.csv", minSup=3, minConf=0.5)
    print("***********************************************************")
    print("***********************************************************")
    print("1: Printing frequent itemsets")
    print("***********************************************************")
    print("***********************************************************")
    fset = table.runApriori()
    for itemset in fset:
        print(itemset)

    print("***********************************************************")
    print("***********************************************************")
    print("2: Printing strong association rules")
    print("***********************************************************")
    print("***********************************************************")
    rules = table.associationRules()
    for rule in rules:
        print(rule)
