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
        print("Node Class delete Method:")
        print(f"value: {value}, ptr: {ptr}, ptrs: {self.ptrs}")
        for index, existing_val in enumerate(self.values):
            if value == existing_val:
                self.values.pop(index)

                if self.is_leaf:
                    self.ptrs.pop(index)
                break
        print(f"value: {value} deleted successfully")


class Btree:
    def __init__(self, b):
        """
        The tree abstraction.
        """
        self.b = b  # branching factor
        self.nodes = []  # list of nodes. Every new node is appended here
        self.root = None  # the index of the root node

        self.max_child_count = b # if b = 3
        self.min_child_count = math.ceil(b / 2) # then min_child is 2
        self.min_leaf_count = math.ceil(b / 2) - 1  # then min_leaf_count is 1

        self.insert_count = 0

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

    def delete(self, value):
        if self.root is None:
            print('Tree is empty')
            return



        # find the index of the node that the value and its ptr/s should be inserted to (_search)
        index = self._search(value)

        index_in_node = self.nodes[index].values.index(value)
        pointerr = self.nodes[index].ptrs[index_in_node]
        print ("**************************************")
        print(f"Value: {value}, pointer: {pointerr} ")
        print(f"Node values: {self.nodes[index].values}, Node pointers: {self.nodes[index].ptrs}")
        print ("**************************************")

        #Checks if the
        #value
        #exists in internal
        #nodes
        is_internal = False
        check_node = self.nodes[index]
        while check_node.parent is not None:
            check_node = self.nodes[check_node.parent]
            if value in check_node.values:
                is_internal = True
                break

        # delete it
        self.nodes[index].delete(value, pointerr)

        if len(self.nodes[index].values) < self.min_leaf_count:
            # ama den yparxei kanena value h ta values einai ligotera tou b//2
            # tote ginetai merge kai telos diagrafetai to node
            print("************* MERGE **************")
            if self.nodes[index].left_sibling is None:
                borrowed_value = self.nodes[self.nodes[index].right_sibling].values[0]
                borrowed_ptr = self.nodes[self.nodes[index].right_sibling].ptrs[0]
                if len(self.nodes[self.nodes[index].right_sibling].values) > self.min_leaf_count:
                    self.nodes[index].insert(borrowed_value, borrowed_ptr)
                    self.nodes[self.nodes[index].right_sibling].delete(borrowed_value, borrowed_ptr)

                    for i in range(len(self.nodes[self.nodes[index].parent].values)):
                        if self.nodes[self.nodes[index].parent].values[i] == borrowed_value:
                            self.nodes[self.nodes[index].parent].delete(self.nodes[self.nodes[index].parent].values[i], self.nodes[self.nodes[index].parent].ptrs[i])
                            self.nodes[self.nodes[index].parent].insert(self.nodes[self.nodes[index].right_sibling].values[0], None)
                            break

            elif is_internal:
                left_sib = self.nodes[self.nodes[index].left_sibling]
                right_sib = self.nodes[self.nodes[index].right_sibling]
                if len(left_sib.values) > self.min_leaf_count and self.nodes[left_sib.parent] == self.nodes[self.nodes[index].parent]:
                    self.nodes[index].insert(left_sib.values[-1], left_sib.ptrs[-1])
                    left_sib.delete(left_sib.values[-1], left_sib.ptrs[-1])

                    check_node.delete(check_node.values[0], check_node.ptrs[0])
                    check_node.insert(self.nodes[index].values[0], None)

                elif len(right_sib.values) > self.min_leaf_count:
                    # to 90 kai sto internal kai sto leaf ginetai right sibling min value (100)
                    # to right sibling min value sto parent node pairnei thn timh toy neou right sibling min value
                    borrowed_value = right_sib.values[0]
                    borrowed_ptr = right_sib.ptrs[0]
                    self.nodes[index].insert(borrowed_value, borrowed_ptr)
                    #self.nodes[index].values.append(borrowed_value)
                    #self.nodes[index].ptrs.append(borrowed_ptr)

                    new_index = check_node.values.index(value)
                    popped = right_sib.values[0]
                    right_sib.delete(right_sib.values[0], right_sib.ptrs[0])
                    popped_parent = self.nodes[self.nodes[index].parent].values.index(popped)

                    check_node.delete(check_node.values[new_index], check_node.ptrs[new_index])
                    check_node.insert(self.nodes[index].values[0], None)

                    prntnode = self.nodes[self.nodes[index].parent]
                    prntnode.delete(prntnode.values[popped_parent], prntnode.ptrs[popped_parent])
                    prntnode.insert(right_sib.values[0], None)

                elif len(right_sib.values) == self.min_leaf_count:
                    print("************ MERGE *************")
                    self.merge(self.nodes[index], self.nodes[self.nodes[index].right_sibling])
                    pass
                # diagrafw to 55
                # enwnetai me to deksia an den exei timh na tou danisei
                # to parent node tou deksia ginetai grandparent node (dhladh parent node sto parent node tou)
        else:
            parentnode = self.nodes[self.nodes[index].parent]
            for i in range(len(parentnode.values)):
                if value == parentnode.values[i]:
                    parentnode.delete(parentnode.values[i], parentnode.ptrs[i])
                    parentnode.insert(self.nodes[index].values[0], None)#self.nodes[index].ptrs[0])
                    break
            node = self.nodes[index]
            while node.parent is not None:
                # loop through the parents to check if the deleted value is
                # in an internal node
                node = self.nodes[node.parent]
                if value in node.values:
                    for i in range(len(node.values)):
                        if value == node.values[i]:
                            node.delete(node.values[i], node.ptrs[i])
                            node.insert(self.nodes[index].values[0], None)
                            break
                    break


    #######################################
    #                MERGE                #
    #######################################

    def merge(self, node1, node2):
        node = Node(self.b, node2.values+node1.values, node1.ptrs+node2.ptrs,node1.left_sibling, node2.right_sibling, node2.parent, True)

        self.nodes.remove(node1)
        self.nodes.remove(node2)
        return node

        # if there's a left sibling and has enough values
        # then borrow from left
        # else if there's a right sibling and has enough values
        # then borrow from right
        #

        # self.nodes.pop(index)  # xwris auto, to node tha exei mia kenh lista mesa -> []

        # if the node has less elements than b/2
        # """
        # # the node has less than b/2-1 keys
        # if len(self.nodes[index].values) < math.ceil(self.b / 2) - 1:
        #     left_sibling_node = None
        #     right_sibling_node = None
        #     if self.nodes[index].left_sibling is not None: # borei na mhn yparxei aristero sibling
        #         left_sibling_node = self.nodes[self.nodes[index].left_sibling]
        #     if self.nodes[index].right_sibling is not None: # borei na mhn yparxei deksi sibling
        #         right_sibling_node = self.nodes[self.nodes[index].right_sibling]
        #
        #     # see if we can borrow from the left sibling
        #     if left_sibling_node is not None:
        #         if len(left_sibling_node.values) < math.ceil(self.b / 2) - 1:
        #             # insert to the node the max value from the left sibling and delete it from the sibling
        #             self.nodes[index].insert(left_sibling_node.values[-1]) # -1 = max value (from right to left)
        #             left_sibling_node.delete(left_sibling_node.values[-1])
        #             # if we can't borrow from the left sibling, then we see if there is a left sibling and merge them
        #         else:
        #             self.merge(index)
        #             # make a new node
        #             # new_values = self.nodes[index].values + left_sibling_node.values
        #             # new_values.sort(reverse=False)
        #             # new_ptrs = self.nodes[index].ptrs + left_sibling_node.ptrs
        #             # new_node = Node(self, self.b, values=new_values.sort(reverse=False) , ptrs=new_ptrs.sort(reverse=False),
        #             # left_sibling=self.nodes[index].left_sibling, right_sibling=self.nodes[index].right_sibling, parent=self.nodes[index].parent, is_leaf=self.nodes[index].is_leaf)
        #             # self.nodes[index] = new_node
        #     elif right_sibling_node is not None:
        #         if len(right_sibling_node.values) < math.ceil(self.b / 2) - 1:
        #             # insert to the node the min value of the right sibling
        #             self.nodes[index].insert(right_sibling_node.values[0])
        #             right_sibling_node.delete(right_sibling_node.values[0])
        #         # else merge with the right sibling
        #         else:
        #             self.merge(index)
        # """

    def borrow(self, sibling, node_id):
        if sibling == 'left':
            node = self.nodes[node_id]
            left_node = self.nodes[node.left_sibling]
            # take and remove the max value of the left node
            borrowed_value = left_node.values.pop(-1)
            # we add the value to node
            node.values.append(borrowed_value)
            # sort the values of the node to ascending
            node.values.sort(reverse=False)
            # check if the left node needs merge
            if len(left_node.values) < self.b / 2:
                #self.merge(node.left_sibling)
                print('left node mpika')
        else:
            node = self.nodes[node_id]
            right_node = self.nodes[node.right_sibling]
            # take and remove the max value of the left node
            borrowed_value = right_node.values.pop(0)
            # we add the value to node
            node.values.append(borrowed_value)
            # sort the values of the node to ascending
            node.values.sort(reverse=False)
            # check if the left node needs merge
            if len(right_node.values) < self.b / 2:
                #self.merge(node.right_sibling)
                print('right node mpika')

    def _search(self, value, return_ops=False):
        """
        Returns the index of the node that the given value exist or should exist in.

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
        print("################## LEAFS ####################")
        for i in range(len(self.nodes)):
            if self.nodes[i].is_leaf:
                print(f"[{i}] -- Pointers: {self.nodes[i].ptrs}, Values: {self.nodes[i].values}")
        print("#############################################")
        print("\n################ NON-LEAFS ##################")
        for i in range(len(self.nodes)):
            if not self.nodes[i].is_leaf:
                print(f"[{i}] -- Pointers: {self.nodes[i].ptrs}, Values: {self.nodes[i].values}")
                if i == 17:
                    print(f"Index 18 node values: {self.nodes[18].values}")
        print("#############################################")

        print(f"Root: {self.root}")
        print(f"Nodes length: {len(self.nodes)}")
        # arrange the nodes top to bottom left to right
        nds = [self.root]
        for ptr in nds:
            if self.nodes[ptr].is_leaf:
                continue
            nds.extend(self.nodes[ptr].ptrs)

        # add each node and each link
        g = 'digraph G{\nforcelabels=true;\n'

        for i in nds:
            node = self.nodes[i] # changed i to i - 1
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
#dsadsada