'''
给你二叉树的根节点 root ，返回它节点值的 前序 遍历。
           1
        /     \
       2       3
      / \       \
     4  5        6
前：中左右 [1,2,4,5,4,6]
中：左中右 [4, 2, 5, 1, 3, 6]
后：左 -> 右 -> 根 [4, 5, 2, 6, 3, 1]
'''
from typing import *
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class state:
    def __init__(self):
        self.left=False
        self.right = False

class Solution:
    def __init__(self):
        self.traver_lis = []

    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root==None:
            return []
        def dfs(root):
            if root==None:
                return
            self.traver_lis.append(root.val)
            dfs(root.left)
            dfs(root.right)
        dfs(root)


if __name__=="__main__":
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


    solution=Solution()
    if True:
        solution.preorderTraversal(node1)
        print(solution.traver_lis)