'''
给两个整数数组 nums1 和 nums2 ，返回 两个数组中 公共的 、长度最长的子数组的长度 。

示例 1：

输入：nums1 = [1,2,3,2,1], nums2 = [3,2,1,4,7]
输出：3
解释：长度最长的公共子数组是 [3,2,1] 。
示例 2：

输入：nums1 = [0,0,0,0,0], nums2 = [0,0,0,0,0]
输出：5
暴力法：
双指针法
a= [ 1 2 3 2 1 ]
     i
b=[ 3  2 1 4 7]
    j
i 从 0开始,每次遍历k个字符,k从0-len(a)
1
3 2 1 4 7
2
3 2 1 4 7
...
12
32 21 14 47
23
32 21 14 47
...
123
321 214 417
...
方法2动态规划
https://leetcode.cn/problems/maximum-length-of-repeated-subarray/solutions/310917/yi-zhang-biao-ba-ju-hua-kan-dong-dong-tai-gui-hua-/?utm_source=LCUS&utm_medium=ip_redirect&utm_campaign=transfer2china
a= [ 1 2 3 2 1 ]
     i
b=[ 3  2 1 4 7]
    j
找相同的数字其实就是表格中的相等的数字连接到的左上到右下的线
    1   2   3   2   1
3           1
2      1        1
1   1               1
4
7
方法就是左上的数子+1
    1   2   3   2   1
3   0   0   1   0   0
2   0   1   0   2   0
1   1   0   0   0   3
4   0   0   0   0   0
7   0   0   0   0   0
dp[i+1][j+1]=dp[i][j]+1 if i==j
dp[i+1][j+1]=0 if i!=j

'''
from typing import *
class Solution:
    def findLength(self, nums1: List[int], nums2: List[int]) -> int:
        '''
        方法1：暴力法
        :param nums1:
        :param nums2:
        :return:
        '''
        m=len(nums1)
        n=len(nums2)
        k_=max(m,n)
        res=[] #记录结果
        for k in range(k_+1):
            for i in range(m):
                for j in range(n):
                    if i+k>m or j+k>n:
                        continue
                    a=nums1[i:i+k]
                    b=nums2[j:j+k]
                    if a and a==b :
                        res.append(a)
        arr=[] #记录最长的子数组
        print(res)
        for l_ in res:
            if len(l_)>len(arr):
                arr=l_
        return arr
    def findLength1(self, nums1: List[int], nums2: List[int]) -> int:
        m=len(nums1)
        n=len(nums2)
        dp=[[0]*(n+1) for i in range(m+1)]
        max_len=0
        a=0 #记录i和j的位置
        b=0

        for i in range(1,m+1):
            for j in range(1,n+1):
                if nums1[i-1]==nums2[j-1]:
                    dp[i][j]=dp[i-1][j-1]+1
                else:
                    dp[i][j]=0
                if dp[i][j]>max_len:
                    max_len=dp[i][j]
                    a,b=i,j
        #print(nums1[a-max_len:a])
        return max_len
if __name__=="__main__":
    solution=Solution()
    if True:
        nums1=[1,2,3,2,1]
        nums2=[3,2,1,4,7]
        arr=solution.findLength1(nums1,nums2)
        print(arr)
    if True:
        nums1=[0,0,0,0,0]
        nums2=[0,0,0,0,0]
        arr=solution.findLength1(nums1,nums2)
        print(arr)
    if True:
        nums1=[1,2,3,2,1,2,2,3]
        nums2=[3,2,1,2,4]
        arr=solution.findLength1(nums1,nums2)
        print(arr)
