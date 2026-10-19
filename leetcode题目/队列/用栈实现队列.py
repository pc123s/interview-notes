'''
请你仅使用两个栈实现先入先出队列。

队列应当支持一般队列支持的所有操作（push、pop、peek、empty）：

实现 MyQueue 类：

void push(int x)将元素 x 推到队列的末尾
int pop() 从队列的开头移除并返回元素
int peek() 返回队列开头的元素
boolean empty()如果队列为空，返回 true ；否则，返回 false
'''

from typing import *
class MyQueue:

    def __init__(self):
        self.stack=[]

    def push(self, x: int) -> None:
        self.stack.append(x)

    def pop(self) -> int:
        return self.stack.pop(0)

    def peek(self) -> int:
        return self.stack[0]

    def empty(self) -> bool:
        if len(self.stack)==0:
            return True
        else:
            return False