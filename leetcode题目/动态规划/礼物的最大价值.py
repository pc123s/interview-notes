'''
礼物的最大价值
在一个
m×n的棋盘的每一格都放有一个礼物，每个礼物都有一定的价值（价值大于 0）。你可以从棋盘的左上角开始拿格子里的礼物，并每次向右或者向下移动一格、直到到达棋盘的右下角。给定一个棋盘及其上面的礼物的价值，请计算你最多能拿到多少价值的礼物？
如输入这样的一个二维数组，
[
[1,3,1],
[1,5,1],
[4,2,1]
]
那么路径 1→3→5→2→1 可以拿到最多价值的礼物，价值为12
示例1
输入：
[  [1,3,1],
   [1,5,1],
   [4,2,1]
]
复制
返回值：
12
思路1：暴力法
思路深度优先遍历，我们可以想象成当前的这个路径就是一棵树，我每次都是向下或者向右进行遍历。最后得到最大值
这种方法就是时间复杂度过高，相当于 o((m*n)*2)的时间复杂度

思路2：dp的思路进行相应的优化
题目中的矩阵是3*3的，我们发现dp[i][j]的最大价值，等于dp[i-1][j]拿上matrix[i][j]或者 dp[i][j-1]拿上matrix[i][j]的最大值

   0 0 0  0
   0 1 4  5
   0 2 9  9
   0 6 11 12




'''
from typing import *

class Solution:
    def __init__(self):
        self.arr=[]
    def maxValue(self , grid: List[List[int]]) -> int:
        # write code here
        m=len(grid)
        n=len(grid[0])
        if m==1:
            return sum(grid[0])
        def dfs(grid,a,b,sumGift):
            if a >= m or b>=n:
                return
            sumGift+=grid[a][b]
            #print(value)
            if a==m-1 and b==n-1:
                self.arr.append(sumGift)
                #print(self.arr)
                return
            dfs(grid,a+1,b,sumGift)
            dfs(grid,a,b+1,sumGift)

        dfs(grid,0,0,0)
        return max(self.arr)

    def maxValue1(self,grid:List[List[int]])->int:
        m=len(grid)
        n=len(grid[0])
        dp=[[0]*(n+1) for i in range(m+1)]
        for i in range(1,m+1):
            for j in range(1,n+1):
                dp[i][j]=max(dp[i][j-1]+grid[i-1][j-1],dp[i-1][j]+grid[i-1][j-1])
        return dp[m][n]

    def maxValue2(self,grid:List[List[int]])->int:
        '''
        改进，不仅要输出最大值还要输出路径
        :param grid:
        :return:
        '''
        m=len(grid)
        n=len(grid[0])
        dp=[[0]*(n+1) for i in range(m+1)]
        path_res=[]
        for i in range(1,m+1):
            for j in range(1,n+1):
                dp[i][j]=max(dp[i][j-1]+grid[i-1][j-1],dp[i-1][j]+grid[i-1][j-1])

        path_res.append(grid[m-1][n-1])
        i,j=m,n
        while True:
            if i==1 and j==1:
                # path_res.append(grid[0][0])
                break
            a=dp[i][j-1]
            b=dp[i-1][j]
            if a>=b:
                # 加入的是上一轮添加的值
                path_res.append(grid[i-1][j-2])
                i=i
                j=j-1
            else:
                path_res.append(grid[i-2][j-1])
                i=i-1
                j=j
        print(path_res[::-1])

        return dp[m][n]

if __name__=="__main__":
    solution=Solution()
    grid=[[1,3,1],
          [1,5,1],
          [4,2,1]]
    arr=solution.maxValue2(grid)
    print(arr)