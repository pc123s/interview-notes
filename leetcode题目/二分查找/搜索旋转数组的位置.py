'''
在传递给函数之前，nums 在预先未知的某个下标 k（0 <= k < nums.length）上进行了 旋转，使数组变为 [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]（下标 从 0 开始 计数）。例如，
[0,1,2,4,5,6,7] 在下标 3 处经旋转后可能变为 [4,5,6,7,0,1,2] 。

给你 旋转后 的数组 nums 和一个整数 target ，如果 nums 中存在这个目标值 target ，则返回它的下标，否则返回 -1 。

你必须设计一个时间复杂度为 O(log n) 的算法解决此问题。

示例 1：
输入：nums = [4,5,6,7,0,1,2], target = 0
输出：4
示例 2：

输入：nums = [4,5,6,7,0,1,2], target = 3
输出：-1
示例 3：

输入：nums = [1], target = 0
输出：-1

思路1：先找到旋转数组的位置，再确定范围，分别在两个范围内查找
例1：
例2： 2 3 4 5 6 7 1
     l     m     r
if num[m]<num[l]:
    说明 旋转数组的位置在(l,m]之间,令r=m
else:
    #nums[m]>nums[l]
    if nums[m+1]<nums[r] 找到了
    if num[m]>=num[r]
        旋转的位置一定在[m,r),l=m


例2 target=1
4 5 6 7 0 1 2
二分的中间值是7

先找断点
4 5 6 7 8  9 10 0 1 2 3
l                     r
          mid
l=mid+1
4 5 6 7 8  9 10 0 1 2 3
             l        r
                 mid
nums[mid]<nums[r]
num[mid]<nums[l]
r=mid-1

4 5 6 7 8  9 10 0 1 2 3
             l  r
            mid
mid=l+(r-l)//0
nums[l]<=nums[mid]
nums[r]>=nums[mid+1]

方法1：利用二分查找先找中间的数，找到后再在左边或者右边进行二分查找
[4  5 6 1 2 3]
l指向旋转数组的左边区域 r指向旋转数组的右边区域
中间值一定满足 nums[mid]>=nums[l]
nums[mid]<nums[r]  r一定在右边区域
'''
import math
from typing import *
class Solution:

    import math
    def searRevertIndex(self,arr):
        '''
        l+(r-l)//2 更倾向于在左边去找数
        :param arr:
        :return:
        '''
        n = len(arr)
        l, r = 0, n - 1
        while l <= r:

            mid = l + (r - l) // 2
            if arr[mid] > arr[r]:
                l = mid + 1
            elif arr[mid] < arr[r]:
                r = mid
            else:
                # 其实当nums[mid]==nums[r] 时，此时旋转数组的值不是l就是r,可以直接返回
                #print(l, r)
                r -= 1
        return l
        #self.searRevertIndex()

    def half_find(self,nums,l,r,target):
        while l<=r:
            mid=l+(r-l)//2
            #print(mid,l,r)
            if nums[mid]>target:
                r=mid-1
            elif nums[mid]==target:
                return mid
            else:
                l=mid+1
        return -1
    def search(self, nums: List[int], target: int) -> int:
        if not nums:
            return -1
        if len(nums)==1:
            if nums[0]==target:
                return 0
            else:
                return -1
        r=len(nums)-1
        Index=self.searchReverseIndex(nums)
        print(Index)
        if nums[0]<=target and nums[Index]>=target:
            return self.half_find(nums,0,Index,target)
        elif nums[Index+1]<=target and nums[r]>=target:
            return self.half_find(nums,Index+1,r,target)
        else:
            return -1


if __name__=="__main__":
    solution=Solution()
    if False:
        index=solution.search_pc([4,5,6,7,0,1,2,3],0)
        print(index)
    if False:
        index = solution.search_pc([8,9,2,3,4], 9)
        print(index)

    if False:
        index=solution.half_find([1,2,3,4,5,6,7],0)
        print(index)
    if True:
        index=solution.searRevertIndex([4,5,1,2,3])
        print(index)
        index=solution.searRevertIndex([4,5,6,1,2,3])
        print(index)
        index=solution.searRevertIndex([4,5,6,7,0,1,2])
        print(index)
        index=solution.searRevertIndex([2,1])
        print(index)
