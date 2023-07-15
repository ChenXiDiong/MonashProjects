""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ 
        Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is 
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert
            it. After insertion, performs sub-tree rotation whenever it becomes
            unbalanced.
            returns the new root of the subtree.

            Complexity: O(log(n)) where n is the number of nodes in the tree. The worst case is when
            we are inserting at the leaf, in which the function traverses a part but not all of the tree
            recursively. The comparison of the keys are in O(comp) but is not as dominant as the recursive
            part of the insert_aux function. The other functions such as get_height, rebalance and 
            assignment are in O(1).
        """
        if current is None:  
            current = AVLTreeNode(key, item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
            current.height = max(self.get_height(current.left),self.get_height(current.right)) + 1
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
            current.height = max(self.get_height(current.left),self.get_height(current.right)) + 1
        else:  # key == current.key
           raise ValueError('Inserting duplicate item')
        return self.rebalance(current)


    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete. After deletion,
            performs sub-tree rotation whenever it becomes unbalanced.
            returns the new root of the subtree.

            Complexity: O(log(n)), where n is the number of nodes in the tree. The dominant line of
            code is the get_successor function, which is in O(log(n)). Although the comparison of the
            keys are in O(comp), it is not as dominant as get_successor. The other functions such as
            is_leaf, get_height, rebalance, assignment, raise are all in O(1).
        """

        if current is None:  # key not found
            raise ValueError('Deleting  a non-existent item')
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
            current.height = max(self.get_height(current.left),self.get_height(current.right)) + 1
        elif key < current.key:
            current.left  = self.delete_aux(current.left, key)
            current.height = max(self.get_height(current.left),self.get_height(current.right)) + 1
        
        
        else:  
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        return self.rebalance(current)

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1), since it is only doing assignments, which is in O(1).
        """
        CurrentRight= current.right
        mid= CurrentRight.Left

        CurrentRight.left= current
        current.right=mid

        self.get_height(current)
        return CurrentRight
        


    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1), since it is only doing assignments, which is in O(1).
        """

        new_current = current.left
        current.left = new_current.right

        new_current.right = current

        current.height = max(self.get_height(current.right), self.get_height(current.left))+1
        new_current.height =  max(self.get_height(new_current.right), self.get_height(new_current.left))+1
        return new_current


    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.

            Complexity: O(1), since get_balance, get_height, left_rotate and right_rotate are all in 
            O(1), and the return, comparison and assignment statements are in O(1) as well.
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    def kth_largest(self, k: int) -> AVLTreeNode:
        """
        Returns the kth largest element in the tree.
        k=1 would return the largest.

        Complexity: O(log(n)) where n is the number of nodes in the tree. Since both kth_largest_aux and 
        kth_smallest_aux are both in O(log(n)), the overall complexity of this function will only be 
        O(log(n)). Since empty list creation, comparison of integers, return, list access, and 
        mathematical operations are all in O(1).
        """
        res = []
        if k < len(self)//2:
            self.kth_largest_aux(self.root, k, res)
            return res[k-1]
        else:
            self.kth_smallest_aux(self.root, k, res)
            return res[len(self)-k]
    
    def kth_largest_aux(self, current: AVLTreeNode, k: int, res: list) -> list:
        """
        Recursive method to find the kth largest element in the AVL tree for values of k smaller than
        half the size of the tree.  

        Complexity: O(log(n)) where n is the number of nodes in the tree. Since k would not be any 
        greater than half the number of nodes, nor would it be less than 1, only half of the tree would 
        be traversed in the worst case, therefore the complexity of this function is in O(log(n)). 
        """
        if len(res) == k:
            return res
        elif current is None:
            return res
        else:
            self.kth_largest_aux(current.right, k, res)
            res.append(current)
            self.kth_largest_aux(current.left, k, res)
            return res

    def kth_smallest_aux(self, current: AVLTreeNode, k: int, res: list) -> list:
        """
        Recursive method to find the kth largest element in the AVL tree for values of k larger than
        half the size of the tree. 

        Complexity: O(log(n)) where n is the number of nodes in the tree. Since k would not be any 
        lesser than half the number of nodes, nor would it be more than the total number of nodes in the
        tree, only half of the tree would be traversed in the worst case, therefore the complexity of 
        this function is in O(log(n)).
        """
        if len(res) == len(self)-k+1:
            return res
        elif current is None:
            return res
        else:
            self.kth_smallest_aux(current.left, k, res)
            res.append(current)
            self.kth_smallest_aux(current.right, k, res)
            return res


