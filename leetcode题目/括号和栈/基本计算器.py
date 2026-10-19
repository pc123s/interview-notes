'''
给你一个字符串表达式 s ，请你实现一个基本计算器来计算并返回它的值。
注意:不允许使用任何将字符串作为数学表达式计算的内置函数，比如 eval() 。
示例 1：
输入：s = "1 + 1"
输出：2
示例 2：

输入：s = " 2-1 + 2 "
输出：3
示例 3：

输入：s = "(1+(4+5+2)-3)+(6+8)"
输出：23

思路：这个和使用栈来消除括号的题目非常相似，都是利用栈来存储最里面的结果，我们知道有括号的运算就是从最里面的
符号开始，当遇到括号（时开始入栈，记录最顶层的元素，遇到）开始出栈，迭代栈内的计算结果。

'''
class Solution:
    def calculate(self, s: str) -> int:
        stack=[]
        res=0 #计算结果
        num=0 #计算当前的数字结果，因为要存储11，12这一类的数字
        sign=1
        length=len(s)
        i=0
        while i<length:
            char=s[i]
            #print(char)
            if char==" ":
                i+=1
            elif char.isdigit():
                # 计算连续迭代char的值，转为int整型
                value=0
                str=""
                # 这一步是计算123这类的字符串
                while i<length and s[i].isdigit():
                    str+=s[i]
                    i+=1
                value=int(str)
                res += sign*value
            elif char=="+":
                sign=1
                i+=1
            elif char=="-":
                sign=-1
                i+=1
            elif char=="(":
                # 让一开始sign和res先入栈，谁先append无所谓
                stack.append(sign)
                stack.append(res)
                i+=1
                res=0
                sign=1
            elif char==")":
                #print(stack)
                # 释放栈内之前的计算结果，并利用value加值计算
                Former_res=stack.pop()
                sign = stack.pop()

                #print(res)
                res=Former_res+sign*res
                i+=1
        # 防止最后不是）结尾，多做一层运算
        #res+=sign*res
        return res


if __name__=="__main__":
    solution=Solution()
    res=solution.calculate("(1+(4+5+2)-3)+(6+8)")
    print(res)
    res=solution.calculate("(1+(4+5+2)-3)+6+8")
    print(res)
    res=solution.calculate("2147483647")
    print(res)
    res=solution.calculate("- (3 + (4 + 5))")
    print(res)