'''
给你一个按 非递减顺序 排序的整数数组 nums，返回 每个数字的平方 组成的新数组，要求也按 非递减顺序 排序。



示例 1：

输入：nums = [-4,-1,0,3,10]
输出：[0,1,9,16,100]
解释：平方后，数组变为 [16,1,0,9,100]
排序后，数组变为 [0,1,9,16,100]
示例 2：

输入：nums = [-7,-3,2,3,11]
输出：[4,9,9,49,121]


请你设计时间复杂度为 O(n) 的算法解决本问题

方法1：
其实这个排序问题中的关键在于其中可能有负数，因为正数的平方仍然是升序的，如果采用常规的排序算法，那么时间复杂都肯定是O(n*log(n))

方法2：
采用指针标记法，由于数组是顺序的，这代表  如果是正数，平方后一定是顺序的，如果是负数，平方后是逆序的


设置a，b两个个指针，分别指向正数和负数开始的位置,采用一个空间记录上述的绝对值的，正数较小插入并右移动，负数较小，插入左移动，0-n的边界值

[-7  -3  2  3  11]
     a   b


'''
from typing import *

class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        if not nums:
            return nums
        n=len(nums)
        #先做一遍循环找到a.b
        a,b=-1,-1 #初始值-1
        for i in range(n-1):
            if nums[i]<0 and nums[i+1]>=0:
                a=i
        if a==-1:# 全是正数和负数
            if nums[a]<0:
                return [i**2 for i in nums][::-1]
            else: #全是正数
                return [i**2 for i in nums]
        #print(a)
        # a不为0找到了分界点
        arr=[] #arr记录数值
        b=a+1
        while a>-1 and b<n:
            if abs(nums[a])>abs(nums[b]):
                arr.append(nums[b]**2)
                b+=1
            else:
                arr.append(nums[a]**2)
                a-=1
        #print(a,b)
        if a>-1:
            while a>-1:
                arr.append(nums[a]**2)
                a-=1
        #print(arr)
        if b<n:
            while b<n:
                arr.append(nums[b]**2)
                b+=1
        return arr


if __name__=="__main__":
    solution=Solution()
    arr=solution.sortedSquares([-7,-3,2,3,11])
    print(arr)


