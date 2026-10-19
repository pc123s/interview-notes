'''
有效的括号
传入 （）
{()}
看你是否能看出这些括号是不是有效的
'''

class Solution:
    def isValid(self, s: str) -> bool:
        if s=="":
            return False
        stack1=[]
        stack2=[]
        for _ in s:
            stack1.append(_)
        while stack1:
            a=stack1.pop()
            if not stack2:
                stack2.append(a)
            else:
                b=stack2[-1]
                if (a=="(" and b==")") or (a=="{" and b=="}") or (a=="[" and b=="]"):
                    stack2.pop()
                else:
                    stack2.append(a)
        if stack2:
            return False
        else:
            return True

solution=Solution()
print(solution.isValid("()"))
print(solution.isValid("()[]{}"))
print(solution.isValid("(]"))
print(solution.isValid("([)]"))
print(solution.isValid("{[]}"))
