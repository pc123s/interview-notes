'''
示例 1：

输入：n = 3
输出：["((()))","(()())","(())()","()(())","()()()"]
示例 2：

输入：n = 1
输出：["()"]

提示：
1 <= n <= 8

1、首先这道题我的第一想法就是二叉树去进行求解。
（1） 采用（）不断迭代生成2叉树，其中二叉树又分为左子树和右子树，对于左右子树来说，必须保证左子树始终大于等于右子树才是一个
正确的括号形式。为此我们可以利用递归加优先深度搜索的方式来进行
方法2：
这个是比较笨的办法，即先生成一个标准组的括号，如()()()，然后利用遍历的方式交换两个不同index的位置，交换完成后进行去重和对有效括号的判断
方法2不对，这样进行的括号生成会遗漏掉很多的情况。所以不能用暴力的解法


solution2和solution3都是对的，可以参考思路
'''
from typing import *
import copy
# 方法2的生成的方法，这个解法是错误的，最好的做法还是采用树的做法来解决

class Solution:
    def is_valid_parenthesis(self,path):
        stack1=list(path)
        stack2=[]
        while stack1:
            a=stack1.pop()
            stack2.append(a)
            if len(stack2)==1:
                pass
            else:
                a=stack2[-1]
                b=stack2[-2]
                if a=="(" and b==")":
                    stack2.pop()
                    stack2.pop()
        if stack2:
            return False
        else:
            return True
    def generateParenthesis(self, n: int) -> List[str]:
        if n==0:
            return []
        res=[]
        begin_str=n*" ( ) "
        begin_str=list(begin_str)
        print(begin_str)
        m=len(begin_str)
        for i in range(m-1):
            for j in range(i+1,m):
                begin_str_=copy.deepcopy(begin_str)
                begin_str_[j],begin_str_[i]=begin_str_[i],begin_str_[j]
                begin_str_=[i for i in begin_str_ if i!=" "]
                res.append("".join(begin_str_))
        res=list(set(res))
        #print(res)
        res=[char for char in res if self.is_valid_parenthesis(char)]
        #print(res)
        return res
class Solution1:
    def __init__(self):
        self.arr=[]
    def dfs_error(self,path,left,right,n):
        print(path,left,right)
        if left==n and right==n:
            #if len(path)==2*n:
            self.arr.append(path)
            return
        if left>n or right>n:
            return
        #这样写相当于先进行path的括号添加，但是没有进行进行左dfs的生成，这样在出现（（（（这样的条件时就无法进行下一步的子树的生成，
        path+="("
        left+=1
        self.dfs(path,left,right,n)
        path+=")"
        right+=1
        self.dfs(path,left,right,n)
    def dfs(self,path,left,right,n):
        if left==n and right==n:
            self.arr.append(path)
            return
        if left>n or right>n or right>left:
            return
        #这样写一旦dfs递归结束，进行递归的是没有添加"("的值
        self.dfs(path+"(",left+1,right,n)
        self.dfs(path+")",left, right+1, n)

    def generateParenthesis(self, n: int) -> List[str]:
        if n == 0:
            return []
        else:
            self.dfs("",0,0,n)
            return self.arr
class Solution2:
    def __init__(self):
        self.arr=[]
    def is_valid_parenthesis(self, path):
        stack1 = list(path)
        stack2 = []
        while stack1:
            a = stack1.pop()
            stack2.append(a)
            if len(stack2) == 1:
                pass
            else:
                a = stack2[-1]
                b = stack2[-2]
                if a == "(" and b == ")":
                    stack2.pop()
                    stack2.pop()
        if stack2:
            return False
        else:
            return True
    def dfs(self,path,left,right,n):
        if len(path)==n:
            self.arr.append(path)
            return
        if left<right:
            return
        #这样写一旦dfs递归结束，进行递归的是没有添加"("的值
        self.dfs(path+"(",left+1,right,n)
        self.dfs(path+")",left,right+1, n)

    def generateParenthesis(self, n: int) -> List[str]:
        if n == 0:
            return []
        else:
            self.dfs("",0,0,n*2)
            arr1=[i for i in self.arr if self.is_valid_parenthesis(i)]
            #arr2=list(set(arr1))
            return arr1
if __name__=="__main__":
    solution=Solution()
    test_arr=["((()))","()()()(","(())()","(()())"]
    for char in test_arr:
        print(solution.is_valid_parenthesis(char))
    solution.generateParenthesis(3)
    solution=Solution1()
    res=solution.generateParenthesis(3)
    print(res)
    solution=Solution2()
    print(solution.generateParenthesis(3))