'''
给你一个整数数组 coins ，表示不同面额的硬币；以及一个整数 amount ，表示总金额。
计算并返回可以凑成总金额所需的 最少的硬币个数 。如果没有任何一种硬币组合能组成总金额，返回 -1 。
你可以认为每种硬币的数量是无限的。



示例 1：

输入：coins = [1, 2, 5], amount = 11
输出：3
解释：11 = 5 + 5 + 1
示例 2：

输入：coins = [2], amount = 3
输出：-1
示例 3：

输入：coins = [1], amount = 0
输出：0

方法:
动态规划，看这个问题能否划分为子问题
dp[n]= 代表n个总金额需要的最少硬币数
这个可以分解为  dp[n-cj]+1  cj表示不同面额的金额数
比如 11 可以分解为 dp[11-2]=dp[9] dp[11-1]=dp[10] dp[11-5]=dp[6] 分别表示 在最优选择9时再拿一个2的硬币 最优选择10时拿1的硬币 最优选择6时，拿5的硬币

所以我们求dp[11]就只需要求前面相应的dp就行

'''
from typing import *
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        if not coins:
            return -1
        coins.sort()
        dp=[0]*(amount+1)
        dp[0]=0
        arr=[]*amount
        for i in range(1,amount+1):
            # 找其中的最小值
            minCoin=999999999999 #记录当前的最小方法
            for c in coins:
                lastDp=i-c
                if lastDp<0 :
                    pass
                else:
                    if dp[lastDp]!=-1:
                        curCoin=dp[lastDp]+1
                        if curCoin<minCoin:
                            minCoin=curCoin
            if minCoin!=999999999999:
                dp[i]=minCoin
            else: #代表当前dp为非有效动态，意思 比如[2] amount=1  这时无论如何都可能达到amount
                dp[i]=-1
            print(dp)
        return dp[-1]

if __name__=="__main__":
    solution=Solution()
    if True:
        coins=[1,2,5]
        amount=11
        res=solution.coinChange(coins,amount)
        print(res)

    coins=[2]
    amount=3
    res=solution.coinChange(coins,amount)
    print(res)