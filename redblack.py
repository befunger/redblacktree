# Individual project by Alexander Willemsen
# Developed for the course DD1327 Fundamentals of Computer Science at KTH Royal Institute of Technology
# This code implements a red-black tree

class _Node:
    '''A node of the binary tree'''
    def __init__(self, inputData, colour, parent):
        self._data = inputData
        self._parent = parent
        self._left = _Leaf()
        self._right = _Leaf()
        self._colour = colour

class _Leaf:
    '''A leaf, the bottom placeholder elements for nodes.'''
    def __init__(self):
        self._data = "Leaf"
        self._colour = "Black"

class RedBlackTree():
    '''The main class for the Red Black Tree, containing all private and public methods for interacting with it.'''
    def __init__(self):
        self._root = None
        
    def _rightrot(self, old): # O(1)
        '''Performs a right rotation around specified node'''
        new = old._left
        old._left = new._right
        if new._right._data != "Leaf":
            new._right._parent = old

        if old == self._root:
            self._root = new
        else:
            new._parent = old._parent
            if old == old._parent._right:
                old._parent._right = new
            else:
                old._parent._left = new
        
        new._right = old
        old._parent = new
        return new

    def _leftrot(self, old): # O(1)
        '''Performs a left rotation around specified node'''
        new = old._right
        old._right = new._left
        if new._left._data != "Leaf":
            new._left._parent = old

        if old == self._root:
            self._root = new
        else:
            new._parent = old._parent
            if old == old._parent._left:
                old._parent._left = new
            else:
                old._parent._right = new
        
        new._left = old
        old._parent = new
        return new

    def insert(self, input): # O(log n)
        '''Adds a new element to the tree'''
        if self._root == None:
            self._root = _Node(input, "Black", None) # Root node is always black and has no parent
        else:
            self._insert(input, self._root, None)

    def _insert(self, input, base, parent, side = None): # O(log n)
        '''Finds the correct place to insert new node'''
        if base._data == "Leaf":
            base = _Node(input, "Red", parent)
            if side == "left":
                parent._left = base
            else:
                parent._right = base

            if base._parent._parent == None:
                return
            self._insertfix(base)   # Tree gets rebalanced to maintain invariants
        
        if input == base._data:
            return
        elif input < base._data:
            self._insert(input, base._left, base, "left")
        else:
            self._insert(input, base._right, base, "right")

    def _insertfix(self, base): # O(log n)
        '''Rebalances the tree after a new insert to uphold invariants'''
        # base is the node worked on
        # father is the parent node of base
        # uncle is the (potential) second child node to father's parent node (sibling of father, uncle of base)
        if base._parent._colour == "Black":
            return

        father = base._parent
        if father == father._parent._left:
            uncle = father._parent._right

            if uncle._colour == "Red":
                father._colour = "Black"
                uncle._colour = "Black"
                if father._parent != self._root: # If father and uncle are the children of the root node, the tree remains balanced (equal # of black nodes in all branches)
                    father._parent._colour = "Red"
                    self._insertfix(father._parent)
            else:
                if base == father._right:
                    father = self._leftrot(father)

                father._colour = "Black"
                father._parent._colour = "Red"
                self._rightrot(father._parent)

        else:
            uncle = father._parent._left

            if uncle._colour == "Red":
                father._colour = "Black"
                uncle._colour = "Black"
                if father._parent != self._root:
                    father._parent._colour = "Red"
                    self._insertfix(father._parent)
            else:
                if base == father._left:
                    father = self._rightrot(father)

                father._colour = "Black"
                father._parent._colour = "Red"
                self._leftrot(father._parent)
        self._root._colour = "Black"

    def max(self, node = None): # O(log n)
        '''Returns the max value in the tree (None if empty)'''
        if node == None:
            if self._root == None:
                return None
            else:
                node = self._root
        while node._right._data != "Leaf":
            node = node._right
        return node._data

    def min(self, node = None): # O(log n)
        '''Returns the min value in the tree (None if empty)'''
        if node == None:
            if self._root == None:
                return None
            else:
                node = self._root
        while node._left._data != "Leaf":
            node = node._left
        return node._data

    def root(self): # O(1)
        '''Returns the root data (None if empty)'''
        if self._root == None:
            return None
        return self._root._data
        
    def search(self, input): # O(log n)
        '''Looks up an input in the tree, returns True if it exists, False otherwise.'''
        node = self._root
        if node == None:
            return False
        while node._data != "Leaf":
            if node._data == input:
                return True
            elif input < node._data:
                node = node._left
            else:
                node = node._right
        return False

    def string(self, base = None): # O(n)
        '''Returns a string of all entries in sorted order'''
        string = ""
        if base == None:
            if self._root == None:
                return None
            else:
                base = self._root

        if base._left._data != "Leaf":
            string = self.string(base._left)
        
        if string != "":
            string += " "
        string += base._data

        if base._right._data != "Leaf":
            string += " " + self.string(base._right)
        
        return string
