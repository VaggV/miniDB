from btree import Btree

bt = Btree(3)

# dentro 1

# bt.insert(5,0)
# bt.insert(12, 1)
# bt.insert(7, 2)
# bt.insert(3, 3)
# bt.insert(2, 4)
# bt.insert(10, 5)
#
# bt.delete(10)
#
# bt.insert(8,6)
# bt.insert(0,7)
# bt.insert(1,8)
# bt.insert(6,9)
# bt.insert(13,10)
# bt.insert(11,11)
# bt.delete(12)
# bt.delete(0)
# bt.delete(8)
# bt.insert(8,12)
# bt.delete(11)
# bt.insert(14, 13)
# bt.delete(8)
# bt.delete(3)

# dentro 2

bt.insert(10)
bt.insert(20)
bt.insert(30)
bt.insert(40)
bt.insert(50)
bt.insert(60)
bt.insert(70)
bt.insert(80)
bt.insert(90)
bt.insert(100)
bt.insert(110)
bt.insert(120)

bt.delete(110)
bt.insert(101)
bt.delete(90)

bt.insert(121)
bt.delete(101)

bt.insert(125)
bt.delete(121)
bt.insert(122)
bt.delete(100)

bt.insert(85)
bt.delete(70)
bt.insert(55)
bt.delete(60)

bt.insert(60)
bt.delete(50)

bt.insert(45)

bt.delete(55)
#bt.delete(120)

#auta ta 2 delete theloun douleia



# dentro 3
#
# for i in range(15):
#     bt.insert(i*10)
# for i in range(10):
#     bt.insert(i*10+1)
#
# bt.delete(51)
# bt.delete(40)
# bt.delete(80)

bt.plot()