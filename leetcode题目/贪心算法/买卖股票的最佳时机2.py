'''
 LeetCode 122

 给你一个整数数组 prices ，其中 prices[i] 表示某支股票第 i 天的价格。

在每一天，你可以决定是否购买和/或出售股票。你在任何时候 最多 只能持有 一股 股票。你也可以先购买，然后在 同一天 出售。

返回 你能获得的 最大 利润 。



示例 1：

输入：prices = [7,1,5,3,6,4]
输出：7
解释：在第 2 天（股票价格 = 1）的时候买入，在第 3 天（股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5 - 1 = 4 。
     随后，在第 4 天（股票价格 = 3）的时候买入，在第 5 天（股票价格 = 6）的时候卖出, 这笔交易所能获得利润 = 6 - 3 = 3 。
     总利润为 4 + 3 = 7 。
示例 2：

输入：prices = [1,2,3,4,5]
输出：4
解释：在第 1 天（股票价格 = 1）的时候买入，在第 5 天 （股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5 - 1 = 4 。
     总利润为 4 。
示例 3：

输入：prices = [7,6,4,3,1]
输出：0
解释：在这种情况下, 交易无法获得正利润，所以不参与交易可以获得最大利润，最大利润为 0 。

1、思路，可以采用深度优先遍历的方式来求解，即每一天我都有两个状态，持有或者卖出股票，这样就形成了一个树，我只要遍历这个树即可（这个思路我也不是非常清楚，感觉时间复杂度很高）

2、思路
采用贪心算法，我要获得最大的利润，比如 我在1买 5卖获得4块钱。也可以想象为我在1 买后，之后后面的股票比今天高，我就一直持有，一直到股价下降我再卖出
并且 = 连续间隔的差值 1 2 2 5 =2-1+2-2+5-2=1+3=4

'''
from  typing import *
class Solution:
    def dfs(self,prices,status,index,profit):
        '''

        :param prices:
        :param status:0表示持有，1表示卖出
        :param index:
        :param profit:
        :return:
        '''
        if index==len(prices): #在树的最深处
            # 记录最大利润
            self.maxnum=max(profit,self.maxnum)
            return

        self.dfs(prices,status,index+1,profit)
        if status==0: #当前持有股票,那么卖出
            self.dfs(prices,1,index+1,profit-prices[index])
        else :
            self.dfs(prices,0,index+1,profit+prices[index])


    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
        if len(prices)==1:
            return 0
        self.maxnum=0
        self.dfs(prices,0,0,0)
        return self.maxnum

    def maxProfit1(self, prices: List[int]) -> int:
        '''
        贪心算法
        :param prices:
        :return:
        '''
        if not prices:
            return 0
        if len(prices)==1:
            return 0
        profit=0
        for i in range(len(prices)-1):
            if prices[i+1]>=prices[i]:
                profit+=prices[i+1]-prices[i]

        return profit

if __name__=="__main__":
    solution=Solution()
    res=solution.maxProfit1([7,1,5,3,6,4])
    print(res)