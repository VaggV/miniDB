from btree import Btree

bt = Btree(3)

bt.insert(5, 0)
bt.insert(12, 0)
bt.insert(7, 0)
bt.insert(3, 0)
bt.insert(2, 0)
bt.insert(10, 0)
#bt.insert(8, 6)
# Ta delete asta me auth th seira kai apla
# kane comment kai uncomment auta pou thes
# Mexri na vroume akrh me ta pointers asta 0 ola
#bt.delete(5, 0)
#bt.delete(12, 0)
#bt.delete(7, 0)
bt.delete(3, 0)
#bt.delete(2, 0)
bt.delete(10, 0)
bt.insert(13, 0)
bt.delete(12, 0)
bt.insert(12, 0)
bt.insert(14, 0)
bt.insert(15, 0)
bt.insert(16, 0)
bt.delete(15, 0)
bt.delete(7, 0)


bt.plot()