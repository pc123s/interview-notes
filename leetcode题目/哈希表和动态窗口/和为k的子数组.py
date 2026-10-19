'''
给你一个整数数组 nums 和一个整数 k ，请你统计并返回 该数组中和为 k 的子数组的个数 。
子数组是数组中元素的连续非空序列。

示例 1：
输入：nums = [1,1,1], k = 2
输出：2

示例 2：
输入：nums = [1,2,3], k = 3
输出：2

思路，采用hash表的方式求解
pre[i]=s[i+1]为 [0,i]的前缀和
则子数组就有 pre[i]-pre[j]=k 为区间[j,i]的数组满足 连续数组和为k
以 nums=[1,1,−1,1,−1],为例，其前缀和 s=[0,1,2,1,2,1] k=1 为 例
j s[j]  s[j]-k 子数组个数
0   0     -1      0
1   1      0      1(s[0])
2   2      1      1(s[1])
3   1      0      1(s[0])
4   2      1      2(s[1],s[3])
5   1      0      1(s[0])

链接：https://leetcode.cn/problems/subarray-sum-equals-k/solutions/2781031/qian-zhui-he-ha-xi-biao-cong-liang-ci-bi-4mwr/
'''
from typing import *
from collections import defaultdict
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        n=len(nums)
        s=[0]*(n+1) #前缀和
        sum=0
        for idx,num in enumerate(nums):
            sum+=num
            s[idx+1]=sum
        '''
        使用dic记录前缀和为 num的值索引
        '''
        #dic={}
        dic=defaultdict(list)
        res=0
        res_arr=[]
        for i in range(n+1):
            s_j=s[i]-k
            l=dic[s_j]
            res+=len(l)
            if l!=[]:
                for j in l:
                    res_arr.append(nums[j:i])
            dic[s[i]].append(i)
            #print(dic)
        print(res_arr)
        return res

    def subarraySum1(self, nums: List[int], k: int) -> int:
        #首先计算一个前缀和
        n=len(nums)
        s=[0]*(n+1)
        '''
        [1,1,-1,1,-1]
        前缀和为 s[i+1]=nums[0:i]的和包括j
        则有s[j]-s[i]为区间为nums[i:j]的区间和
        s=[0,1,2,1,2,1]
        '''
        sum=0

        for i in range(n):
            sum+=nums[i]
            s[i+1]=sum
        dic=defaultdict(list)
        res=0 #记录有多少个子数组和
        arr=[]
        for i in range(0,n+1):
            s_j=s[i]-k
            if s_j in dic:
                res+=len(dic[s_j])
                j_l=dic[s_j]
                for j in j_l:
                    arr.append(nums[j:i])

            dic[s[i]].append(i)
        print(arr)
        print(dic)
        return arr


if __name__=="__main__":
    solution=Solution()
    if True:
        nums=[1,1,-1,1,-1]
        res=solution.subarraySum1(nums,1)
        print(res)
    if True:
        nums=[1,1,1]
        res=solution.subarraySum1(nums,2)
        print(res)
    if True:
        nums=[1,2,3]
        res=solution.subarraySum1(nums,3)
        print(res)
