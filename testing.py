from btree import Btree

bt = Btree(3)

bt.insert(5, 0)
bt.insert(12, 1)
bt.insert(7, 2)
bt.insert(3, 3)
bt.insert(2, 4)
bt.insert(10, 5)

bt.plot()