'''
请设计一个函数，用来判断在一个n乘m的矩阵中是否存在一条包含某长度为len的字符串所有字符的路径。路径可以从矩阵中的任意一个格子开始，每一步可以在矩阵中向左，向右，向上，向下移动一个格子。
如果一条路径经过了矩阵中的某一个格子，则该路径不能再进入该格子。 例如
| a b c e |
| s f c s |
| a d e e |
矩阵中包含一条字符串"bcced"的路径，但是矩阵中不包含"abcb"路径，因为字符串的第一个字符b占据了矩阵中的第一行第二个格子之后，路径不能再次进入该格子。

输入：
[[a,b,c,e],[s,f,c,s],[a,d,e,e]],"abcced"
复制
返回值：
true
输入：
[[a,b,c,e],[s,f,c,s],[a,d,e,e]],"abcb"
复制
返回值：
false

这道题的关键在于回溯，回溯过程中需要记录在当前位置是否已经对上下左右的字符
我们需要一个flag矩阵记录，true记录已经访问过，false代表还没有访问，
递归终止的条件，1、超出矩阵 2、与word[k]的字符不一致3、flag的当前位置为True,终止递归

'''
from typing import *
class Solution:
    def hasPath(self,matrix:List[List[int]],word:str):
        m=len(matrix)
        n=len(matrix[0])
        flag=[[False for i in range(n)] for j in range(m)]
        for i in range(m):
            for j in range(n):
                if matrix[i][j]==word[0]:
                    res=self.dfs(matrix,m,n,i,j,word,0,flag)
                    if res:
                        return res
        return False
    # state记录状态，state=1,2,3,4 分别代表向上 向下 向左 向右
    def dfs(self,matrix,m,n,i,j,word,k,flag):
        if i>=m or i<0 or j<0 or j>=n or word[k]!=matrix[i][j] or flag[i][j]==True:
            return False
        #print(i,j)
        #print(matrix[i][j])
        if k==len(word)-1:
            return True
        flag[i][j]=True
        res1=self.dfs(matrix,m,n,i+1,j,word,k+1,flag)
        res2=self.dfs(matrix,m,n,i-1,j,word,k+1,flag)
        res3=self.dfs(matrix,m,n,i,j+1,word,k+1,flag)
        res4=self.dfs(matrix,m,n,i,j-1,word,k+1,flag)
        if (res1 or res2 or res3 or res4):
            return True
        flag[i][j]=False


if __name__=="__main__":
    solution=Solution()
    if True:
        matrix=[["a", "b", "c", "e"], ["s", "f", "c", "s"], ["a", "d", "e", "e"]]
        word="abcced"
        res=solution.hasPath(matrix,word)
        print(res)
        matrix=[["a", "b", "c", "e"], ["s", "f", "c", "s"], ["a", "d", "e", "e"]]
        word="abcb"
        res=solution.hasPath(matrix,word)
        print(res)