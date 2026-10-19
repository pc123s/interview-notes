'''
''
一个长度为 n – 1 的递增排序数组中的所有数字都是唯一的，并且每个数字都在范围 0 ～ n – 1 之内。

在范围 0 ～ n – 1 内的 n 个数字中有且只有一个数字不在该数组中，请找出这个数字。
输入: [0,1,3]
输出: 2

输入: [0,1,2,3,4,5,6,7,9]
输出: 8

方法：
https://www.bilibili.com/video/BV1HM4y137sg/?t=86&spm_id_from=333.1350.jump_directly&vd_source=2a3297d2a8d1548f7f8d80a163171480

这个采用遍历法能够很快的找出答案，但是时间复杂度为O(n)

方法2
时间复杂度O（log(n)）
空间复杂度 O(N)

nums
[ 0, 1, 2, 3, 5, 6, 7, 8, 9]
index
[0, 1, 2, 3,  4, 5, 6, 7, 8]
 l          mid           r
mid的index和value不同，l的index和value相同 r的index和value不同，说明[l,mid]的数据有问题（右闭）

nums
[ 0, 1, 2, 3, 4, 5, 7, 8, 9]
index
[0, 1, 2, 3, 4, 5, 6, 7, 8 ]
 l          mid           r
mid的index和value相同，l的index和value相同，r的index不同，说明[l,mid]都是正常的,出问题的在[mid+1,r]中
l=mid+1

nums
[ 0, 1, 2, 3, 4, 5, 6, 7, 9]

index
[0, 1, 2, 3, 4, 5, 6, 7,  8]
                l         r
                  mid
此时l没问题，r有问题，mid没问题，继续收缩l

nums
[ 0, 1, 2, 3, 4, 5, 6, 7, 9]
index
[0, 1, 2, 3, 4, 5, 6, 7,  8]
                      l   r
                     mid
此时l没问题，r有问题，l=mid+1
nums[mid]!=idx[mid] 返回index

nums=[ 1 , 2 , 4 ,5, 6, 7]
idx=[ 0 , 1 , 2 ,3, 4, 5]

'''



from typing import *
class Solution:
    def missingNumber(self,nums:List[int])->int:
        if not nums:
            return 0
        n=len(nums)
        idx=[i for i in range(n)]
        l, r = 0, n - 1
        while l<=r:
            mid=(l+r)//2
            if idx[mid]==nums[mid]:
                l=mid+1
            else:
                r=mid-1
        return l

if __name__=="__main__":
    solution=Solution()
    res=solution.missingNumber([0,1,2,4,5,6,7,8])
    print(res)
