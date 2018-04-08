# Working but mostly undocumented minimalist binary heap implementation.
#  Returns HeapNode references from the insert method.

#NOTE
#I modified it so I can look up a node by it's name using a hash table
#This is used so I can call decrease key on a node without search time

class HeapNode:
    def __init__(self, index, data, name="Null"):
        self.index = index
        self.data = data
        self.name = name
    def __str__(self):
        return str(self.index) + ":" + str(self.data)

class Heap:
    def __init__(self):
        self.nodes = []
        self.node_dict = {}

    def empty(self):
        return len(self.nodes) == 0

    def swap(self, node1, node2):
        self.nodes[node1.index] = node2
        self.nodes[node2.index] = node1
        temp = node1.index
        node1.index = node2.index
        node2.index = temp

    def getParent(self, node):
        if (node.index <= 0):
            return None
        else:
            return self.nodes[(node.index-1)//2]

    def getLeftChild(self, node):
        index = (node.index*2)+1
        if (index < len(self.nodes)):
            return self.nodes[index]
        else:
            return None

    def getRightChild(self, node):
        index = (node.index*2)+2
        if (index < len(self.nodes)):
            return self.nodes[index]
        else:
            return None

    def decreaseKey(self, node):
        parent = self.getParent(node)
        while (parent != None):
            if (node.data < parent.data):
                self.swap(node, parent)
            else:
                break
            parent = self.getParent(node)

    def increaseKey(self, node):
        swapped = True

        while swapped:
            swapped = False
            minChild = self.getLeftChild(node)
            rightChild = self.getRightChild(node)
            if (rightChild != None and rightChild.data < minChild.data):
                minChild = rightChild
            if (minChild != None and minChild.data < node.data):
                self.swap(minChild, node)
                swapped = True

    def deleteLast(self):
        if len(self.nodes) > 0:
            return self.nodes.pop()
        else:
            return None

    #O(1) op
    def getByName(self, name):
        return self.node_dict[name]

    def insert(self, data, name="Null"):
        node = HeapNode(len(self.nodes), data,name)
        #Added node hash table
        self.node_dict[name] = node
        self.nodes.append(node)
        self.decreaseKey(node)
        return node

    def deleteMin(self):
        if len(self.nodes) > 0:
            m = self.nodes[0]
            last = self.deleteLast()
            if len(self.nodes) > 0:
                last.index = 0
                self.nodes[0] = last
                self.increaseKey(last)

            return (m.data, m.name)
        else:
            return None

    def __str__(self):
        return str([str(x) for x in self.nodes])


if __name__ == "__main__":
    # test using naive heapsort

    from random import *
    values = [randint(0,1000) for x in range(1000)]
    h = Heap()
    nodes = [h.insert(v) for v in values]

    assert sorted(values) == [h.deleteMin() for x in values]
