'''
给你一个整数数组 nums，找到峰值元素并返回其索引。数组可能包含多个峰值，在这种情况下，返回 任何一个峰值 所在位置即可。

你可以假设 nums[-1] = nums[n] = -∞ 。

你必须实现时间复杂度为 O(log n) 的算法来解决此问题。



示例 1：

输入：nums = [1,2,3,1]
输出：2
解释：3 是峰值元素，你的函数应该返回其索引 2。
示例 2：

输入：nums = [1,2,1,3,5,6,4]
输出：1 或 5
解释：你的函数可以返回索引 1，其峰值元素为 2；
     或者返回索引 5， 其峰值元素为 6。
1 <= nums.length <= 1000
-231 <= nums[i] <= 231 - 1
对于所有有效的 i 都有 nums[i] != nums[i + 1]


有log(n)那么要使用二分查找的方式进行，我们知道二分查找一般都要在顺序数列中，这个是非顺序的
方法1：
首先想到的是遍历法，如果i满足nums[i]>nums[i-1]且 nums[i]<nums[i+1]那么i就是峰值
只需要不断移动i指针的位置即可

方法2：
二分查找。
首先确定l,r边界值，确定中间值mid,
我们发现mid mid+1 mid-1三个值，
如果满足上面的条件，则输出mid否则
比较mid和mid+1
如果nums[mid+1]>nums[mid] 那么说明，峰值在右边
在右区间查找
否则在左区间查找

'''
from typing import *
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        if len(nums)==1:
            return 0
        if len(nums)==2:
            return nums.index(max(nums))
        l,r=0,len(nums)-1
        #采用二分查找
        while l<=r:
            mid=l+(r-l)//2
            if mid==0 and nums[mid]>nums[mid+1]:
                return mid
            if mid==len(nums)-1 and nums[mid]>nums[mid-1]:
                return mid
            if nums[mid-1]<nums[mid] and nums[mid]>nums[mid+1]:
                return mid
            elif nums[mid]<nums[mid+1]:
                l=mid+1
            elif nums[mid]>nums[mid+1]:
                r=mid-1
    def findPeakElement1(self,nums:List[int])-> int:
        '''
        采用二分法进行查找，
        如果l,r mid 比较mid和mid+1的值
        如果 nums[mid]>nums[mid+1] 那么值在 [l,mid]之间
        如果 nums[mid]<nums[mid+1] 那麽值在[mid+1,r]之間

        :param nums:
        :return:
        '''
        if len(nums)==1:
            return nums[0]
        if len(nums)==2:
            return nums.index(max(nums))
        l,r=0,len(nums)-1
        while l<=r:
            mid=l+(r-l)//2
            if nums[mid]>nums[mid-1] and nums[mid]>nums[mid+1]:
                return mid
            elif nums[mid]>nums[mid+1]:
                r=mid
            elif nums[mid]<nums[mid+1]:
                l=mid+1
            elif mid==0 and nums[mid]>nums[mid+1]:
                return mid
            elif mid==len(nums)-1 and nums[mid]>nums[mid-1]:
                return mid



if __name__=="__main__":
    solution=Solution()
    if False:
        index=solution.findPeakElement([1,2,3,1])
        print(index)
        index=solution.findPeakElement([1,2,1,3,5,6,4])
        print(index)
    if True:
        index=solution.findPeakElement([3,1,2])
        print(index)
    if True:
        index=solution.findPeakElement([6,5,4,3,2,3,2])
        print(index)