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

其实这个还是找旋转数组的旋转点
[3 , 4 , 5, 1 ,2]
 l       m     r
 m>r->l=m+1
[8, 9 , 1, 2 ,3,4,5]
 l         m       r
nums[r]==nums[m]
[3, 3 , 1, 2 ,3,3,3]
 l            m   r
[3, 3 , 1, 2 ,3,3,3]
 l  m             r


'''
from  typing import *
import math
class Solution:
    def minNumberInRotateArray(self , nums: List[int]) -> int:
        l,r=0,len(nums)-1
        while l<=r:
            mid=l+(r-l)//2
            if nums[mid]>nums[r]:
                l=mid+1
            elif nums[mid]<nums[r]:
                r=mid
            else: # 当nums[mid]==nums[r]时，无法确定是否要向左缩圈，只能确认最小值在r左边
                r=mid-1

        return l
if __name__=="__main__":
    solution=Solution()
    res=solution.minNumberInRotateArray([3,4,5,1,2])
    print(res)
    res=solution.minNumberInRotateArray([3,4,0,1,2])
    print(res)
    res=solution.minNumberInRotateArray([3,4,5,6,7,8,0,1,2])
    print(res)
    res=solution.minNumberInRotateArray([3,4,5,6,7,0,1,2])
    print(res)
    res=solution.minNumberInRotateArray([3,4,5,6,7,0,1,2,3])
    print(res)
    res=solution.minNumberInRotateArray([3,4,5,6,7,0,1,2,3,4])
    print(res)
    res=solution.minNumberInRotateArray([3,4,5,6,7,0,1,2,3,4,5])
    print(res)
    res=solution.minNumberInRotateArray([3,3,200,300,300,0,1,2,3])
    print(res)