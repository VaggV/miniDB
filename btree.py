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

        self.min_child_count = math.ceil(b / 2)
        self.min_leaf_count = math.ceil(b/2) - 1


    def insert(self, value, ptr, rptr=None):
        """
        Insert the value and its ptr/s to the appropriate node (node-level insertion is covered by the node object).
        User can input two ptrs to insert to a non leaf node.
        """
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

    def replace_item(self, the_list, value, new_value):
        """
        Replaces the value in the_list given with the new_value
        """
        for index, item in enumerate(the_list):
            if value == the_list[index]:
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

    # noinspection PyUnresolvedReferences
    def delete(self, value):
        """
        Delete the value from the B+tree
        """
        if self.root is None:
            print('Tree is empty')
            return

        # Find the entry to be deleted
        index = self._search(value)
        if value not in self.nodes[index].values:
            print(f"Value [{value}] not found in the tree.")
            return

        thisNode = self.nodes[index]

        internalNode = self.checkifinternal(index, value)

        # Find the value's index in the node so we can get the ptr and delete it
        index_in_node = self.nodes[index].values.index(value)
        ptr = self.nodes[index].ptrs[index_in_node]

        rSibling = None
        lSibling = None
        if thisNode.right_sibling is not None:
            rSibling = self.nodes[thisNode.right_sibling]
        if thisNode.left_sibling is not None:
            lSibling = self.nodes[thisNode.left_sibling]

        # If right sibling and left siblings are children of the same parent
        # then save them in different variables
        rParSibling = None
        lParSibling = None
        if rSibling is not None and rSibling.parent == thisNode.parent:
            rParSibling = rSibling
        if lSibling is not None and lSibling.parent == thisNode.parent:
            lParSibling = lSibling

        # Delete entry from leaf.
        thisNode.delete(value, ptr)

        # If this leaf is left with less than the required amount of values then:
        if len(thisNode.values) < self.min_leaf_count:
            # if both siblings exist
            if lParSibling is not None and rParSibling is not None:
                # if both siblings have minimum amount of values
                if len(lParSibling.values) <= self.min_leaf_count and len(rParSibling.values) <= self.min_leaf_count:
                    # merge with lParSibling
                    self.merge(index, thisNode, lSibling, value, 'left')
                    if internalNode is not None:
                        self.redistribute(index, thisNode, value, 'left', lSibling, thisNode.parent, internalNode=internalNode)
                    else:
                        self.redistribute(index, thisNode, value, 'left', lSibling, thisNode.parent)
                # else 1 of the siblings has enough values, then
                else:
                    # if the left sibling has enough values
                    if len(lParSibling.values) > self.min_leaf_count:
                        # borrow from lParSibling
                        self.borrow(thisNode, lSibling, 'left', value, internalNode)
                    # else if the right sibling has enough values
                    elif len(rParSibling.values) > self.min_leaf_count:
                        # borrow from rParSibling
                        # if the value is also in an internal node (is_internal = True)
                        if internalNode is not None:
                            # pass the internal node so the value in the internal node can be changed
                            self.borrow(thisNode, rSibling, 'right', value, internalNode)
                        else:
                            # else the value might only be in the parent node
                            self.borrow(thisNode, rSibling, 'right', value)
            elif rParSibling is not None:
                if len(rParSibling.values) <= self.min_leaf_count:
                    # merge with rParSibling node
                    if internalNode is not None:
                        self.merge(index, thisNode, rSibling, value, 'right', internalNode)
                        self.redistribute(index, thisNode, value, 'right', rSibling, thisNode.parent,internalNode=internalNode)
                    else:
                        self.merge(index, thisNode, rSibling, value, 'right')
                        self.redistribute(index, thisNode, value, 'right', rSibling, thisNode.parent)
                else:
                    # borrow (from rParSibling)
                    if internalNode is not None:
                        self.borrow(thisNode, rSibling, 'right', value, internalNode)
                    else:
                        self.borrow(thisNode, rSibling, 'right', value)
            elif lParSibling is not None:
                if len(lParSibling.values) <= self.min_leaf_count:
                    # merge with lParSibling node
                    self.merge(index, thisNode, lSibling, value, 'left')
                    if internalNode is not None:
                        self.redistribute(index, thisNode, value, 'left', lSibling, thisNode.parent, internalNode=internalNode)
                    else:
                        self.redistribute(index, thisNode, value, 'left', lSibling, thisNode.parent)
                else:
                    # borrow (from lParSibling)
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
                if values == 0:
                    self.nodes[index] = None
                    self.nodes = []
                    self.root = None
        # else it has enough values and the value can simply be deleted
        # but we have to delete it from the internal node (in case it's internal)
        else:
            if internalNode is not None:
                for i, value1 in enumerate(internalNode.values):
                    if value1 == value:
                        internalNode.values[i] = thisNode.values[0]

    def merge(self, thisNodeIndex, thisNode, siblingNode=None, deletedValue=None, siblingRorL=None, internalNode=None, mergeInternalNodes=False, parentNode=None, parentNodeIndex=None, parentOfParent=None):
        """
        if mergeInternalNodes is False then it merges the leaf nodes
        if mergeInternalNodes is True then it merges the internal nodes
        """

        # if we dont have to merge internal nodes
        if not mergeInternalNodes:
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
            elif siblingRorL == 'right':
                thisNode.right_sibling = siblingNode.right_sibling
                if siblingNode.right_sibling is not None:
                    self.nodes[siblingNode.right_sibling].left_sibling = thisNodeIndex

            for i, value in enumerate(siblingNode.values):
                thisNode.insert(siblingNode.values[i], siblingNode.ptrs[i])

            if internalNode is not None:
                for i, value in enumerate(internalNode.values):
                    if value == deletedValue:
                        internalNode.values[i] = thisNode.values[0]
                        break

            parentNode.ptrs.remove(index_sibling_node)
            self.nodes[index_sibling_node] = None
        # else we have to merge internal nodes
        else:
            if parentOfParent is None:
                pass
            else:
                if len(parentNode.ptrs) < self.min_child_count:
                    parentPtrsIndex = parentOfParent.ptrs.index(parentNodeIndex)
                    if parentPtrsIndex > 0:
                        mergeNodeIndex = parentOfParent.ptrs[parentPtrsIndex-1]
                        leftOrRight = 'left'
                    else:
                        mergeNodeIndex = parentOfParent.ptrs[parentPtrsIndex+1]
                        leftOrRight = 'right'

                    if deletedValue in parentOfParent.values:
                        parentOfParent.values.remove(deletedValue)

                    mergeNode = self.nodes[mergeNodeIndex]
                    for i, value in enumerate(parentNode.values):
                        mergeNode.values.append(value)

                    if leftOrRight == 'left':
                        parentChildItemIndex = None
                        if self.nodes[parentNode.ptrs[0]].values[0] in parentOfParent.values:
                            parentChildItemIndex = parentOfParent.values.index(self.nodes[parentNode.ptrs[0]].values[0])


                        for i, ptr in enumerate(parentNode.ptrs):
                            mergeNode.ptrs.append(ptr)

                            if self.nodes[ptr].parent != mergeNodeIndex:
                                self.nodes[ptr].parent = mergeNodeIndex

                        if parentChildItemIndex is None:
                            popped = parentOfParent.values.pop(0)
                            mergeNode.values.append(popped)
                        else:
                            popped = parentOfParent.values.pop(parentChildItemIndex)
                            mergeNode.values.append(popped)

                    else:
                        for i, ptr in reversed(list(enumerate(parentNode.ptrs))):
                            mergeNode.ptrs.insert(0,ptr)
                            if self.nodes[ptr].parent != mergeNodeIndex:
                                self.nodes[ptr].parent = mergeNodeIndex

                        popped = parentOfParent.values.pop(0)
                        mergeNode.values.insert(0, popped)

                    mergeNode.values.sort()

                    thisNode.parent = mergeNodeIndex
                    self.nodes[parentNodeIndex] = None
                    parentOfParent.ptrs.remove(parentNodeIndex)

                    return True

                return False

    def borrow(self, thisNode, siblingNode=None, siblingRorL=None, deletedValue=None, internalNode=None, borrowNode=False):
        """
        If borrowNode is False then it borrows a value from a sibling
        If borrowNode is True then it borrows a node from a sibling parent
        """

        if not borrowNode:
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
        else:
            borrowed = False
            parentNode = self.nodes[thisNode.parent]
            # leftParentInd is the left sibling index of the current's node parent
            # rightParentInd is the right sibling index of the current's node parent

            leftParentInd, rightParentInd = self.getsiblingsofparent(thisNode)

            leftParSibNode = None
            if leftParentInd != -1:
                leftParSibNode = self.nodes[leftParentInd]

            rightParSibNode = None
            if rightParentInd != -1:
                rightParSibNode = self.nodes[rightParentInd]

            # if the left sibling of the parent exists and it has enough children
            if leftParSibNode is not None and len(leftParSibNode.ptrs) > self.min_child_count:
                borrowedNode = self.nodes[leftParSibNode.ptrs[-1]]
                borrowedNodeIndex = leftParSibNode.ptrs[-1]
                leftParSibNode.ptrs.remove(borrowedNodeIndex)
                parentNode.ptrs.insert(0, borrowedNodeIndex)

                leftParSibNode.values.pop(-1)
                thisNodeIndex = self.nodes.index(thisNode)

                internal_nd = self.checkifinternal(thisNodeIndex, thisNode.values[0])
                if internal_nd is not None:
                    self.replace_item(internal_nd.values, thisNode.values[0], borrowedNode.values[0])
                parentNode.values.insert(0, thisNode.values[0])

                borrowedNode.parent = thisNode.parent
                borrowed = True
            # else if the right sibling of the parent exists and it has enough children
            elif rightParSibNode is not None and len(rightParSibNode.ptrs) > self.min_child_count:
                borrowedNode = self.nodes[rightParSibNode.ptrs[0]]
                borrowedNodeIndex = rightParSibNode.ptrs[0]
                rightParSibNode.ptrs.remove(borrowedNodeIndex)
                parentNode.ptrs.append(borrowedNodeIndex)

                rightParSibNode.values.pop(0)
                parentNode.values.append(borrowedNode.values[0])
                internal_nd = self.checkifinternal(borrowedNodeIndex, borrowedNode.values[0])
                if internal_nd is not None:
                    self.replace_item(internal_nd.values, borrowedNode.values[0], self.nodes[rightParSibNode.ptrs[0]].values[0])

                borrowedNode.parent = thisNode.parent
                borrowed = True

            return borrowed

    def redistribute(self, thisNodeIndex, thisNode, deletedValue, siblingRorL, siblingNode, parentIndex, internalNode=None):
        """
        Rearranges the internal nodes based on their children count
        """

        if parentIndex == self.root:
            parentNode = self.nodes[parentIndex]
            if len(self.nodes[self.root].values) == 0:
                # thisNode.is_leaf = False
                self.nodes[self.root] = None
                self.root = thisNodeIndex
                self.nodes[self.root].parent = None
                return

        # If the children count of the parent is lower than the minimum child count then it borrows an internal node
        if len(self.nodes[parentIndex].ptrs) < self.min_child_count:
            borrowed = self.borrow(thisNode, borrowNode=True)
            # if it didnt borrow any child
            if not borrowed:
                # then internal nodes have to be merged
                currentNodeIndex = thisNodeIndex
                currentNode = thisNode
                parentNode = self.nodes[currentNode.parent]
                parentNdIndex = currentNode.parent
                parentOfParent = None
                if parentNode.parent is not None:
                    parentOfParent = self.nodes[parentNode.parent]

                while len(parentNode.ptrs) < self.min_child_count:
                    merged = self.merge(currentNodeIndex, currentNode, mergeInternalNodes=True, parentNode=parentNode, parentNodeIndex=parentNdIndex, parentOfParent=parentOfParent)

                    if not merged:
                        break

                    if parentOfParent is not None:
                        currentNodeIndex = currentNode.parent
                        currentNode = parentNode
                        parentNode = parentOfParent
                        for i, node in enumerate(self.nodes):
                            if node == parentNode:
                                parentNdIndex = i
                                break
                        parentOfParent = None
                        if parentNode.parent is not None:
                            parentOfParent = self.nodes[parentNode.parent]

                    if len(self.nodes[self.root].values) == 0:
                        new_root = self.nodes[self.root].ptrs[0]
                        self.nodes[self.root] = None
                        self.root = new_root
                        self.nodes[self.root].parent = None
                        break
        else:
            return

    def getsiblingsofparent(self, thisNode):
        """
        returns the indexes of the parent's siblings
        """
        if thisNode.parent is None:
            return -1, -1

        nextLeft = None
        if thisNode.left_sibling is not None:
            nextLeft = self.nodes[thisNode.left_sibling]
            while nextLeft.parent == thisNode.parent:
                if nextLeft.left_sibling is not None:
                    nextLeft = self.nodes[nextLeft.left_sibling]
                else:
                    nextLeft = None
                    break

        nextRight = None
        if thisNode.right_sibling is not None:
            nextRight = self.nodes[thisNode.right_sibling]
            while nextRight.parent == thisNode.parent:
                if nextRight.right_sibling is not None:
                    nextRight = self.nodes[nextRight.right_sibling]
                else:
                    nextRight = None
                    break

        if nextLeft is not None and nextRight is not None:
            return nextLeft.parent, nextRight.parent
        elif nextLeft is not None:
            return nextLeft.parent, -1
        elif nextRight is not None:
            return -1, nextRight.parent

        return -1, -1

    def checkifinternal(self, currentNodeIndex, value):
        """
        Checks if value is present in an internal node
        If it is present it returns the internal node
        else it returns None
        """
        is_internal = False
        internalNode = self.nodes[currentNodeIndex]
        while internalNode.parent is not None:
            internalNode = self.nodes[internalNode.parent]
            if value in internalNode.values:
                is_internal = True
                return internalNode

        return None

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

        if not self.nodes:
            print("Cannot plot tree, it is empty")
            return

        # arrange the nodes top to bottom left to right
        nds = [self.root]
        for ptr in nds:
            if self.nodes[ptr] is not None:
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