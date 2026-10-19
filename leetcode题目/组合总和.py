'''
给你一个 无重复元素 的整数数组 candidates 和一个目标整数 target ，
找出 candidates 中可以使数字和为目标数 target 的 所有 不同组合 ，并以列表形式返回。你可以按 任意顺序 返回这些组合。
candidates 中的 同一个 数字可以 无限制重复被选取 。如果至少一个数字的被选数量不同，则两种组合是不同的。
对于给定的输入，保证和为 target 的不同组合数少于 150 个。

示例 1：

输入：candidates = [2,3,6,7], target = 7
输出：[[2,2,3],[7]]
解释：
2 和 3 可以形成一组候选，2 + 2 + 3 = 7 。注意 2 可以使用多次。
7 也是一个候选， 7 = 7 。
仅有这两种组合。

示例 2：

输入: candidates = [2,3,5], target = 8
输出: [[2,2,2,2],[2,3,3],[3,5]]
示例 3：

输入: candidates = [2], target = 1
输出: []
'''
'''
思路1：
采用遍历+树的做法  2->[2,3,5]->[2,3,5] 一旦发现最左侧的树枝大于target停止
2->[3,5]->[3,5]
整体思路其实就是遍历和树
'''
from typing import *
class Solution:
    def __init__(self):
        self.arr=[] #记录最终的结果
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        self.arr=[]
        for i in range(len(candidates)):
            num=candidates[i]
            self.grow_tree([num],candidates[i:],num,target)
        return self.arr
    def grow_tree(self,root,lst,total_sum, max_sum):
        """
        对列表进行遍历的树生长
        root: 根节点
        lst: 叶子节点
        total_sum: 当前路径的总和
        max_sum: 最大允许的路径和
        """
        if total_sum >= max_sum:  # 如果当前路径的总和超过最大允许的路径和，退出递归
            if  total_sum==max_sum :
                self.arr.append(root)
            return
        #print(root + lst)  # 打印当前路径
        for i in range(len(lst)):  # 对每个叶子节点进行遍历
            self.grow_tree(root + [lst[i]], lst[i:], total_sum + lst[i], max_sum)  # 对子树进行递归生长


solution=Solution()
print(solution.combinationSum([2,3,5],8))
print(solution.combinationSum([2],1))
print(solution.combinationSum([2,3,6,7],7))
# solution.grow_tree([3],[1,2,3],3,8)
# print(solution.arr)

# 示例：

