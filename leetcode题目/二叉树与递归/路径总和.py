'''
https://leetcode.cn/problems/path-sum-ii/

给你二叉树的根节点 root 和一个整数目标和 targetSum ，找出所有 从根节点到叶子节点 路径总和等于给定目标和的路径。

叶子节点 是指没有子节点的节点。



示例 1：
输入：root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
输出：[[5,4,11,2],[5,8,4,5]]
输入：root = [1,2,3], targetSum = 5
输出：[]

思路：采用深度优先搜索的方式进行解题。
这个方法做下来，不好的地方就在于需要进行深度拷贝，而且回溯也不好进行回溯。
这道题的难点在于回溯的时机
                   8
            4            8
        11           13     4
      7    2              5    1

8->4->11->7 此时7的left和right满足条件
回溯 8->4->11 找11的右子树
8->4->11->2 2的left和right满足条件，回溯
8->4->11 11递归完成，递归完成回溯
8->4    4找右子树，右子树为None，回溯
8 8找右子树
8->8->13 13满足条件回溯

所以这个回溯的最好时机在于，将一个点的左右子树走完然后进行回溯，并且为了避免记录路径的list的被重置，需要
使用深拷贝进行list的拷贝。

例如：
8->4->11->7 ，走到7,7的左右子树都为None记录路径
7.左子树为none->return 7，右子树为none return 回溯
8->4->11 找11的右子树
8->4->11->2 2的left和right满足条件记录路径
11的左右子树走完，回溯。
8->4   4找右子树，右子树为None，回溯
8 8找右子树
8->8->13 13左右子树都为None,记录路径。
依次类推
'''
from typing import *
import copy
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def __init__(self):
        self.tranver_res=[] #记录路径的遍历结果
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        if root is None:
            return []
        path_record=[]
        def dfs(root,path_record):
            '''
            这个计算出来的路径有重复
            :param root:
            :param path_record:
            :return:
            '''
            if sum(path_record)==targetSum:
                a=copy.deepcopy(path_record)
                self.tranver_res.append(a)
            if root==None:
                return

            path_record.append(root.val)
            dfs(root.left,path_record)
            dfs(root.right,path_record)
            path_record.pop()
        dfs(root,path_record)
        return  self.tranver_res
    def pathSum1(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        if root is None:
            return []

        def dfs(root,path_record):
            if not root:
                return
            path_record.append(root.val)
            # 题目中没有说这个target是正数还是负数，所以不做处理
            # if sum(path_record)>targetSum:
            #     path_record.pop()
            #     return
            if not root.left and not root.right and sum(path_record)==targetSum:
                a = copy.deepcopy(path_record)
                self.tranver_res.append(a)

            dfs(root.left,path_record)
            dfs(root.right,path_record)
            path_record.pop()
        dfs(root,[])
        return self.tranver_res
if __name__=="__main__":
    node1=TreeNode(1)
    node2=TreeNode(2)
    node4_1=TreeNode(4)
    node4_2=TreeNode(4)
    node5=TreeNode(5)
    node5_1 = TreeNode(5)
    node7=TreeNode(7)
    node8=TreeNode(8)
    node11=TreeNode(11)
    node13=TreeNode(13)
    node5.left=node4_1
    node5.right=node8
    node4_1.left=node11
    node8.left=node13
    node8.right=node4_2
    node11.left=node7
    node11.right=node2
    node4_2.left=node5_1
    node4_2.right=node1
    solution=Solution()
    res=solution.pathSum1(node5,22)
    print(res)
