'''
有一个长度为 n 的非降序数组，比如[1,2,3,4,5]，将它进行旋转，即把一个数组最开始的若干个元素搬到数组的末尾，变成一个旋转数组，比如变成了[3,4,5,1,2]，或者[4,5,1,2,3]这样的。请问，给定这样一个旋转数组，求数组中的最小值。
数据范围：
时间复杂度 O(logn)

示例1
输入：
[3,4,5,1,2]
返回值：
1

示例2
输入：
[3,100,200,3]
返回值：
3
旋转数组反转仍然会有两个有序数组， array1 array2
3 4 5    1 2 并且array1的值始终大于array2
旋转点为array1的尾点(这个就错了)

'''
from  typing import *
import math
class Solution:
    def minNumberInRotateArray(self , nums: List[int]) -> int:
        '''
        收缩区间法
        取中点
        l,r=0,n-1  m=l+(r-l)//2
        if nums[m]>nums[r] m一定在array1 旋转点在[m,r]
        elif nums[m]<nums[r] m在array2,旋转点在[l,m]
        else: nums[m]==nums[r]  此时不确定旋转点的位置，收缩右区间
        这种方法思路的话，旋转点必须是array2数组的第一个，否则会有相应的bug
        :param nums:
        :return:
        '''
        n=len(nums)
        l,r=0,n-1
        while l<=r:
            #mid=l+(r-l)//2
            mid=l+math.ceil((r-l)/2)
            if nums[mid]>nums[r]:
                l=mid
            # 这个解法有个很大的漏洞 nums[mid]<nums[r],mid和r可能在同一个数组中，
            elif nums[mid]<nums[r]:
                if r==n-1:
                    r=mid-1
                else:
                    r=mid
            else:
                r-=1
        return l
    def minNumberInRotateArray1(self , nums: List[int]) -> int:
        '''
        :param nums:
        :return:
        '''
        n=len(nums)
        l,r=0,n-1
        while l<=r:

            mid=l+(r-l)//2
            if nums[mid]>nums[r]:
                l=mid+1
            elif nums[mid]<nums[r]:
                r=mid
            else:
                # 其实当nums[mid]==nums[r] 时，此时旋转数组的值不是l就是r,可以直接返回
                print(l,r)
                r-=1
        return nums[l]


if __name__=='__main__':
    solution=Solution()
    res=solution.minNumberInRotateArray1([3,4,0,1,2])
    print(res)
    res=solution.minNumberInRotateArray1([3,4,5,6,7,8,0,1,2])
    print(res)
    res=solution.minNumberInRotateArray1([3,4,5,6,7,0,1,2])
    print(res)
    res=solution.minNumberInRotateArray1([3,4,5,6,7,0,1,2,3])
    print(res)
    res=solution.minNumberInRotateArray1([3,4,5,6,7,0,1,2,3,4])
    print(res)
    res=solution.minNumberInRotateArray1([3,4,5,6,7,0,1,2,3,4,5])
    print(res)