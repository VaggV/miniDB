from btree import Btree

bt = Btree(3)

bt.insert(5, 0)
bt.insert(12, 1)
bt.insert(7, 2)
bt.insert(3, 3)
bt.insert(2, 4)
bt.insert(10, 5)
#bt.insert(8, 6)

bt.delete(12,1)
bt.delete(7,2)
bt.delete(3,3)

bt.plot()