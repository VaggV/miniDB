from btree import Btree
from random import randrange
import random

'''
Test the Btree
'''

NUM = 60
B = 6
lst = []

print(f"Branching factor: {B}")

insertcounter = 0
while len(lst)!=NUM:
    new_v = randrange(100)
    if new_v not in lst:
        lst.append(new_v)
        insertcounter += 1

print(f"Inserted {insertcounter} items")

bt = Btree(B)

for ind, el in enumerate(lst):
    bt.insert(el, ind)


delcounter = 0
listLength = len(lst)
for i in range(len(lst)):
    delvalue = random.choice(lst)
    lst.remove(delvalue)
    bt.delete(delvalue)
    # if counter >= listLength/2:
    #     break
    delcounter += 1

print(f"Deleted {delcounter} items")

bt.plot()
