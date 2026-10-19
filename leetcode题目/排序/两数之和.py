'''
两数之和

给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。

你可以按任意顺序返回答案。

示例 1：

输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
示例 2：

输入：nums = [3,2,4], target = 6
输出：[1,2]
示例 3：

输入：nums = [3,3], target = 6
输出：[0,1]

方法1：暴力法
双指针 遍历即可 ，这种不写了

方法2：利用同样的 list存储排序后的数据的位置index,左右指针指向ranklist，  向中间移动即可
这样的好处是可以用O(n)的时间复杂度和O(n)的空间复杂度解决这个问题。

'''
from typing import *

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        if not nums:
            return []
        #nums.sort()

        rankList=sorted(enumerate(nums),key=lambda k:k[1])
        n=len(nums)
        print(rankList)
        left,right=0,n-1
        while left!=right:
            seta,setb=rankList[left],rankList[right]
            val1,val2=seta[1],setb[1]
            rank1,rank2=seta[0],setb[0]
            if val1+val2>target:
                right-=1
            elif val1+val2<target:
                left+=1
            else: #找到目标值
                return [rank1,rank2]
    def twoSum1(self,nums:List[int],target:int):
        if not nums:
            return []
        rankList=sorted(enumerate(nums),key=lambda x:x[1])
        n=len(nums)
        #print(rankList)
        left,right=0,n-1
        while left!=right:
            a=rankList[left][1]
            b=rankList[right][1]
            index1=rankList[left][0]
            index2=rankList[right][0]
            if a+b==target:
                return [index1,index2]
            elif a+b>target:
                right-=1
            else:
                left+=1
if __name__=="__main__":
    solution=Solution()
    nums = [2, 7, 11, 15]
    target = 9
    res=solution.twoSum1(nums,target)
    print(res)
    nums = [3, 2, 4]
    target = 6
    res=solution.twoSum1(nums,target)
    print(res)
    nums = [3, 3]
    target = 6
    res=solution.twoSum1(nums,target)
    print(res)
