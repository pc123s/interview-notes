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

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def dfs(self,root):
        if not root :
            return root
        print(root.val)
        self.dfs(root.left)
        self.dfs(root.right)
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
            index=inorder.index(a)

            left_area=inorder[:index]
            right_area=inorder[index+1:]
            left=buildTree_dfs(preorder[1:1+index],left_area)
            right=buildTree_dfs(preorder[1+index:],right_area)
            return TreeNode(a,left,right)
        node=buildTree_dfs(preorder,inorder,map)
        return node

    def buildTree1(self, preorder: List[int], inorder: List[int]) -> TreeNode:

        # 题目中说 preorder 和 inorder 均无重复元素
        # 通过哈希表把中序遍历序列中的值和顺序建立映射关系
        # 通过 for 循环，遍历完中序遍历序列中的所有元素
        map = dict()

        for i in range(len(inorder)):
            # 以中序序列中的元素值 inorder[i] 作为 key
            # 以位置 i 作为 value
            # 存放到哈希表中
            # 比如中序遍历序列中的元素是 [   A  ,   D  ,   E  ,   F  ,   G  ,   H  ,   M  ,   Z  ]
            # 那么这个哈希表就是以下的样子
            # | 索引 | 位置  |
            # | A | 0  |
            # | D | 1  |
            # | E | 2  |
            # | F | 3  |
            # | G | 4  |
            # | H | 5  |
            # | M | 6  |
            # | Z | 7  |
            map[inorder[i]] = i

        # 下面开始构建二叉树
        # 把前序遍历序列中的第一个元素 preorder[0] 作为二叉树的根节点
        # 因为任意二叉树的前序遍历序列中的第一个元素，一定是二叉树的根节点
        root = TreeNode(preorder[0])

        # 继续遍历前序遍历序列中的其它元素
        for i in range(1, len(preorder)):
            # 把当前遍历的元素构造为一个二叉树的节点
            node = TreeNode(preorder[i])

            # 把构造的节点插入到以 root 为根节点的二叉树中
            self.insertNode(root, node, map)

        # 当 preorder 中所有元素都构造并且插入完毕之后
        # 二叉树就完成了构建
        return root

        # root : 二叉树的根节点
        # node : 待插入的节点

    def insertNode(self, root: TreeNode, node: TreeNode, map: dict):
        # 当 root 和 node 指向的节点相同时，跳出循环
        while root != node:

            # 如果 node 的中序遍历序列位置小于 root 的中序遍历序列位置
            # 说明 node 应该在 root 的左子树中
            if map[node.val] < map[root.val]:

                # 如果此时 root 没有左子树
                if not root.left:
                    # 那么就把 node 设置为 root 的左子树
                    root.left = node

                # 1、如果之前 root 没有左子树，那么通过上面的代码，就设置好了 root 的左子树
                # 也就是说 node 是 root 的一个叶子节点，完成了插入操作
                # 把 root 指向 root.left 后，root 为 node，跳出了循环

                # 2、如果之前 root 已经有左子树，那么就不能直接把 node 插入到 root 的左子树上
                # 需要判断应该把 node 插入到 root 左子树上的孩子节点的那个位置上
                # 比如现在的 root 是这个样子，node 为 A
                #        G
                #       /
                #      D
                #     /  \
                #    ①   ②
                # root 已经有左子树 D 了，所以 node 应该考虑插入到 D 中的 ① 还是 ② 上面
                # 所以，把 root 指向 root.left ，继续遍历 root 的左子树的情况
                root = root.left


            else:

                # 如果 node 的中序遍历序列位置大于 root 的中序遍历序列位置
                # 说明 node 应该在 root 的右子树中

                # 如果此时 root 没有右子树
                if not root.right:
                    # 那么就把 node 设置为 root 的右子树
                    root.right = node

                # 把 root 指向 root.right ，继续遍历 root 的右子树的情况
                root = root.right



if __name__=="__main__":
    prel=[5,4,11,7,2,8,13,4,5,1]
    inl=[7,11,2,4,5,13,8,5,4,1]
    solution=Solution()
    node=solution.buildTree(prel,inl)
    print(node)
    solution.dfs(node)
