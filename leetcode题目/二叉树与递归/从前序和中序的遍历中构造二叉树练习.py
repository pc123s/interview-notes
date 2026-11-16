'''
https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/solutions/2646359/tu-jie-cong-on2-dao-onpythonjavacgojsrus-aob8/

给定两个整数数组 preorder 和 inorder ，其中 preorder 是二叉树的先序遍历， inorder 是同一棵树的中序遍历，请构造二叉树并返回其根节点。
示例 1:
输入: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
输出: [3,9,20,null,null,15,7]
示例 2:
输入: preorder = [-1], inorder = [-1]
输出: [-1]

思路：
          3
         / \
        9  20
          /  \
         15   7
3 9 20 15 7
9 3 15 20 7
           5
         /   \
        4     8
       /     / \
      11    13  4
     /  \      / \
    7    2    5   1
前序：5 4 11 7 2 8 13 4 5 1
中序：7 11 2 4 5 13 8 5 4 1
我们发现，前序中的节点往往都是根节点， 而对应在中序的这个节点，能够将数据分为左右两个子树
同样这道题需要采用递归进行求解。
利用前序遍历的顺序，对中序遍历进行二分切割，不断切割直到 子数集只有一个元素代表已经切割完成
比如
前序为5()  中序搜索5 left=[7,11,2,4] right=[13,8,5,4,1]
left:前序为4(prelist的第一个) 在左边区域 left_1=[7,11,2] right_1=[] return None
left_1:前序为11(prelist的第一个) 左边为[7] 右边为[2]

right:前序为8（5对应的中序的list的index的前序位置+1 ） 左边搜索 left_2=[13] right_2=[5,4,1]
right_2:前序为4(8对应的中序list的index+1所在的前序位置的数) 左边搜索 left_2=[13] right_2=[5,4,1]

当[]为空或者为1的时候返回 None或者TreeNode
11.left=7
11.right=2
return 11
继续递归
4.left=11
4.right=N

方法2:
方法更适用于二叉树是惟一的情况
第二个方法采用插入的方法，其中采用hash表的方式来优化搜索的步骤，但是前提是这个二叉树中的值是唯一的。
3 9 20 15 7
9 3 15 20 7
root=3
9 9的位置比3小，3的左边 3.left=9
20 20的位置比3大，3的右边，3.right=20
15 15的位置比 3大，3的右边  右边有值，则root=20  15比20小 在15在20的左边 20.left=15
7 7的位置比3大，3的右边， 右边有值，则root=20, 7比20大，7在20的右边


'''
from typing import *
import copy
from  collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def tree_to_list(self, root: Optional[TreeNode]) -> List[Optional[int]]:
        if not root:
            return []
        q=deque([])
        q.append(root)
        res = []
        while q:
            node=q.popleft()
            if node:
                res.append(node.val)
                q.append(node.left)
                q.append(node.right)
            else:
                res.append(None)
        '''
            3
           / \
          9  20
             / \
            15  7
        后面这一步就是为了把最后的几个None去掉
        [3, 9, 20, None, None, 15, 7, None, None, None, None]
        '''
        while res and res[-1] is None:
            res.pop()
        return res

    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder:
            return None
        # 只有一个元素
        if len(preorder)==1:
            return TreeNode(preorder[0])

        def buildTree_dfs(preorder,inorder):
            if not inorder:
                return None
            a=preorder[0]
            mid=inorder.index(a)
            left_area=inorder[:mid]
            right_area=inorder[mid+1:]
            left_node=buildTree_dfs(preorder[1:mid+1],left_area)
            right_node=buildTree_dfs(preorder[mid+1:],right_area)
            return TreeNode(a,left_node,right_node)
        root=buildTree_dfs(preorder,inorder)
        return root

if __name__=='__main__':
    prel=[5,4,11,7,2,8,13,4,5,1]
    inl=[7,11,2,4,5,13,8,5,4,1]
    solution=Solution()
    node=solution.buildTree(prel,inl)
    print(node)
    res=solution.tree_to_list(node)
    print(res)

