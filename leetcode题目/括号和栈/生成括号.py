'''
数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。 示例 1：
输入：n = 3 输出：["((()))","(()())","(())()","()(())","()()()"] 示例 2：
输入：n = 1 输出：["()"]
提示： 1 <= n <= 8
'''
class Solution:
    def __init__(self):
        self.res=[]
    def dfs(self,left,right,path):
        if left==0 and right==0:
            self.res.append(path)
            return
        if left>right:
            return
        if left==0:
            self.dfs(left, right-1, path+")")
            return
        if  right==0:
            self.dfs(left-1, right, path + "(")
            return
        self.dfs(left-1,right,path+"(")
        self.dfs(left,right-1,path+")")

    def generateParenthesis(self, n: int):
        self.dfs(n,n,"")
        return self.res

solution=Solution()
print(solution.generateParenthesis(3))