'''
给定 pushed 和 popped 两个序列，每个序列中的 值都不重复，只有当它们可能是在最初空栈上进行的推入 push 和弹出 pop 操作序列的结果时，返回 true；否则，返回 false 。
示例 1：

输入：pushed = [1,2,3,4,5], popped = [4,5,3,2,1]
输出：true
解释：我们可以按以下顺序执行：
push(1), push(2), push(3), push(4), pop() -> 4,
push(5), pop() -> 5, pop() -> 3, pop() -> 2, pop() -> 1
示例 2：

输入：pushed = [1,2,3,4,5], popped = [4,3,5,1,2]
输出：false
解释：1 不能在 2 之前弹出。

其实这个题目是什么意思呢，大致就是前面是栈的输入序列，后面是栈的输出序列，看后面的弹出是否在前面能实现
我的想法是模拟这样一个过程，采用一个stack承接的pushed的值,如果栈顶元素和pop的下标一致时则弹出，一直执行这个操作，如果pushed不为空则返回False.
'''
from typing import *
class Solution:
    def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:
        stack=[]
        for item in pushed:
            stack.append(item)
            while stack and stack[-1]==popped[0]:
                print(stack,popped)
                stack.pop()
                popped.pop(0)
        if stack:
            return False
        else:
            return True

if __name__=="__main__":
    solution=Solution()
    print(solution.validateStackSequences([1,2,3,4,5],[4,5,3,2,1]))
    print(solution.validateStackSequences([1, 2, 3, 4, 5], [4,3,5,1,2]))

