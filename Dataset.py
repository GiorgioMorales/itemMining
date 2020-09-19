import numpy as np
import pandas as pd


class Dataset:

    def __init__(self, addr="dataset/txn_by_dept.csv"):
        """ Initialize table reading the data from the specified address"""
        data = pd.read_csv(addr)
        df = pd.DataFrame(data, columns=['POS Txn', 'ID'])
        rows = df['POS Txn'].unique()
        cols = df['ID'].unique()
        binary = np.zeros((df['POS Txn'].unique().size, cols.size))
        for ind in df.index:
            binary[np.where(rows == df['POS Txn'][ind])[0][0]][np.where(cols == df['ID'][ind])[0][0]] = 1
        self.binary = pd.DataFrame(binary, columns=cols, index=rows)

    def getTable(self):
        return self.binary

    def computeSupport(self, c):
        index = 0
        s = 0
        # for k in self.binary.index:
        #     if all(self.binary.loc[k][elem] == 1 for elem in c):
        #         s += 1
        # index += 1

        # Creates a column of ones
        multColumn = np.ones(self.binary.shape[0])
        for elem in c:
            multColumn *= self.binary[elem].to_numpy()

        return np.sum(multColumn)




