'''
机器人的行动轨迹
有个机器人，可以向下 向右，进行移动，其中矩阵中有障碍物的会用1来表示
求机器人能够到达矩阵右下角的所有路径

输入：
[
[0,0,0],
[0,1,0],
[0,0,0]
]
输出：2

输入
matrix = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,0,0]
]
输出：0
输入：
matrix = [
    [0,0,1,0],
    [0,1,0,0],
    [0,0,0,0]
]
输出:1

方法1：使用动态规划的方法
假设 矩阵为m×n,
那么 从左到右开始遍历，有
当所在的区域为0时代表可以通行，那么就有
dp[i][j]=dp[i-1][j]+dp[i][j-1] #即从上或者从下来，那么路径为两者之和（上面有3条路，下面有一条路）
i和j是从1开始的
需要注意的两点：
dp[i][0] i从0，m 都为1，
dp[0][j] j从0，n 都为1，
因为第一行和第一列，无论何时都只有一条路径（因为只能向右或者向下）
但是需要考虑第一行或者第一列有阻碍的情况，比如遇到1了，这时后面的行或者列的dp都为0，因为不可能绕过去了



'''
from typing import *
from collections import deque
import copy
class Solution:
    def __init__(self):
        self.arr=[]
    def find_path(self,matrix:List[List[int]]):
        m=len(matrix)
        n=len(matrix[0])

        res=[[0 for i in range(n)] for j in range(m)]
        #对第一行 第一列进行特殊处理
        triger=False
        for i in range(m):
            if matrix[i][0]==0:
                res[i][0]=1
            else:#有障碍物
                triger=True
                break
        if triger:
            for j in range(i,m):
                res[i][0]=0
        #print(res)
        triger=False
        for i in range(n):
            if matrix[0][i]==0:
                res[0][i]=1
            else:
                triger=True
                break
        if triger:
            for j in range(i,n):
                res[0][i]=0

        print(res)
        for i in range(1,m):
            for j in range(1,n):
                if matrix[i][j]==0:
                    res[i][j]=res[i-1][j]+res[i][j-1]

        print(res[m-1][n-1])


    def find_path1(self, matrix: List[List[int]]):
        m = len(matrix)
        n = len(matrix[0])
        flag=[[False for i in range(n)] for j in range(m)]
        self.dfs(matrix,0,0,m,n,flag,[])
        #print(self.arr)
        return len(self.arr)
    def dfs(self,matrix,i,j,m,n,flag,path:List[List]):
        if i>=m or j>=n or flag[i][j]==True or matrix[i][j]==1:
            return False
        path.append([i, j])

        if i==m-1 and j==n-1:
            path1=copy.deepcopy(path)
            self.arr.append(path1)
            # 找到终点值需要回溯一次
            flag[i][j]=False
            path.pop()
            return True
        flag[i][j]=True
        s_direc=  self.dfs(matrix,i+1,j,m,n,flag,path)
        r_direc = self.dfs(matrix,i,j+1,m,n,flag,path)
        if s_direc or r_direc:
            # 代表你左边或者右边找到了正确的值，此时需要回溯一次
            flag[i][j]=False
            path.pop()
            return
        if self.arr:
            path.pop()
            flag[i][j]=False
        #return False
        #return
        #return path

if __name__=="__main__":
    solution=Solution()

    if True:
        matrix=[
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        res=solution.find_path1(matrix)
    if True:
        matrix = [
            [1,0,0,0],
            [0,1,0,0],
            [0,0,0,0]
        ]
        solution.arr=[]
        solution.find_path1(matrix)
    if True:
        matrix = [
            [0,0,1,0],
            [0,1,0,0],
            [0,0,0,0]
        ]
        solution.arr=[]
        solution.find_path1(matrix)
    if True:
        matrix = [
            [0,0,0,0],
            [0,1,0,0],
            [0,0,0,0]
        ]
        solution.arr=[]
        solution.find_path1(matrix)
