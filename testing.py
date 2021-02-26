from btree import Btree

bt = Btree(3)

bt.insert(5, 0)
bt.insert(12, 0)
bt.insert(7, 0)
bt.insert(3, 0)
bt.insert(2, 0)
bt.insert(10, 0)

bt.delete(10,0)

bt.insert(8,0)
bt.insert(0,0)
bt.insert(1,0)
bt.insert(6,0)
bt.insert(13,0)
bt.insert(11,0)

bt.delete(12,0)

bt.delete(0,0)
bt.delete(8,0)
bt.insert(8,0)

bt.delete(11, 0)
bt.insert(14, 0)

bt.delete(8, 0)

bt.delete(3,0)

bt.plot()