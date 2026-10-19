'''
二叉树的层序遍历

https://www.algomooc.com/795.html
其实就是将树一层一层的进行遍历.（即逐层地，从左到右访问所有节点）

一开始我想着用递归做，但是我发现这个递归的话不好找递归的边界值，所以，现在用栈来实现
思路1：
分别将节点入栈，然后入栈的同时记录val，将节点的左右节点进行入栈，依次类推
https://zhuanlan.zhihu.com/p/73438175
以这个为例
[A] 记录 A
[C B] 记录C B



'''
from typing import *
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def __init__(self):
        self.tranver_lis=[]
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if root==None:
            return  self.tranver_lis
        stack=[]
        stack.append(root)
        while stack:
            c_treenode=stack.pop(0)
            self.tranver_lis.append(c_treenode.val)
            if c_treenode.left!=None:
                stack.append(c_treenode.left)
            if c_treenode.right!=None:
                stack.append(c_treenode.right)
        return self.tranver_lis


if __name__=="__main__":
    solution=Solution()
    node1 = TreeNode("A")
    node2 = TreeNode("B")
    node3 = TreeNode("C")
    node4 = TreeNode("D")
    node5 = TreeNode("E")
    node6 = TreeNode("F")
    node7 = TreeNode("G")
    node8 = TreeNode("H")
    node9 = TreeNode("I")

    node1.left=node2
    node1.right=node3
    node2.left=node4
    node2.right=node5
    node4.left=node6
    node4.right=node7
    node7.left = node8
    node7.right = node9
    res=solution.levelOrder(node1)
    print(res)