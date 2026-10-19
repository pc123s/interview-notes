'''
给你一个整数数组 nums ，其中元素已经按 升序 排列，请你将其转换为一棵平衡二叉搜索树。
输入：nums = [-10,-3,0,5,9]
输出：[0,-3,9,-10,null,5]
解释：[0,-10,5,null,-3,null,9] 也将被视为正确答案：


输入：nums = [1,3]
输出：[3,1]
解释：[1,null,3] 和 [3,1] 都是高度平衡二叉搜索树。

二叉搜索树是左子树都小于根节点，右子树大于根节点。

思路：二分+递归
因为数组是顺序的，所以每次选中间的数组值作为根节点是最好的。然后分别将数组分为左右两个部分去找值，左边的为左子树，右边的为右子树。

[-10,-3,0,5,9]
1、二分查找，找到0，对左右分别继续进行二分查找。
左边二分中间值 -10 右边二分中间值5 则0.left=-10 0.right=5

继续重复上面的操作
'''
from typing import *
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None
        if len(nums)==1:
            return TreeNode(nums[0])
        # 大于2
        preNode=TreeNode(-1)
        preNodeCopy=preNode
        def dfs(nums,l,r,preNode,is_left=False):
            if l>r:
                return
            print(l,r)
            mid=l+(r-l)//2
            cNode=TreeNode(nums[mid])
            if is_left:
                preNode.left=cNode
            else:
                preNode.right=cNode
            preNode=cNode
            dfs(nums,l,mid-1,preNode,is_left=True)
            dfs(nums,mid+1,r,preNode,is_left=False)
        dfs(nums,0,len(nums)-1,preNode,is_left=True)
        return preNodeCopy.left

    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root == None:
            return

        def dfs(root):
            if root == None:
                return None
            print(root.val)
            dfs(root.left)
            dfs(root.right)

        dfs(root)
if __name__=="__main__":
    soluion=Solution()
    root=soluion.sortedArrayToBST([1,2,3,4,5,6,7])
    print(root)

    soluion.preorderTraversal(root)
