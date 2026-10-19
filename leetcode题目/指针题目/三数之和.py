'''
给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，
同时还满足 nums[i] + nums[j] + nums[k] == 0 。请
你返回所有和为 0 且不重复的三元组。
示例 1：

输入：nums = [-1,0,1,2,-1,-4]
输出：[[-1,-1,2],[-1,0,1]]
解释：
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0 。
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0 。
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0 。
不同的三元组是 [-1,0,1] 和 [-1,-1,2] 。
注意，输出的顺序和三元组的顺序并不重要。
示例 2：

输入：nums = [0,1,1]
输出：[]
解释：唯一可能的三元组和不为 0 。
示例 3：

输入：nums = [0,0,0]
输出：[[0,0,0]]
解释：唯一可能的三元组和为 0 。
'''
'''
错误方法：
采用O(N2)
1、排序
2、在左右两边各放一个游标，中间为一个游标
3、每次移动中间游标，如果比目标值小，则右移，且保证右移后数字改变
易错思路1：a和c各占两边最小和最大，如果如果两者之和>0,则加上中间任何值都比0大，这是错误的
正确解法双指针：
设三个指针为a,b,c
固定a,b在左，c在右。
当a+b+c小于0，移b，
当a+b+c>0,左移c
找到则移动a
双指针适合 如果我们发现随着第一个元素的递增，第二个元素是递减的，那么就可以使用双指针的方法
'''
from typing import *
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n=len(nums)
        res=[]
        nums.sort()
        triger=False
        for i in range(n-2):
            a=i
            b=a+1
            c=n-1
            # 找到了移动a，发现与之前的值重复，说明这个寻找的过程是前一个的子集
            if triger==True and nums[a]==nums[a-1]:
                 continue
            while b<c:
                if nums[a]+nums[b]+nums[c]==0:
                    res.append([nums[a],nums[b],nums[c]])
                    triger= True
                    #找到了 b移动
                    while nums[b+1]==nums[b]:
                        b += 1
                        if b==c:
                            break
                    b+=1
                elif nums[a]+nums[b]+nums[c]<0:
                    b+=1
                else:
                    while nums[c-1]==nums[c]:
                        c -= 1
                        if b==c:
                            break
                    c-=1
        return res

if __name__=="__main__":
    solution=Solution()
    print(solution.threeSum([-1,0,1,2,-1,-4]))
    print(solution.threeSum([0,0,0]))
    print(solution.threeSum([0,0,0,0]))
    print(solution.threeSum([-1,0,1,2,-1,-4,-2,-3,3,0,4]))