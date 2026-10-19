'''
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。
有效字符串需满足：
左括号必须用相同类型的右括号闭合。
左括号必须以正确的顺序闭合。

链接：https://leetcode.cn/problems/valid-parentheses

输入：s = "()"
输出：true

输入：s = "()[]{}"
输出：true

输入：s = "(]"
输出：false

输入：s = "([)]"
输出：false

输入：s = "{[]}"
输出：true

思路采用栈的方式对数据进行存储，可以发现如果里面的括号不消除外面的也无法消除，出栈后如果栈为空则为True,否则为False
stack 使用list表示
'''
class Solution:
    def isValid(self, s: str) -> bool:
        if s=="":
            return False
        stack=[]
        for _ in s:
            stack.append(_)
            if len(stack)==1:
                continue
            else:
                b,a=stack[-1],stack[-2]
                if ((a=="(" and b==")") or (a=="{" and b=="}") or  (a=="[" and b=="]")):
                    stack.pop()
                    stack.pop()
        if len(stack)==0:
            return True
        else:
            return False
solution=Solution()
print(solution.isValid("()"))
print(solution.isValid("()[]{}"))
print(solution.isValid("(]"))
print(solution.isValid("([)]"))
print(solution.isValid("{[]}"))


class Solution:
    def isValid(self,str):
        if str=='':
            return False
        stack=[]
        for _ in str:
            stack.append(_)
            if len(stack)==1:
                continue
            else:
                a,b=stack[-2],stack[-1]
                if (a=="(" and b==")") or (a=="[" and b=="]") or (a=="{" and b=="}"):
                    stack.pop()
                    stack.pop()
        if stack==[]:
            return True
        else:
            return False
print("#################################")
solution=Solution()
print(solution.isValid("()"))
print(solution.isValid("()[]{}"))
print(solution.isValid("(]"))
print(solution.isValid("([)]"))
print(solution.isValid("{[]}"))