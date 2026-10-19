'''
给你一个整数数组 coins ，表示不同面额的硬币；以及一个整数 amount ，表示总金额。
计算并返回可以凑成总金额所需的 最少的硬币个数 。如果没有任何一种硬币组合能组成总金额，返回 -1 。
你可以认为每种硬币的数量是无限的。


1+1  2
2   2

示例 1：

输入：amount = 5, coins = [1, 2, 5]
输出：4
解释：有四种方式可以凑成总金额：
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1
示例 2：

输入：amount = 3, coins = [2]
输出：0
解释：只用面额 2 的硬币不能凑成总金额 3 。
示例 3：

输入：amount = 10, coins = [10]
输出：1
方法:
[1,2,5] amount=11

按照零钱兑换1的思路，先求出dp再进行相应的回溯。
动态规划，看这个问题能否划分为子问题
dp[n]= 代表总钱数为amount时个数
这个可以分解为  dp[n-cj]+1 的方案和
比如 11 可以分解为 dp[11-2]=dp[9] dp[11-1]=dp[10] dp[11-5]=dp[6] 分别表示 在最优选择9时再拿一个2的硬币 最优选择10时拿1的硬币 最优选择6时，拿5的硬币
dp[11]=dp[6]+dp[9]+dp[10]

很显然这种方案会受到 数字顺序的影响 比如 1+1+2 和 2+1+1是一个方案
所以这里改变dp思路，我们希望你放入的零钱是顺序的，就是放入比如 11,如果 1 5 5三个硬币，那么一定是 1 5 5 而不是 5 1 1
出事化dp[i][0]为1  ，其余为0 也可以写为dp[0][0]=1,我们循环列的时候得从0开始循环
二维dp
    0  1  2  3  4  5  6  7  8  9  10  11
0   1  0  0  0  0  0  0  0  0  0  0   0
1   1  0  0  0  0  0  0  0  0  0  0   0
2   1  0  0  0  0  0  0  0  0  0  0   0
5   1  0  0  0  0  0  0  0  0  0  0   0
dp[0][0]- dp[0][11] 不做处理
dp[1]开始，表示我们只能用1的硬币达成目标
dp[1][1]=dp[1][1-1]+dp[0][1]=1 (按照上一个方案或者 相当于前一个方案)
dp[1][2]=dp[1][2-1]+dp[0][2]=1 ...
二维dp
    0  1  2  3  4  5  6  7  8  9  10  11
0   1  0  0  0  0  0  0  0  0  0  0   0
1   1  1  1  1  1  1  1  1  1  1  1   1
2   1  1  2  2  3  3  4  4  5  5  6   6
5   1  0  0  0  0  0  0  0  0  0  0   0
d[2]开始，表示我们添加了新的2硬币，这时在1硬币的基础上进行
dp[2][1]=dp[2][1-2]+dp[2-1][1]=0+1=1 因为1-2小于0了dp[2][1-2]=0，代表没法只用硬币2来满足要求，
dp[2][2]=dp[2][2-2]+dp[2-1][2]=1+1=2 因为1-2小于0了，代表没法只用硬币2来满足要求，

依次类推

这个bp的重点在 dp[i] 这一行表明我们要求你只能加入这个硬币 dp[2] 表示这一行你只能加入硬币2



'''
from typing import *
class Solution:
    def change(self,  amount: int, coins: List[int]) -> int:
        if not coins:
            return -1
        coins.sort()
        m=len(coins)+1
        n=amount+1
        dp=[[0 for i in range(n)] for j in range(m)]
        #print(dp)
        dp[0][0]=1
        #初始化部分矩阵
        # for i in range(m):
        #     #print(i)
        #     dp[i][0]=1
        for i in range(1,m):
            for j in range(n):
                c_coin=coins[i-1]
                if j-c_coin<0:
                    dp[i][j]=dp[i-1][j]
                else:
                    dp[i][j]=dp[i-1][j]+dp[i][j-c_coin]
        return dp[m-1][n-1]

if __name__=="__main__":
    solution=Solution()
    if True:
        coins=[1,2,5]
        amount=5
        res=solution.change(amount,coins)
        print(res)

    coins=[2]
    amount=3
    res=solution.change(amount,coins)
    print(res)

    coins=[10]
    amount=10
    res=solution.change(amount,coins)
    print(res)