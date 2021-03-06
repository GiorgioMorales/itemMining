from optparse import OptionParser

from Dataset import Dataset
from ItemsetRule import *
import itertools


# Static methods
def nextLayer(c):
    """Returns the set of itemsets of the next layer of the tree"""
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


def rankRules(ruls, k):
    """Selects the top k association rules based on a measure m"""
    # Sort and filter the rules using the relative support as the first criteria
    s = sorted(ruls, key=lambda i: (i.conf, i.rsup, i.leverage, -i.itemsTotal), reverse=True)
    s = s[0:k]
    return s


class ItemMining:
    """Main class used for Itemset Mining. Zaki and Meira book, Chapter 8."""

    def __init__(self, addr, minSup=3, minConf=0.4):
        self.table = Dataset(addr)
        self.root = Itemset()
        self.minSup = minSup
        self.minConf = minConf

    def setMinSup(self, minSup):
        self.minSup = minSup

    def setMinConf(self, minConf):
        self.minConf = minConf

    def runApriori(self):
        """
        The Apriori Algorithm that generates a frequent itemset based off of the table submitted in the Dataset
        """
        frequent = []
        k = 1
        c = {k: self.root}
        c[k].addChildren([Itemset(c[k], [x]) for x in self.table.getTable().columns])
        k += 1
        c[k] = c[k - 1].getChildren()
        while c[k]:  # While the layer is not empty
            for i in c[k]:  # For each leaf in layer C^k
                sup = self.table.computeSupport(i.getItemset())  # Calculates teh support of the leaf
                if sup >= self.minSup:
                    frequent.append(i)
                    i.addSupport(sup)
                else:
                    i.getParent().delChild(i)
                    if i in c[k]:
                        c[k].remove(i)
            k += 1
            c[k] = self.extendPrefixTree(c[k - 1])  # Creates next layer based off of current layer
        return frequent

    def extendPrefixTree(self, c):
        """
        Creates the next layer of the prefix tree given a layer c
        """
        for a in c:
            for b in a.getSiblings()[a.getSiblings().index(a) + 1:]:
                temp = list(set(a.getItemset() + b.getItemset()))  # Ca U Cb
                if a.getSupport() < self.minSup or b.getSupport() < self.minSup:  # Determines if Ca U Cb contains
                    # any elements that are below minimal support
                    temp = None
                if temp:
                    if a.getChildren():
                        t = a.getChildren()
                        t.append(Itemset(a, temp))
                        a.addChildren(t)
                    else:
                        a.addChildren([Itemset(a, temp)])
            if not a.getChildren():  # If the leaf is the end of the branch, delete the leaf and the childless ancestors
                temp = a.getParent()
                temp.delChild(a)
                while temp.getChildren() == [] and temp.getItemset() is not None:
                    t = temp.getParent()
                    t.delChild(temp)
                    temp = t
        return nextLayer(c)

    def associationRules(self):
        """Generate a list of association rules given a list of frequent itemsets and a minimum confidence parameter"""
        arules = []
        frequent = self.runApriori()
        for z in frequent:
            supZ = z.getSupport()  # Uses the support that was previously calculated
            z = z.getItemset()
            if len(z) >= 2:
                A = subsets(z, 1)  # Set of antecedents is initialized using all the nonempty subsets of z
                while len(A) > 0:
                    X = list(A[-1])  # Start from the last itemset because it has more elements
                    A = A[0:-1]  # A<-A/X
                    sx = self.table.computeSupport(X)
                    c = supZ / sx  # Computes confidence
                    if c >= self.minConf:
                        sy = self.table.computeSupport(list(set(z) - set(X)))  # computes relative support of Z\X
                        arules.append(Rule(X, list(set(z) - set(X)), supZ, c, sx, sy,
                                           self.table.binary.shape[0]))  # creates the Rule (X->Z\X, sup(Z), c, |D|)
                    else:
                        # Remove all subsets of X from A
                        A = list(set(A) - set(subsets(X, 1)))

        return arules


if __name__ == '__main__':

    # Parse input arguments
    optparser = OptionParser()
    optparser.add_option('-s', '--minSup', dest='minS', default=4, type='float')
    optparser.add_option('-c', '--minConf', dest='minC', default=0.4, type='float')
    (options, args) = optparser.parse_args()

    table = ItemMining("Dataset/txn_by_dept.csv", minSup=options.minS, minConf=options.minC)
    print("***********************************************************")
    print("***********************************************************")
    print("1: Printing frequent itemsets")
    print("***********************************************************")
    print("***********************************************************")
    fset = table.runApriori()
    for iset in fset:
        print(iset)

    print("\n\n***********************************************************")
    print("***********************************************************")
    print("2: Printing strong association rules")
    print("***********************************************************")
    print("***********************************************************")
    rules = table.associationRules()
    for rule in rules:
        print(rule)

    print("\n\n***********************************************************")
    print("***********************************************************")
    print("3: Rank association rules")
    print("***********************************************************")
    print("***********************************************************")
    score = "confidence"  # Select score. Options: 'support', 'confidence', 'lift', and 'leverage'
    topRules = rankRules(rules, k=30)
    for rule in topRules:
        print(rule)
