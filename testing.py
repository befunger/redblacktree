# Individual project by Alexander Willemsen
# Developed for the course DD1327 Fundamentals of Computer Science at KTH Royal Institute of Technology
# This code implements some basic tests for the red-black tree main code.

import redblack
import random

def test_invariants(tree): # O(n)
    '''Verifies whether all 5 of the invariants unique to a red black tree are upheld.'''
    healthy = True
    if tree._root == None:
        return True

    if colourcheck(tree._root) == False: #Constraint 1
        print("Constraint 1 broken. Node without black or red colour found.")
        healthy = False
    if rootcheck(tree._root) == False: # Constraint 2
        print("Constraint 2 broken. Root not black.")
        healthy = False
    if leafcheck(tree._root) == False: # Constraint 3
        print("Constraint 3 broken. Non-black leaf found.")
        healthy = False
    if redcheck(tree._root) == False: # Constraint 4
        print("Constraint 4 broken. Red with non-black sub-node found.")
        healthy = False
    if blackcheck(tree._root) == False: # Constraint 5
        print("Constraint 5 broken. Differing amounts of black nodes in different branches found.")
        healthy = False

    return healthy

def colourcheck(node): # O(n)
    '''Checks if all nodes are either black or red colour attribute'''
    if node._colour == "Black" or node._colour == "Red":
        if node._data == "Leaf":
            return True
        elif colourcheck(node._left) and colourcheck(node._right):
            return True
    return False
    
def rootcheck(node): # O(1)
    '''Checks if root has black colour attribute'''
    if node._colour != "Black":
        return False
    return True

def leafcheck(node): # O(n)
    '''Checks if all leaves have black colour attribute'''
    if node._data == "Leaf":
        if node._colour == "Black":
            return True
    else:
        if leafcheck(node._left) and leafcheck(node._right):
            return True
    return False

def redcheck(node): # O(n)
    '''Checks if all red nodes have only black subnodes'''
    if node._data == "Leaf":
        return True
    
    if node._colour == "Red":
        if node._left._colour != "Black" or node._right._colour != "Black":
            return False
    if redcheck(node._left) and redcheck(node._right):
        return True
    else:
        return False

def blackcheck(node): # O(n)
    '''Checks if all branches have same black depth. (# of black nodes)
        If true, returns the depth, else returns False.'''
    if node._data == "Leaf":
        return 1

    left = blackcheck(node._left)
    right = blackcheck(node._right)
    if left == False or right == False or left != right:
        return False
    elif node._colour == "Black":
        return left + 1
    else:
        return left



# Case 1: Basic testing - Testing a simple tree and showcasing the test functions in action by intentionally breaking the established 'good' tree.
'''
Sketch of the tree constructed in Test 1: ([L] = leaf nodes)

                            Foxtrot 
                          /         \ 
                    Charlie          Victor
                   /       \         /    \ 
              Alpha        Delta   [L]   Yankee
            /     \       /    \         /    \ 
          [L]    Bravo  [L]    [L]     [L]    [L]
                 /   \ 
               [L]   [L]
'''

print("Case 1.a: Basic Test")
Tree = redblack.RedBlackTree()
Tree.insert("Victor")
Tree.insert("Foxtrot")
Tree.insert("Delta")
Tree.insert("Charlie")
Tree.insert("Alpha")
Tree.insert("Yankee")
Tree.insert("Bravo")

assert Tree.string() == "Alpha Bravo Charlie Delta Foxtrot Victor Yankee"
assert test_invariants(Tree)
assert Tree.max() == "Yankee"
assert Tree.min() == "Alpha"
assert Tree.search("Delta")
assert Tree.search("Quebec") == False
assert Tree.root() == Tree._root._data

print("\nCase 1.b: Changing the root colour")
Tree._root._colour = "Green"
assert test_invariants(Tree) == False

print("\nCase 1.c: Swapping a node colour")
Tree._root._colour = "Black"
Tree._root._left._left._colour = "Red"
assert test_invariants(Tree) == False

print("\nCase 1.d: Changing a leaf colour")
Tree._root._left._left._colour = "Black"
Tree._root._right._left._colour = "Red"
assert test_invariants(Tree) == False

#Case 2: Fringe testing - Testing edge cases
print("\nCase 2.a: Empty tree")
Tree = redblack.RedBlackTree()
assert test_invariants(Tree)
assert Tree.root() == None
assert Tree.max() == None
assert Tree.min() == None
assert Tree.string() == None
assert Tree.search("element") == False

print("\nCase 2.b: Root only")
Tree = redblack.RedBlackTree()
Tree.insert("Datalogi")
assert test_invariants(Tree)
assert Tree.string() == "Datalogi"
assert Tree.max() == "Datalogi"
assert Tree.min() == "Datalogi"
assert Tree.search("Datalogi")

print("\nCase 2.c: Inserting sorted data") # Note that this is the worst-case that gives many other binary search trees O(n) operations
Tree = redblack.RedBlackTree()
for i in range(1000):
    Tree.insert(i)
assert test_invariants(Tree)
assert Tree.root() != 0 # Shows that the tree has rebalanced regardless of the sorted input
assert Tree.max() == 999
assert Tree.min() == 0
assert Tree.search(523)


# Case 3: Bulk testing - Generates 100 trees with 1000 random entries each, and checks that they all uphold all invariants
print("\nCase 3: Bulk testing")
for i in range(100):
    Tree = redblack.RedBlackTree()
    for j in range(1000):
        entry = str(random.randint(1, 99999))
        Tree.insert(entry)
    assert test_invariants(Tree)
    assert int(Tree.max()) < 100000
    assert int(Tree.min()) > 0


print("\nAll tests completed!")