'''
请根据每日 气温 列表 temperatures ，重新生成一个列表，要求其对应位置的输出为：要想观测到更高的气温，至少需要等待的天数。
如果气温在这之后都不会升高，
请在该位置用 0 来代替。

示例 1:

输入: temperatures = [73,74,75,71,69,72,76,73]
输出: [1,1,4,2,1,1,0,0]
示例 2:

输入: temperatures = [30,40,50,60]
输出: [1,1,1,0]
示例 3:

输入: temperatures = [30,60,90]
输出: [1,1,0]

首先我想到的是暴力法，即两个指针，一个指向当前位置，一个指向当前位置后面的位置，如果后面位置的指针比当前指针高则输出两个的间隔，否则输出0
这种可以，但是时间复杂度过高O(n2)

方法2：采用递增栈的解法进行求解，所谓递增栈即栈顶元素比栈底元素小（从右向左依次递增） 如[5,3,2,1] 即递增栈:只有比栈顶元素小的元素才能直接进,否则要进行出栈的操作。
从右向左单调递增
输入: temperatures = [73,74,75,71,69,72,76,73]
输出: [1,1,4,2,1,1,0,0]

73,74,75,71,69,72,76,73
0   1  2  3  4  5  6  7
用一个栈存入第一个值,这个栈是个递减栈， 左边大  右边小
当遇到栈尾大的值时，将值弹出，与当前值计算index并存入
遇到比栈尾小的值时，将值加入，直到遇到大的值，再一个个弹出计算当前值和栈尾部值的差值，因为存的index，所以只需要计算index的位置差，并
存入弹出元素index的位置。
为此我们需要存储一个上升温度天数的list

73 - [73]
74 - [74] 74-73 求出下标
75 - [75] 75-74 求出下标
71 - [75,71]
69 - [75,71,69]
72 - [75,71,69] 72和69求下标 72和71求下标 入栈[75,72]
76 - [76] 76和72求下标 76和75求下标 入栈[76]
73 - [73] 76出栈


'''



from typing import *
class Solution:
    def dailyTemperatures_test(self, temperatures: List[int]) -> List[int]:
        n=len(temperatures)
        stack=[] #单调栈，从左到右，依次变小
        temperature_up_res=[0]*n #记录上升的天数
        stack.append(0)
        for i in range(1,n):
            if temperatures[i]>temperatures[stack[-1]]:
                # 不断将栈尾的数据弹出
                while stack and temperatures[i]>temperatures[stack[-1]]:
                    j=stack.pop()
                    temperature_up_res[j]=i-j
                stack.append(i)
            else:
                stack.append(i)
        #print(temperature_up_res)
        return temperature_up_res






    def dailyTemperatures_1(self, temperatures: List[int]) -> List[int]:
        n=len(temperatures)
        res=[0 for i in range(n)]
        for i in range(n-1):
            j=i+1
            while j<n:
                a,b=temperatures[i],temperatures[j]
                if b>a:
                    res[i]=(j-i)
                    break
                j+=1
        #最后一位肯定为0
        #res.append(0)
        return res



if __name__=='__main__':
    solution=Solution()
    res=solution.dailyTemperatures_test([73,74,75,71,69,72,76,73])
    print(res)
    res=solution.dailyTemperatures_test([30,40,50,60])
    print(res)
    res = solution.dailyTemperatures_test([30,60,90])
    print(res)













