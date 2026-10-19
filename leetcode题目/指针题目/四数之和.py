'''
给你一个由 n 个整数组成的数组 nums ，和一个目标值 target 。请你找出并返回满足下述全部条件且不重复的四元组
[nums[a], nums[b], nums[c], nums[d]] （若两个四元组元素一一对应，则认为两个四元组重复）：
0 <= a, b, c, d < n a、b、c 和 d 互不相同，这里是指下标互不相同。 nums[a] + nums[b] + nums[c] + nums[d] == target
你可以按 任意顺序 返回答案 。 示例 1：
输入：nums = [1,0,-1,0,-2,2], target = 0 输出：[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]] 示例 2：
输入：nums = [2,2,2,2,2], target = 8 输出：[[2,2,2,2]]
'''

from typing import List
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        res=[]
        if len(nums)<4:
            return res
        nums.sort()
        n=len(nums)
        for i in range(n-3):
            if i>0 and nums[i]==nums[i-1]: #重复则跳过,向右移动只可能是左边的子集
                continue
            for j in range(i+1,n-2):
                if j>i+1 and nums[j]==nums[j-1]: #重复则跳过,向右移动只可能是前一个的子集
                    continue
                res_1=[]
                a=j+1
                b=n-1
                i_j=nums[i]+nums[j]
                while a<b: #因为a或者b移动不止一步
                    i_j_a_b=i_j+nums[a]+nums[b]
                    if i_j_a_b==target:
                        res_1=[nums[i],nums[j],nums[a],nums[b]]
                        res.append(res_1)
                        # 相等则移动左边的值,直到发现不相等的时候，打破循环
                        while nums[a+1]==nums[a]:
                            a+=1
                            if a==b:
                                break
                        a+=1
                    elif i_j_a_b<target:
                        while nums[a + 1] == nums[a]:
                            a += 1
                            if a == b:
                                break
                        a+=1
                    else:
                        while nums[b - 1] == nums[b]:
                            b -= 1
                            if a == b:
                                break
                        b-=1
        return res
solution=Solution()
print(solution.fourSum([1,0,-1,0,-2,2],0))
print(solution.fourSum([2,2,2,2,2],8))
print(solution.fourSum([-1,0,1,2,-1,-4],target=-1))
print(solution.fourSum([0,0,0,5,-3,-4,1],target=-6))
print(solution.fourSum([2,2,2,2,2],target=8))
print(solution.fourSum([1,-2,-5,-4,-3,3,3,5],target=-11))



