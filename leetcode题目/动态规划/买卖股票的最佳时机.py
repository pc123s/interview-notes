'''
给定一个数组 prices ，它的第 i 个元素 prices[i] 表示一支给定股票第 i 天的价格。

你只能选择 某一天 买入这只股票，并选择在 未来的某一个不同的日子 卖出该股票。设计一个算法来计算你所能获取的最大利润。

返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 0 。

输入：[7,1,5,3,6,4]
输出：5
解释：在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
     注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格；同时，你不能在买入前卖出股票。

输入：prices = [7,6,4,3,1]
输出：0
解释：在这种情况下, 没有交易完成, 所以最大利润为 0。

思路：（1）暴力法，直接循环遍历，差不多是o（n2）的时间复杂度(时间复杂度过高)
（2）排序的算法；对数组排序，输入值和在原数组中的位置， 取第一个set(index,value)为最小值，从后向前遍历，如果满足value大于最小值且index>index_min，即最大收益。
（3） 遍历一次，记录股票最低点的位置和最高点的位置，只要最高点在最低点后面，那么一定可以卖出。即最大利润。

 minPrice=99999
 maxprice=-1
 我们每次遍历都在寻找整个数组的最小和最大值，然后每次都计算一次差值，差值必须满足，第一，minPrice和maxPrice不为初始值，maxIndex大于minIndex
  [ 7  ,  1  ,  5  ,  3  ,  6  ,  4 ]
   i
   j
dp[0      0     0     0     0     0]
先找minPrice
minPrice=7
minIndex=0
更新完minIndex以后我们需要查看：1 minIndex是否大于maxIndex,如果比它大，那么需要将其index和value更新到最新的值。（因为之前找的index,maxValu已经不算数了）
查看是否更新maxPrice
要更新，1、minprice不为空
2、i必须大于minIndex
  [ 7  ,  1  ,  5  ,  3  ,  6  ,  4 ]
          i
    j
minPrice=1
仍然不更新maxPrice
  [ 7  ,  1  ,  5  ,  3  ,  6  ,  4 ]
                i
    j
minprice=1
maxIndex=2
maxPrice=5 #计算一次差值


注意：当c_price小于最小的股票值时可以选择不更新，因为找到最小值，后面即使出现最小值了也无所谓
但是当c_price大于最大的股票值时，需要更新值，因为我们一定要保证最大值是最新的。
比如

[2, 1, 2, 1, 0, 1, 2]
             i
在没到之前我们此时已经找到了最大和最小值，分别为1 和2
当i指向0
最小值为0，如果我们不更新最大值时，那么最大值用于指向index为2的2了，无法更新最大收益
方法（4）
我们每向前遍历一次就记录一下之前的最小值，并且每天询问，我今天是不是可以把股票卖了，卖了收益多少。

'''
from typing import *
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
        n=len(prices)
        minPrice=999999
        minIndex=0
        maxPrice=-1
        maxIndex=0
        #dp=[0 for i in range(n)]
        maxProfit=0
        for i in range(len(prices)):
            curPrice=prices[i]
            # 先更新最小值
            if curPrice<minPrice:
                minPrice=curPrice
                minIndex=i
                #代表minIndex已经更新了，此时最大值要从当前开始计算，之前的最大值不算了
                if minIndex>maxIndex:
                    maxIndex=minIndex
                    maxPrice=curPrice
            if minPrice!=99999 and i>minIndex:
                if curPrice>=maxPrice:
                    maxPrice=curPrice
                    maxIndex=i
                    cProfit=maxPrice-minPrice
                    maxPrice=curPrice
                    if cProfit>maxProfit:
                        maxProfit=cProfit
        #print(minIndex,maxIndex)
        return maxProfit
    def maxProfit1(self, prices: List[int]) -> int:
        if not prices:
            return 0
        n=len(prices)
        minPrice=9999999
        maxProfit=0
        for i in range(len(prices)):
            curPrice=prices[i]
            if curPrice<minPrice:
                minPrice=curPrice
            cProfit=curPrice-minPrice
            if cProfit>maxProfit:
                maxProfit=cProfit
        return maxProfit
    def maxProfit2(self,prices:List[int])->int:
        '''
        :param prices:
        :return:
        7 1 5 3 6 4
        1 min_price=7
        5 min_price=1 4
        3 min_price=1 2
        6 min_price=1 5
        4 min_price=1 3
        '''
        if not prices or len(prices)==1:
            return 0
        minPrice=99999
        max_profit=0
        if prices[0]<minPrice:
            minPrice=prices[0]
        n=len(prices)
        for i in range(1,n):
            if prices[i]>minPrice:
                profit=prices[i]-minPrice
                if profit>max_profit:
                    max_profit=profit
            if prices[i]<minPrice:
                minPrice=prices[i]
        return max_profit


        
        
if __name__=="__main__":
    solution=Solution()
    res=solution.maxProfit2([7,1,5,3,6,4])
    print(res)
    res=solution.maxProfit([1,2,3,4,5,6,7,8])
    print(res)
    res=solution.maxProfit2([2,2,2,2,2,2])
    print(res)
    prices =[2, 1, 2, 1, 0, 1, 2]
    res=solution.maxProfit2(prices)
    print(res)
