'''
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。
每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？

示例 1：

输入：n = 2
输出：2
解释：有两种方法可以爬到楼顶。
1. 1 阶 + 1 阶
2. 2 阶
示例 2：

输入：n = 3
输出：3
解释：有三种方法可以爬到楼顶。
1. 1 阶 + 1 阶 + 1 阶
2. 1 阶 + 2 阶
3. 2 阶 + 1 阶

确定思想
n<2 f(n)=n
n>2 f(n)=f(n-1)+f(n-2)
'''

from typing import *
class Solution:
    def climbStairs(self, n: int) -> int:
        if n<=2:
            return n
        dp=[0]*(n+1)
        dp[0]=1
        dp[1]=2
        for i in range(2,n):
            dp[i]=dp[i-1]+dp[i-2]
        print(dp)
        return dp[n-1]

if __name__=="__main__":
    solution=Solution()
    res=solution.climbStairs(2)
    print(res)
    res=solution.climbStairs(3)
    print(res)

