"""
https://en.wikipedia.org/wiki/B%2B_tree
"""

import math

class Node:
    """
    Node abstraction. Represents a single bucket
    """

    def __init__(self, b, values=None, ptrs=None,
                 left_sibling=None, right_sibling=None, parent=None, is_leaf=False):
        if ptrs is None:
            ptrs = []
        if values is None:
            values = []
        self.b = b  # branching factor
        self.values = values  # Values (the data from the pk column)
        self.ptrs = ptrs  # ptrs (the indexes of each datapoint or the index of another bucket)
        self.left_sibling = left_sibling  # the index of a buckets left sibling
        self.right_sibling = right_sibling  # the index of a buckets right sibling
        self.parent = parent  # the index of a buckets parent
        self.is_leaf = is_leaf  # a boolean value signaling whether the node is a leaf or not

    def find(self, value, return_ops=False):
        """
        Returns the index of the next node to search for a value if the node is not a leaf (a ptrs of the available ones).
        If it is a leaf (we have found the appropriate node), it returns nothing.

        value: the value that we are searching for
        return_ops: set to True if you want to use the number of operations (for benchmarking)
        """
        ops = 0  # number of operations (<>= etc). Used for benchmarking
        if self.is_leaf:  #
            return

        # for each value in the node, if the user supplied value is smaller, return the btrees value index
        # else (no value in the node is larger) return the last ptr
        for index, existing_val in enumerate(self.values):
            ops += 1
            if value < existing_val:
                if return_ops:
                    return self.ptrs[index], ops
                else:
                    return self.ptrs[index]

        if return_ops:
            return self.ptrs[-1], ops
        else:
            return self.ptrs[-1]

    def insert(self, value, ptr, ptr1=None):
        """
        Insert the value and its ptr/s to the appropriate place (node wise).
        User can input two ptrs to insert to a non leaf node.

        value: the value that we are inserting to the node
        ptr: the ptr of the inserted value (its index for example)
        ptr1: the 2nd ptr (in case the user wants to insert into a nonleaf node for ex)

        """
        # for each value in the node, if the user supplied value is smaller, insert the value and its ptr into that position
        # if a second ptr is provided, insert it right next to the 1st ptr
        # else (no value in the node is larger) append value and ptr/s to the back of the list.

        for index, existing_val in enumerate(self.values):
            if value < existing_val:

                self.values.insert(index, value)
                if ptr is not None:
                    self.ptrs.insert(index + 1, ptr)

                if ptr1:
                    self.ptrs.insert(index + 1, ptr1)
                return
        self.values.append(value)
        if ptr is not None:
            self.ptrs.append(ptr)
        if ptr1:
            self.ptrs.append(ptr1)

    def show(self):
        """
        print the node's value and important info
        """
        print('Values', self.values)
        print('ptrs', self.ptrs)
        print('Parent', self.parent)
        print('LS', self.left_sibling)
        print('RS', self.right_sibling)

    def delete(self, value, ptr):
        # for index, existing_val in enumerate(self.values):
        #     if value == existing_val:
        #         self.values.pop(index)
        #         self.ptrs.pop(index+1)
        # print("Node Class delete Method:")
        # print(f"value: {value}, ptr: {ptr}, ptrs: {self.ptrs}")
        for index, existing_val in enumerate(self.values):
            if value == existing_val:
                self.values.pop(index)

                if self.is_leaf:
                    self.ptrs.pop(index)
                break
        #print(f"value: {value} deleted successfully")


