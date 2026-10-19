'''
https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/
给你二叉树的根结点 root ，请你将它展开为一个单链表：

展开后的单链表应该同样使用 TreeNode ，其中 right 子指针指向链表中下一个结点，而左子指针始终为 null 。
展开后的单链表应该与二叉树 先序遍历 顺序相同。

思路，采用深度优先遍历的方式，将二叉树存储起来，再按照从左到右的思路将其连接上去

'''
import copy
from typing import *

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def __init__(self):
        self.path_record=[]
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        if not root:
            return None
        def dfs(root):
            if root==None:
                return
            self.path_record.append(root)
            dfs(root.left)
            dfs(root.right)

        dfs(root)
        preRoot=TreeNode(-1)
        preRootCopy=preRoot
        n=len(self.path_record)
        for i in range(n):
            preRoot.right=self.path_record[i]
            preRoot.left=None
            preRoot=self.path_record[i]
        return preRootCopy.left
if __name__=='__main__':
    node1 = TreeNode(1)
    node2 = TreeNode(2)
    node4_1 = TreeNode(4)
    node4_2 = TreeNode(4)
    node5 = TreeNode(5)
    node5_1 = TreeNode(5)
    node7 = TreeNode(7)
    node8 = TreeNode(8)
    node11 = TreeNode(11)
    node13 = TreeNode(13)
    node5.left = node4_1
    node5.right = node8
    node4_1.left = node11
    node8.left = node13
    node8.right = node4_2
    node11.left = node7
    node11.right = node2
    node4_2.left = node5_1
    node4_2.right = node1
    solution=Solution()
    preRoot=solution.flatten(node5)
    while preRoot:
        print(preRoot.val)
        preRoot=preRoot.left