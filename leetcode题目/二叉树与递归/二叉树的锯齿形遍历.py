'''
给定一个二叉树，返回其节点值的锯齿形层序遍历。（即先从左往右，再从右往左进行下一层遍历，以此类推，层与层之间交替进行）。

https://zhuanlan.zhihu.com/p/73438175
例如：
给定二叉树 [3,9,20,null,null,15,7],

    3
   / \
  9  20
    /  \
   15   7
返回锯齿形层序遍历如下：

[
  [3],
  [20,9],
  [15,7]
]
思路：
遍历看当时的元素是在奇数层还是偶数层，偶数层的话需要反转插入的顺序
创建两个栈，一个入最新的元素，一个收集最新元素输出的元素，
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

    def zigzagLevelOrder(self, root: TreeNode) -> List[List[int]]:
        if root==None:
            return  self.tranver_lis
        stack1=[] #如最新的元素
        stack2=[] #收集最新元素的输出
        stack1.append(root)
        count=1 # 记录层数，看在奇数层还是偶数层
        while stack1 or stack2:
            #如果是偶数，反转list
            if count % 2 == 0:
                stack1=stack1[::-1]            #
            while stack1:
                cNode=stack1.pop(0)
                self.tranver_lis.append(cNode.val)
                stack2.append(cNode)
            while stack2:
                cNode_insert=stack2.pop(0)
                if cNode_insert.left:
                    stack1.append(cNode_insert.left)
                if cNode_insert.right:
                    stack1.append(cNode_insert.right)
            count+=1
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
    res=solution.zigzagLevelOrder(node1)
    print(res)