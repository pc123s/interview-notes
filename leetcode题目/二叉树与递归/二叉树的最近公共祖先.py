'''
https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/description/
https://www.algomooc.com/852.html
给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。
百度百科中最近公共祖先的定义为：“对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”

示例 1：
输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
输出：3
解释：节点 5 和节点 1 的最近公共祖先是节点 3 。

示例 2：
输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
输出：5
解释：节点 5 和节点 4 的最近公共祖先是节点 5 。因为根据定义最近公共祖先节点可以为节点本身。

示例 3：
输入：root = [1,2], p = 1, q = 2
输出：1

思路1：
这个题有很多思路，其中最著名的就是递归。但是我看了递归的方法，没有看懂。要ac的话，有一种方法即分别遍历两个节点，记录路径，然后根据遍历的路径去找。

                       3
                5           1
            6     2      0     8
                7   4
p和q是6和4，利用前序遍历就是 p:3->5->6
q:3->5->2->4
如果是公共祖先，那么两者的公共路径的后一个值就是公共的祖先。
如果是
3->5->6 3->5->6->7呢，那么公共祖先就是6
但是这种耗时太高


注意:
1、这里要注意深拷贝的问题，l=[1,2,3] l1=copy.deepcopy(l) l==l1是False，因为两个的内存不同了

'''
from typing import *
import copy
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def __init__(self):
        self.res1=[]
        self.res2=[]
        self.is_find=False #设置一个全局变量来控制整个的递归过程
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        '''
        方法1不对，这是因为python中的==比较也是在比较内存的，深度copy了以后内存变了，所以不好进行判断，解决方法是一遍遍历找到所有的路径
        :param root:
        :param p:
        :param q:
        :return:
        '''
        if root == None:
            return None


        def dfs(root, path_record, target_Node1,target_Node2):
            if root == None or self.is_find:
                return
            print(root.val)
            path_record.append(root)
            if root == target_Node1:
                a = copy.deepcopy(path_record)
                self.res1=a
                #print(a)

                #self.is_find = True
            if root==target_Node2:

                a = copy.deepcopy(path_record)
                #print(a)
                self.res2=a
                #self.is_find = True


            # 是否找到数据了，找到了就位False
            # print(self.is_find)
            dfs(root.left, path_record, target_Node1,target_Node2)
            dfs(root.right, path_record, target_Node1,target_Node2)
            path_record.pop()
        path_record = []
        dfs(root, path_record, p,q)
        print(self.res1)
        print(self.res2)
        if not self.res1 or not self.res2:
            return None

        # 始终保持 path_res1和p为较短的路径
        if len(self.res1) > len(self.res2):
            self.res1, self.res2 = self.res2,self.res1

        is_diff=False
        for i in range(len(self.res1)):
            if self.res1[i].val != self.res2[i].val:
                is_diff=True
                break
        if is_diff:
            return self.res1[i - 1]
        else:
            return self.res1[i]
    def lowestCommonAncestor1(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        '''
        标准做法
        :param root:
        :param p:
        :param q:
        :return:
        '''
        if not root:
            return None

        # 遇见两个节点分别返回节点本身
        if root==p:
            return p
        if root==q:
            return q
        # 在左边和右边分别去找，并返回找到的值
        left=self.lowestCommonAncestor1(root.left,p,q)
        right=self.lowestCommonAncestor1(root.right,p,q)


        # 左子树没有找到并且右子树也没有找到
        if not left and not right:
            return None
        elif not left:
            return right
        elif not right:
            return left
        else:
            return root


if __name__=="__main__":
    '''
    以这个例子中的树为例
    https://leetcode.cn/problems/path-sum-ii/
    '''
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
    res=solution.lowestCommonAncestor1(node5,node2,node11)
    print(res)