class Btree:
    def __init__(self, b):
        """
        The tree abstraction.
        """
        self.b = b  # branching factor
        self.nodes = []  # list of nodes. Every new node is appended here
        self.root = None  # the index of the root node

        self.min_child_count = math.ceil(b / 2) # if b = 3 -> then min_child is 2
        self.min_leaf_count = math.ceil(b/2) - 1  # if b = 3 -> then min_leaf_count is 1
        self.insert_count = 0 # used to automatically add pointers to values on insert NA TO VGALOUME PRIN STILOUME TIN ERGASIA

    def insert(self, value, rptr=None):
        """
        Insert the value and its ptr/s to the appropriate node (node-level insertion is covered by the node object).
        User can input two ptrs to insert to a non leaf node.
        """
        ptr = self.insert_count
        self.insert_count += 1
        # if the tree is empty, add the first node and set the root index to 0 (the only node's index)
        if self.root is None:
            self.nodes.append(Node(self.b, is_leaf=True))
            self.root = 0

        # find the index of the node that the value and its ptr/s should be inserted to (_search)
        index = self._search(value)
        # insert to it
        self.nodes[index].insert(value, ptr)
        # if the node has more elements than b-1, split the node
        if len(self.nodes[index].values) == self.b:
            self.split(index)

    # def delete2(self, value):
    #     if self.root is None:
    #         print('Tree is empty')
    #         return
    #
    #     # find the index of the node that the value and its ptr/s should be inserted to (_search)
    #     index = self._search(value)
    #
    #     index_in_node = self.nodes[index].values.index(value)
    #     pointerr = self.nodes[index].ptrs[index_in_node]
    #     # print ("**************************************")
    #     # print(f"Value: {value}, pointer: {pointerr} ")
    #     # print(f"Node values: {self.nodes[index].values}, Node pointers: {self.nodes[index].ptrs}")
    #     # print ("**************************************")
    #     is_internal = False
    #     check_node = self.nodes[index]
    #     while check_node.parent is not None:
    #         check_node = self.nodes[check_node.parent]
    #         if value in check_node.values:
    #             is_internal = True
    #             break
    #
    #     # delete it
    #     self.nodes[index].delete(value, pointerr)
    #
    #     parent_node = None
    #     right_sib = None
    #     left_sib = None
    #
    #     if len(self.nodes[index].values) < self.min_leaf_count:
    #         # If the values are below the minimum leaf count then ...
    #         if not is_internal:
    #             if self.nodes[index].left_sibling is None:
    #                 # if there is no left sibling it means its the leftest node
    #
    #                 borrowed_value = self.nodes[self.nodes[index].right_sibling].values[0]
    #                 borrowed_ptr = self.nodes[self.nodes[index].right_sibling].ptrs[0]
    #                 if len(self.nodes[self.nodes[index].right_sibling].values) > self.min_leaf_count:
    #                     # if there is enough values in the right sibling then borrow
    #
    #                     self.nodes[index].insert(borrowed_value, borrowed_ptr)
    #                     self.nodes[self.nodes[index].right_sibling].delete(borrowed_value, borrowed_ptr)
    #
    #                     for i in range(len(self.nodes[self.nodes[index].parent].values)):
    #                         if self.nodes[self.nodes[index].parent].values[i] == borrowed_value:
    #                             self.nodes[self.nodes[index].parent].delete(self.nodes[self.nodes[index].parent].values[i], self.nodes[self.nodes[index].parent].ptrs[i])
    #                             self.nodes[self.nodes[index].parent].insert(self.nodes[self.nodes[index].right_sibling].values[0], None)
    #                             break
    #                 else:
    #                     # else there is not enough values in the right sibling and it has to merge
    #
    #                     pass
    #
    #         elif is_internal:
    #             # else if the node is present in internal nodes
    #
    #             left_sib = self.nodes[self.nodes[index].left_sibling]
    #             right_sib = self.nodes[self.nodes[index].right_sibling]
    #             if len(left_sib.values) > self.min_leaf_count and self.nodes[left_sib.parent] == self.nodes[self.nodes[index].parent]:
    #                 # if the left node has enough values and is an immediate sibling
    #
    #                 self.nodes[index].insert(left_sib.values[-1], left_sib.ptrs[-1])
    #                 left_sib.delete(left_sib.values[-1], left_sib.ptrs[-1])
    #
    #                 check_node.delete(check_node.values[0], check_node.ptrs[0])
    #                 check_node.insert(self.nodes[index].values[0], None)
    #
    #             elif len(right_sib.values) > self.min_leaf_count and self.nodes[right_sib.parent] == self.nodes[self.nodes[index].parent]:
    #                 # else if the right node has enough values and is an immediate sibling
    #
    #                 borrowed_value = right_sib.values[0]
    #                 borrowed_ptr = right_sib.ptrs[0]
    #                 self.nodes[index].insert(borrowed_value, borrowed_ptr)
    #
    #                 new_index = check_node.values.index(value)
    #                 popped = right_sib.values[0]
    #                 right_sib.delete(right_sib.values[0], right_sib.ptrs[0])
    #                 popped_parent = self.nodes[self.nodes[index].parent].values.index(popped)
    #
    #                 check_node.delete(check_node.values[new_index], check_node.ptrs[new_index])
    #                 check_node.insert(self.nodes[index].values[0], None)
    #
    #                 prntnode = self.nodes[self.nodes[index].parent]
    #                 prntnode.delete(prntnode.values[popped_parent], prntnode.ptrs[popped_parent])
    #                 prntnode.insert(right_sib.values[0], None)
    #
    #             elif self.nodes[right_sib.parent] == self.nodes[self.nodes[index].parent]:
    #                 # else if the right sibling values is equal to the minimum leaf count
    #                 # it means the self.node cant borrow and it has to merge
    #                 parent_node = self.nodes[self.nodes[index].parent]
    #                 grandparent_node = self.nodes[parent_node.parent]
    #                 print(f"Grandparent_node pointers: {grandparent_node.ptrs} ")
    #                 print(f"Deleted value: {value}")
    #                 if len(parent_node.ptrs) == self.min_child_count:
    #                     # = self.nodes[right_sib.parent]
    #                     print(f"Deleted value: {value}")
    #
    #                     grandpindex = grandparent_node.ptrs.index(self.nodes[index].parent) + 1
    #                     right_sibling_parent = self.nodes[self.nodes[parent_node.parent].ptrs[grandpindex]]
    #                     print(f"right_sibling_parent values: {right_sibling_parent.values}")
    #                     print(f"right sibling index: {grandpindex}")
    #                     print(f"right sibling parent pointers: {right_sibling_parent.ptrs}")
    #                     if len(right_sibling_parent.ptrs) >= self.min_child_count:
    #                         grandparent_node.values.remove(self.nodes[right_sibling_parent.ptrs[0]].values[0])
    #
    #                         right_sibling_parent.values.insert(0,self.nodes[right_sibling_parent.ptrs[0]].values[0])
    #                         right_sibling_parent.ptrs.insert(0, self.nodes[index].right_sibling)
    #
    #                         grandparent_node.ptrs.remove(self.nodes.index(parent_node))
    #                         parent_node = None
    #                         check_node.values[0] = self.nodes[self.nodes[index].right_sibling].values[0]
    #                 else:
    #                     print(f"Check node values: {check_node.values}")
    #                     print(f"right sibling values[0]: {self.nodes[self.nodes[index].right_sibling].values[0]}")
    #                     self.replace_item(check_node.values, value, self.nodes[self.nodes[index].right_sibling].values[0])
    #                     parent_node.values.remove(self.nodes[self.nodes[index].right_sibling].values[0])
    #                 self.nodes[index] = None
    #                 pass
    #     else:
    #         parentnode = self.nodes[self.nodes[index].parent]
    #         for i in range(len(parentnode.values)):
    #             if value == parentnode.values[i]:
    #                 parentnode.delete(parentnode.values[i], parentnode.ptrs[i])
    #                 parentnode.insert(self.nodes[index].values[0], None)
    #                 break
    #         node = self.nodes[index]
    #         while node.parent is not None:
    #             # loop through the parents to check if the deleted value is
    #             # in an internal node
    #             node = self.nodes[node.parent]
    #             if value in node.values:
    #                 for i in range(len(node.values)):
    #                     if value == node.values[i]:
    #                         node.delete(node.values[i], node.ptrs[i])
    #                         node.insert(self.nodes[index].values[0], None)
    #                         break
    #                 break

    def replace_item(self, the_list, value, new_value):
        for index, item in enumerate(the_list):
            if value == the_list[index]:
                print(f"NEW VALUE: {new_value}")
                the_list[index] = new_value
                return
        return

    def _search(self, value, return_ops=False, delete=False):
        """
        Returns the index of the node that the given value exists or should exist in.

        value: the value that we are searching for
        return_ops: set to True if you want to use the number of operations (for benchmarking)
        """
        ops = 0  # number of operations (<>= etc). Used for benchmarking

        # start with the root node
        node = self.nodes[self.root]
        # while the node that we are searching in is not a leaf
        # keep searching
        while not node.is_leaf:
            idx, ops1 = node.find(value, return_ops=True)
            node = self.nodes[idx]
            ops += ops1

        index = self.nodes.index(node)
        # finally return the index of the appropriate node (and the ops if you want to)
        if return_ops:
            return index, ops
        else:
            return index

    def delete(self, value):
        if self.root is None:
            print('Tree is empty')
            return

        # 1. Find the entry to be deleted
        index = self._search(value)
        if value not in self.nodes[index].values:
            print(f"Value [{value}] not found in the tree.")
            return

        thisNode = self.nodes[index]

        is_internal = False
        internalNode = self.nodes[index]
        while internalNode.parent is not None:
            internalNode = self.nodes[internalNode.parent]
            if value in internalNode.values:
                is_internal = True
                break

        index_in_node = self.nodes[index].values.index(value)
        ptr = self.nodes[index].ptrs[index_in_node]

        # 2. Delete entry from leaf.
        thisNode.delete(value, ptr)


        rSibling = None
        lSibling = None
        if thisNode.right_sibling is not None:
            rSibling = self.nodes[thisNode.right_sibling]
        if thisNode.left_sibling is not None:
            lSibling = self.nodes[thisNode.left_sibling]

        # If right sibling and left siblings are childs of the same parent
        # then save them in different variables
        rParSibling = None
        lParSibling = None
        if rSibling is not None and rSibling.parent == thisNode.parent:
            rParSibling = rSibling
        if lSibling is not None and lSibling.parent == thisNode.parent:
            lParSibling = lSibling

        #print(f"delvalue: {value} , right sibling values = {rSibling.values}")


        # 2. If this leaf is left with less than the required amount of values then:
        if len(thisNode.values) < self.min_leaf_count:
            # 3. if both siblings exist
            if lParSibling is not None and rParSibling is not None:
                # 3. if both siblings have minimum amount of values
                if len(lParSibling.values) <= self.min_leaf_count and len(rParSibling.values) <= self.min_leaf_count:
                    # 3. merge with lParSibling
                    self.merge(index, thisNode, lSibling, value, 'left')
                    self.redistribute(index, thisNode, value, 'left', lSibling, thisNode.parent)
                # 3. else 1 of the siblings has enough values, then
                else:
                    # if the left sibling has enough values
                    if len(lParSibling.values) > self.min_leaf_count:
                        # 3. borrow from lParSibling
                        self.borrow(thisNode, lSibling, 'left', value, internalNode)
                    # else if the right sibling has enough values
                    elif len(rParSibling.values) > self.min_leaf_count:
                        # 3. borrow from rParSibling
                        # if the value is also in an internal node (is_internal = True)
                        if is_internal:
                            # pass the internal node so the value in the internal node can be changed
                            self.borrow(thisNode, rSibling, 'right', value, internalNode)
                        else:
                            # else the value might only be in the parent node
                            self.borrow(thisNode, rSibling, 'right', value)
            elif rParSibling is not None:
                if len(rParSibling.values) <= self.min_leaf_count:
                    # 3. merge with rParSibling node
                    if is_internal:
                        self.merge(index, thisNode, rSibling, value, 'right', internalNode)
                    else:
                        self.merge(index, thisNode, rSibling, value, 'right')
                    self.redistribute(index, thisNode, value, 'right', rSibling, thisNode.parent)
                else:
                    # 3. borrow (from rParSibling)
                    if is_internal:
                        print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                        print(f"delvalue: {value} , right sibling values = {rSibling.values}")
                        self.borrow(thisNode, rSibling, 'right', value, internalNode)
                    else:
                        self.borrow(thisNode, rSibling, 'right', value)
            elif lParSibling is not None:
                if len(lParSibling.values) <= self.min_leaf_count:
                    # 3. merge with lParSibling node
                    #print(f"rightSibling values: {rSibling.values}")
                    #print(f"rightParSibling values: {rParSibling.values}")
                    self.merge(index, thisNode, lSibling, value, 'left')
                    self.redistribute(index, thisNode, value, 'left', lSibling, thisNode.parent)
                else:
                    # 3. borrow (from lParSibling)
                    self.borrow(thisNode, lSibling, 'left', value, internalNode)
            # else there is no siblings with the same parent
            else:
                values = 0
                lastNode = None
                for i, node in enumerate(self.nodes):
                    if node is not None:
                        lastNode = node
                        for j, val in enumerate(node.values):
                            values += 1
                print(f"VALUES : {values}")
                if values == 0:
                    self.nodes[index] = None
                    self.nodes = []
                    self.root = None
        # else it has enough values and the value can simply be deleted
        # but we have to delete it from the internal node (in case it's internal)
        else:
            if is_internal:
                for i, value1 in enumerate(internalNode.values):
                    if value1 == value:
                        internalNode.values[i] = thisNode.values[0]





            #print(f"index: {index}, self.root: {self.root}")
            # if index == self.root:
            #     print("Yes")
            #     print(f"length of this node: {len(thisNode.values)}")
            #     if len(thisNode.values) == 0:
            #         self.nodes[self.root] = None
            #         self.root = None

        # print("#######################################")
        # print("#######################################")
        # print("#######################################")
        # print(f"Deleted value: {value}")
        # print(f"thisNode index: {index}")
        # print(f"right sibling index: {thisNode.right_sibling}")
        # print(f"left sibling index: {thisNode.left_sibling}")
        # if thisNode.right_sibling is not None:
        #     print(f"{self.nodes[thisNode.left_sibling].values} {thisNode.values} {self.nodes[thisNode.right_sibling].values}")
        # else:
        #     print(f"{self.nodes[thisNode.left_sibling].values} {thisNode.values}")
        # print("########################################")
        # print("########################################")
        # print("########################################")


    def merge(self, thisNodeIndex, thisNode, siblingNode, deletedValue, siblingRorL, internalNode=None):
        this_Node = self.nodes[thisNodeIndex]

        #if siblingNode in self.nodes:
        index_sibling_node = self.nodes.index(siblingNode)

        parentNode = self.nodes[thisNode.parent]
        if deletedValue in parentNode.values:
            parentNode.values.remove(deletedValue)
        else:
            if siblingRorL == 'left':
                parentNode.values.remove(thisNode.values[0])
            elif siblingRorL == 'right':
                parentNode.values.remove(siblingNode.values[0])

        if siblingRorL == 'left':
            thisNode.left_sibling = siblingNode.left_sibling
            if siblingNode.left_sibling is not None:
                self.nodes[siblingNode.left_sibling].right_sibling = thisNodeIndex
            # else:
            #     self.nodes[siblingNode.left_sibling].right_sibling = None
        elif siblingRorL == 'right':
            thisNode.right_sibling = siblingNode.right_sibling
            if siblingNode.right_sibling is not None:
                self.nodes[siblingNode.right_sibling].left_sibling = thisNodeIndex
            # else:
            #     self.nodes[siblingNode.right_sibling].left_sibling = None

        if internalNode is not None:
            for i, value in enumerate(internalNode.values):
                if value == deletedValue:
                    internalNode.values[i] = thisNode.values[0]
                    break

        for i, value in enumerate(siblingNode.values):
            thisNode.insert(siblingNode.values[i], siblingNode.ptrs[i])

        parentNode.ptrs.remove(index_sibling_node)
        self.nodes[index_sibling_node] = None


        # dokimasa na ftiaksw neo node anti na kanoume insert sto allo alla prepei na eixe ena mikro lathos kai to kana comment

        # mergedValues = thisNode.values
        # mergedPtrs = thisNode.ptrs
        # newLeftSib = None
        # newRightSib = None
        # if siblingRorL == 'left':
        #     newLeftSib = siblingNode.left_sibling
        #     newRightSib = thisNode.right_sibling
        # elif siblingRorL == 'right':
        #     newLeftSib = siblingNode.right_sibling
        #     newRightSib = thisNode.left_sibling
        # mergedNode = Node(self.b, mergedValues, mergedPtrs, newLeftSib, newRightSib, thisNode.parent, True)
        # self.nodes[index_sibling_node] = None
        # self.nodes[thisNodeIndex] = mergedNode

    def borrow(self, thisNode, siblingNode, siblingRorL, deletedValue, internalNode=None):
        parentNode = self.nodes[thisNode.parent]
        if siblingRorL == 'right':
            borrowed_value = siblingNode.values[0]
            borrowed_ptr = siblingNode.ptrs[0]
            thisNode.insert(borrowed_value, borrowed_ptr)
            siblingNode.delete(borrowed_value, borrowed_ptr)
            for i, value in enumerate(parentNode.values):
                if value == borrowed_value:
                    parentNode.values[i] = siblingNode.values[0]
                    break
            if internalNode is not None:
                for i, value in enumerate(internalNode.values):
                    if value == deletedValue:
                        internalNode.values[i] = thisNode.values[0]
                        break
        elif siblingRorL == 'left':
            borrowed_value = siblingNode.values[-1]
            borrowed_ptr = siblingNode.ptrs[-1]
            thisNode.insert(borrowed_value, borrowed_ptr)
            siblingNode.delete(borrowed_value, borrowed_ptr)
            if deletedValue in parentNode.values:
                for i, value in enumerate(parentNode.values):
                    if value == deletedValue:
                        parentNode.values[i] = thisNode.values[0]
                        break
            else:
                for i, value in enumerate(parentNode.values):
                    if value == thisNode.values[1]:
                        parentNode.values[i] = thisNode.values[0]
                        break



    def redistribute(self, thisNodeIndex, thisNode, deletedValue, siblingRorL, siblingNode, parentIndex):
        parentNode = self.nodes[parentIndex]
        if parentIndex == self.root:
            if len(self.nodes[self.root].values) == 0:
                # thisNode.is_leaf = False
                self.nodes[self.root] = None
                self.root = thisNodeIndex
                self.nodes[self.root].parent = None
                return

        if len(parentNode.values) <= self.min_leaf_count:
            # go to 5
            pass
        else:
            return

    def split(self, node_id):
        """
        Split the node with index=node_id
        """
        # fetch the node to be split
        node = self.nodes[node_id]
        # the value that will be propagated to the parent is the middle one.
        new_parent_value = node.values[len(node.values) // 2]
        if node.is_leaf:
            # if the node is a leaf, the parent value should be a part of the new node (right)
            # Important: in a b+tree, every value should appear in a leaf
            right_values = node.values[len(node.values) // 2:]
            right_ptrs = node.ptrs[len(node.ptrs) // 2:]

            # create the new node with the right half of the old nodes values and ptrs (including the middle ones)
            right = Node(self.b, right_values, right_ptrs,
                         left_sibling=node_id, right_sibling=node.right_sibling, parent=node.parent,
                         is_leaf=node.is_leaf)
            # since the new node (right) will be the next one to be appended to the nodes list
            # its index will be equal to the length of the nodes list.
            # Thus we set the old nodes (now left) right sibling to the right nodes future index (len of nodes)
            if node.right_sibling is not None:
                self.nodes[node.right_sibling].left_sibling = len(self.nodes)
            node.right_sibling = len(self.nodes)

        else:
            # if the node is not a leaf, the parent value shoudl NOT be part of the new node
            right_values = node.values[len(node.values) // 2 + 1:]
            if self.b % 2 == 1:
                right_ptrs = node.ptrs[len(node.ptrs) // 2:]
            else:
                right_ptrs = node.ptrs[len(node.ptrs) // 2 + 1:]

            # if non leafs should be connected change the following two lines and add siblings
            right = Node(self.b, right_values, right_ptrs,
                         parent=node.parent, is_leaf=node.is_leaf)
            # make sure that a non leaf node doesnt have a parent
            node.right_sibling = None
            # the right node's kids should have him as a parent (if not all nodes will have left as parent)
            for ptr in right_ptrs:
                self.nodes[ptr].parent = len(self.nodes)

        # old node (left) keeps only the first half of the values/ptrs
        node.values = node.values[:len(node.values) // 2]
        if self.b % 2 == 1:
            node.ptrs = node.ptrs[:len(node.ptrs) // 2]
        else:
            node.ptrs = node.ptrs[:len(node.ptrs) // 2 + 1]

        # append the new node (right) to the nodes list
        self.nodes.append(right)

        # If the new nodes have no parents (a new level needs to be added
        if node.parent is None:
            # its the root that is split
            # new root contains the parent value and ptrs to the two recently split nodes
            parent = Node(self.b, [new_parent_value], [node_id, len(self.nodes) - 1]
                          , parent=node.parent, is_leaf=False)

            # set root, and parent of split celss to the index of the new root node (len of nodes-1)
            self.nodes.append(parent)
            self.root = len(self.nodes) - 1
            node.parent = len(self.nodes) - 1
            right.parent = len(self.nodes) - 1
        else:
            # insert the parent value to the parent

            self.nodes[node.parent].insert(new_parent_value, len(self.nodes) - 1)
            # check whether the parent needs to be split
            if len(self.nodes[node.parent].values) == self.b:
                self.split(node.parent)

    def show(self):
        """
        Show important info for each node (sort the by level - root first, then left to right)
        """
        nds = [self.root]
        for ptr in nds:
            if self.nodes[ptr].is_leaf:
                continue
            nds.extend(self.nodes[ptr].ptrs)

        for ptr in nds:
            print(f'## {ptr} ##')
            self.nodes[ptr].show()
            print('----')

    def plot(self):
        #Test
        # print("################## LEAFS ####################")
        # for i in range(len(self.nodes)):
        #     if self.nodes[i] is not None:
        #         if self.nodes[i].is_leaf:
        #             print(f"[{i}] -- Pointers: {self.nodes[i].ptrs}, Values: {self.nodes[i].values}")
        # print("#############################################")
        # for i in range(len(self.nodes)):
        #     if self.nodes[i] is not None:
        #         if self.nodes[i].is_leaf:
        #             print(f"{self.nodes[i].left_sibling} + {i} + {self.nodes[i].right_sibling}")
        # print("\n################ NON-LEAFS ##################")
        # for i in range(len(self.nodes)):
        #     if self.nodes[i] is not None:
        #         if not self.nodes[i].is_leaf:
        #             print(f"[{i}] -- Pointers: {self.nodes[i].ptrs}, Values: {self.nodes[i].values}")
        # #print(f"Index 18 node values: {self.nodes[18].values}")
        # #print(f"Index 11 node values: {self.nodes[11].values}")
        # print("#############################################")


        # print(f"Root: {self.nodes[self.root].values}")
        # print(f"Nodes length: {len(self.nodes)}")


        if not self.nodes:
            print("Cannot plot tree, it is empty")
            return

        # arrange the nodes top to bottom left to right
        nds = [self.root]
        for ptr in nds:
            if self.nodes[ptr] is not None: # <-------------------
                if self.nodes[ptr].is_leaf:
                    continue
                nds.extend(self.nodes[ptr].ptrs)

        # add each node and each link
        g = 'digraph G{\nforcelabels=true;\n'

        for i in nds:
            if self.nodes[i] is not None:
                node = self.nodes[i]
                g += f'{i} [label="{node.values}"]\n'
                if node.is_leaf:
                    continue
                    # if node.left_sibling is not None:
                    #     g+=f'"{node.values}"->"{self.nodes[node.left_sibling].values}" [color="blue" constraint=false];\n'
                    # if node.right_sibling is not None:
                    #     g+=f'"{node.values}"->"{self.nodes[node.right_sibling].values}" [color="green" constraint=false];\n'
                    #
                    # g+=f'"{node.values}"->"{self.nodes[node.parent].values}" [color="red" constraint=false];\n'
                else:
                    for child in node.ptrs:
                        if self.nodes[child] is not None:
                            g += f'{child} [label="{self.nodes[child].values}"]\n'
                            g += f'{i}->{child};\n'
        g += "}"

        try:
            from graphviz import Source
            src = Source(g)
            src.render('bplustree', view=True)
        except ImportError:
            print('"graphviz" package not found. Writing to graph.gv.')
            with open('graph.gv', 'w') as f:
                f.write(g)

    def find(self, operator, value):
        """
        Return ptrs of elements where btree_value"operator"value.
        Important, the user supplied "value" is the right value of the operation. That is why the operation are reversed below.
        The left value of the op is the btree value.
        """
        results = []
        # find the index of the node that the element should exist in
        leaf_idx, ops = self._search(value, True)
        target_node = self.nodes[leaf_idx]

        if operator == '==':
            # if the element exist, append to list, else pass and return
            # noinspection PyBroadException
            try:
                results.append(target_node.ptrs[target_node.values.index(value)])
                # print('Found')
            except:
                # print('Not found')
                pass

        # for all other ops, the code is the same, only the operations themselves and the sibling indexes change
        # for > and >= (btree value is >/>= of user supplied value), we return all the right siblings (all values are larger than current cell)
        # for < and <= (btree value is </<= of user supplied value), we return all the left siblings (all values are smaller than current cell)

        if operator == '>':
            for idx, node_value in enumerate(target_node.values):
                ops += 1
                if node_value > value:
                    results.append(target_node.ptrs[idx])
            while target_node.right_sibling is not None:
                target_node = self.nodes[target_node.right_sibling]
                results.extend(target_node.ptrs)

        if operator == '>=':
            for idx, node_value in enumerate(target_node.values):
                ops += 1
                if node_value >= value:
                    results.append(target_node.ptrs[idx])
            while target_node.right_sibling is not None:
                target_node = self.nodes[target_node.right_sibling]
                results.extend(target_node.ptrs)

        if operator == '<':
            for idx, node_value in enumerate(target_node.values):
                ops += 1
                if node_value < value:
                    results.append(target_node.ptrs[idx])
            while target_node.left_sibling is not None:
                target_node = self.nodes[target_node.left_sibling]
                results.extend(target_node.ptrs)

        if operator == '<=':
            for idx, node_value in enumerate(target_node.values):
                ops += 1
                if node_value <= value:
                    results.append(target_node.ptrs[idx])
            while target_node.left_sibling is not None:
                target_node = self.nodes[target_node.left_sibling]
                results.extend(target_node.ptrs)

        # print the number of operations (usefull for benchamrking)
        print(f'With BTree -> {ops} comparison operations')
        return results