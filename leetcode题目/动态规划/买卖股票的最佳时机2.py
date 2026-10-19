'''
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

注意这道题代表可以买卖无数次股票，这也代表，只要后面的股票比前面高我们就可以获利

思路：
1、贪心算法
5>1 获利4
3小于5 不计算
6大于3 获利3
4小于6不获利
3+4=7
可以ac


方法2：暴力搜索法
暴力搜索的角度来看，
持有=0 卖出=1
              0·
       0              1
    0     1        0     1
  0   1  0       0  1  0

从树的结构而言，1时为卖出，但是我们需要考虑买入，即计算之前的所有0-1的路径的收益
这里需要注意，需要0之后可以0或者1，但1之后不能为1
比如我们有8个路径， 0 1 0 1 0 1 0 1 0 1最后需要考虑这8个最大值。递归的话计算一次就行，关键在于怎么计算
在路径中1时需要计算一次收益

暴力搜索的时间复杂度很高，没有通过全部AC但是可行


'''
from typing import *
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        '''
        :param prices:
        :return:
        '''
        n=len(prices)
        res=0 #记录最大的利润数

        def dfs(profit:int,res:int,state:int,n:int,i:int,prices:List[int],buy_price):
            '''

            :param profit:记录最大的收益
            :param res: 记录当前路径的收益
            :param state: 状态
            :param n: 多少层
            :param i: 到第几层了
            :param prices: prices数组
            buy_price：记录卖之前的最小值
            :return:
            '''
            if i==n:
                #print(res)
                if res>self.profit:
                    self.profit=res
                return
            # if res<0:
            #     return
            if state==0:
                if buy_price>prices[i]:
                    buy_price=prices[i]
                dfs(profit, res, 0, n, i + 1, prices, buy_price)
                dfs(profit, res, 1, n, i + 1, prices, buy_price)

            else:
                res+=prices[i]-buy_price
                buy_price=prices[i]
                dfs(profit, res, 0, n, i + 1, prices, buy_price)
            #print(res)

        profit=0
        self.profit=0
        dfs(profit,0,0,n,0,prices,prices[0])
        print(self.profit)
    def maxProfit1(self,prices: List[int]):
        n=len(prices)
        if n==1:
            return 0
        profit=0
        for i in range(0,n-1):
            if prices[i+1]>prices[i]:
                profit+=prices[i+1]-prices[i]
        return profit


if __name__=="__main__":
    solution=Solution()
    prices=[7,1,5,3,6,4]
    solution.maxProfit(prices)
    prices=[7, 6, 4, 3, 1]
    solution.maxProfit(prices)
