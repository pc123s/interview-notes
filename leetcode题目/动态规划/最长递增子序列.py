'''
给你一个整数数组 nums ，找到其中最长严格递增子序列的长度。

子序列 是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，[3,6,2,7] 是数组 [0,3,1,6,2,2,7] 的
子序列。

示例 1：

输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。
示例 2：

输入：nums = [0,1,0,3,2,3]
输出：4
示例 3：

输入：nums = [7,7,7,7,7,7,7]
输出：1

方法：动态规划
dp[i] 表示以 i结尾的最长递增子序列
从i-1到i的转移方程可以表示为：
当nums[i]>nums[j] m_j=递增序列长度为dp[j]+1,j从0,i
其中最大的m_j就是dp[i]的值

'''
from typing import *
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        n=len(nums)
        dp=[0]*(n)
        dp[0]=1
        #print(dp)
        for i in range(1,n):
            max_len=1
            for j in range(i):
                if nums[i]>nums[j]:
                    c_max_len=dp[j]+1
                    if c_max_len>max_len:
                        max_len=c_max_len
            #print(i)

            #print(dp)
            dp[i]=max_len
        return dp[i]

if __name__=="__main__":
    solution=Solution()
    if True:
        nums=[10, 9, 2, 5, 3, 7, 101, 18]
        res=solution.lengthOfLIS(nums)
        print(res)
    if True:
        nums=[0,1,0,3,2,3]
        res = solution.lengthOfLIS(nums)
        print(res)
    if True:
        nums=[7,7,7,7,7,7,7]
        res = solution.lengthOfLIS(nums)
        print(res)
