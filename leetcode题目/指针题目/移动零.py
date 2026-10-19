'''
移动零
给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。

请注意 ，必须在不复制数组的情况下原地对数组进行操作。

示例 1:

输入: nums = [0,1,0,3,12]
输出: [1,3,12,0,0]
示例 2:

输入: nums = [0]
输出: [0]

题解：采用双指针，i指向初始位置，j指向非零元素，发现非0元素，则将其移动至i的位置，
循环完成后i指向最后一个非零元素
2、从i开始，将后面的元素变为0
i指向第一个非0的位置，j在i后面
0,1,0,3,12
i
 j
nums[j]!=0 nums[i]=nums[j]
i+=1
j+=1
1,1,0,3,12
  i
   j
nums[j]==0 j+=1
1,1,0,3,12
  i
      j
nums[j]!=0 nums[i]=nums[j]
i+=1
j+=1
1,3,0,3,12
    i
        j
nums[j]!=0 nums[i]=nums[j]
i+=1
j+=1
1,3,12,3,12
    i
            j
j打破循环，i-n全为0
'''
from typing import *
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n=len(nums)
        i=0
        while i<n:
            if nums[i]==0:
                break
            i+=1
        for j in range(i+1,n):
            if nums[j]!=0:
                nums[i]=nums[j]
                i+=1
        if i!=n:# 如果i==n代表数组没有0
            for z in range(i,n):
                nums[z]=0
        print(nums)
    def moveZeroes1(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n=len(nums)
        i=0
        while i<n and nums[i]!=0:
            i+=1
        #print(i)
        #exit()
        # 此时i指向0的位置，j指向后面非0位置
        for j in range(i+1,n):
            if nums[j]!=0:
                nums[i]=nums[j]
                i+=1
        if i!=n:
            for z in range(i,n):
                nums[z]=0
        return nums

if __name__=="__main__":
    solution=Solution()
    if True:
        nums=[0,1,0,3,12]
        res=solution.moveZeroes1(nums)
        print(res)
    if True:
        nums = [1]
        res=solution.moveZeroes1(nums)
        print(res)
    if True:
        nums = [0,1]
        res=solution.moveZeroes1(nums)
        print(res)
        #print(res)
        #exit()
