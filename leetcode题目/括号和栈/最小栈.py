'''
请你设计一个 最小栈 。它提供 push ，pop ，top 操作，并能在常数时间内检索到最小元素的栈。
实现 MinStack 类:
MinStack() 初始化堆栈对象。
void push(int val) 将元素val推入堆栈。
void pop() 删除堆栈顶部的元素。
int top() 获取堆栈顶部的元素。
int getMin() 获取堆栈中的最小元素。
'''
class MinStack:
    def __init__(self):
        """
        initialize your data structure here.
        """
        # 一个栈叫做 stack，负责栈的正常操作
        self.stack=[]
        # 一个栈叫做 min_stack，负责获取 stack 中的最小值
        self.minstack=[]

    def push(self, x: int) -> None:
        # 新添加的元素添加到 stack 中
        self.stack.append(x)

        # 判断 min_stack 是否为空，如果为空，直接同时把新添加的元素添加到 minStack 中
        # 如果 min_stack 不为空
        if self.min_stack:
            # 获取 min_stack 的栈顶元素
            top = self.min_stack[-1]

            # 只有新添加的元素不大于 top 才允许添加到 minStack 中，目的是为了让 minStack 从栈底到栈顶是降序的
            if x <= top:
                self.min_stack.append(x)

        # min_stack 中没有元素，所以直接把新添加的元素添加到 min_stack 中
        else:
            self.min_stack.append(x)

    def pop(self) -> None:
        # 正常栈进行pop
        pop=self.stack[-1]
        self.stack.pop()
        top=self.minstack[-1] #获取最小栈中的最小值
        if top==pop:
            self.minstack.pop()

    def top(self) -> int:
        top=self.stack[-1]
        return top
    def getMin(self) -> int:
        return self.minstack[-1]



# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(x)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()