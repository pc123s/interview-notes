'''
给定一个二叉搜索树的根节点 root 和一个值 key，删除二叉搜索树中的 key 对应的节点，并保证二叉搜索树的性质不变。返回二叉搜索树（有可能被更新）的根节点的引用。
一般来说，删除节点可分为两个步骤：
首先找到需要删除的节点；
如果找到了，删除它。

输入：root = [5,3,6,2,4,null,7], key = 3
输出：[5,4,6,2,null,null,7]
解释：给定需要删除的节点值是 3，所以我们首先找到 3 这个节点，然后删除它。
一个正确的答案是 [5,4,6,2,null,null,7], 如下图所示。
另一个正确答案是 [5,2,6,null,4,null,7]。


示例 2:

输入: root = [5,3,6,2,4,null,7], key = 0
输出: [5,3,6,2,4,null,7]
解释: 二叉树不包含值为 0 的节点
示例 3:

输入: root = [], key = 0
输出: []

思路主要是：保持二叉树的性质不变，以先序遍历为例，即我进行先序遍历，不能
遍历到结束，除了删除的节点不对以外，其他是不变的。

其次，这个是一个二叉搜索树，这也代表左节点的值都是小于当前节点的
https://leetcode.cn/problems/path-sum-ii/
                           5
                         /   \
                        4     7
                       /     / \
                      2     6   9
                     /  \      / \
                    1    3    8
那么删除分三种情况：
删除节点的左子树和右子树都是None,比如节点1，那么直接删除节点，让上一个节点对应子树为None,返回None
                           5
                         /   \
                        4     7
                       /     / \
                      2     6   9
                     / \       /
                   None 3     8
删除节点的左子树为None,右子树不为None,右孩子补位，返回右子树为ROOT,比如删除左边的节点2
                           5
                         /   \
                        4     7
                       /     / \
                      3     6   9
                               /
                              8
删除节点的左子树不为None,右子树为None,左孩子补位，返回左子树为ROOT
                           5
                         /   \
                        4     7
                       /     / \
                      2     6   9
                     / \       /
                    1  None    8

                           5
                         /   \
                        4     7
                       /     / \
                      1     6   9
                               /
                              8
删除节点的左右子树都不为None,
两种方法：1、找到删除节点右子树的最小值或者左子树的最大值去代替删除节点。
2、将删除节点的左子树头结点（左孩子）放到删除节点的右子树的最左面节点的左孩子上，返回删除节点右孩子为新的根节点。
比如我要删除6
                           5
                         /   \
                        2     6
                       /     / \
                      1     4   8
                           /   / \
                          3   7   9
方法1：
                           5
                         /   \
                        2     7
                       /     / \
                      1     4   8
                           /     \
                          3      9

方法2：
                           5
                         /   \
                        2     8
                       /     / \
                      1     7   9
                           /
                          4
                         /
                        3

找到后返回承接的节点的值
从代码的程度来看，感觉方法2更加好理解
'''
from typing import *
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        '''
        方法1
        :param root:
        :param key:
        :return:
        '''
        if not root:
            return None
        if root.val==key:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            minRightNode=self.findminNode(root.right)
            root.val=minRightNode.val
            root.right=self.deleteNode(root.right,minRightNode.val)
        elif root.val < key: #在右子树去找
            root.right=self.deleteNode(root.right,key)
        else: #root.val>key 在左子树去找
            root.left=self.deleteNode(root.left,key)

        return root

    def findminNode(self,root):
        while root.left:
            root=root.left
        return root

    def deleteNode1(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        '''
        方法1
        :param root:
        :param key:
        :return:
        '''
        if not root:
            return None
        if root.val==key:
            if not root.left:
                return root.right
            if not root.right:
                return root.left

            root_left=root.left
            minRightNode=self.findminNode(root.right)

            minRightNode.left=root_left
            return root.right
        elif root.val < key: #在右子树去找
            root.right=self.deleteNode1(root.right,key)
        else: #root.val>key 在左子树去找
            root.left=self.deleteNode1(root.left,key)

        return root



if __name__=="__main__":
    node1=TreeNode(1)
    node2=TreeNode(2)
    node3=TreeNode(3)
    node4=TreeNode(4)
    node5=TreeNode(5)
    node6=TreeNode(6)
    node7=TreeNode(7)
    node8=TreeNode(8)
    node9=TreeNode(9)
    node5.left=node2
    node5.right=node6
    node2.left=node1
    node6.left=node4
    node6.right=node8
    node4.left=node3
    node8.left=node7
    node8.right=node9
    solution=Solution()
    def dfs(root):
        if not root:
            return
        print(root.val)
        dfs(root.left)
        dfs(root.right)

    if False:
        root=solution.deleteNode(node5, 6)
        dfs(root)
    if True:
        root=solution.deleteNode1(node5, 6)
        dfs(root)



