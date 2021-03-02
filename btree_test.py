from btree import Btree
from random import randrange
import random

'''
Test the Btree
'''

NUM = 500
B = 7
lst = []

while len(lst)!=NUM:
    new_v = randrange(100)
    if new_v not in lst:
        lst.append(new_v)

bt = Btree(B)

for ind, el in enumerate(lst):
    bt.insert(el, ind)

print(f"List: {lst}")

counter = 0
listLength = len(lst)
for i in range(len(lst)):
    delvalue = random.choice(lst)
    lst.remove(delvalue)
    bt.delete(delvalue)
    # if counter >= listLength/2:
    #     break
    counter += 1


print(f"deleted list: {lst}")
bt.plot()
