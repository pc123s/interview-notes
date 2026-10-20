'''
给你一个按照非递减顺序排列的整数数组 nums，和一个目标值 target。请你找出给定目标值在数组中的开始位置和结束位置。
如果数组中不存在目标值 target，返回 [-1, -1]。
你必须设计并实现时间复杂度为 O(log n) 的算法解决此问题。

示例 1：

输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]
示例 2：

输入：nums = [5,7,7,8,8,10], target = 6
输出：[-1,-1]
示例 3：

输入：nums = [], target = 0
输出：[-1,-1]

log(n)的复杂度
做法一样，还是采用二分查找，只不过找到以后向前和向后搜索一下

'''

from typing import *


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        if not nums:
            return [-1,-1]
        n=len(nums)
        l,r=0,n-1
        while l<=r:
            mid=l+(r-l)//2
            if nums[mid]==target:
                l,r=mid,mid
                while l>=0 and nums[l]==target:
                    l-=1
                while r<n and nums[r]==target:
                    r+=1
                return [l+1,r-1]
            elif nums[mid]>target:
                r=mid-1
            else:
                l=mid+1
        return [l,r]
if __name__=="__main__":
    s=Solution()
    l=s.searchRange([1,2,3,3,4,5],3)
    print(l)
    l=s.searchRange([1],1)
    print(l)
