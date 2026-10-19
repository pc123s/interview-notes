from collections import deque
'''
设计实现双端队列。
实现 MyCircularDeque 类:
MyCircularDeque(int k) ：构造函数,双端队列最大为 k 。
boolean insertFront()：将一个元素添加到双端队列头部。 如果操作成功返回 true ，否则返回 false 。
boolean insertLast() ：将一个元素添加到双端队列尾部。如果操作成功返回 true ，否则返回 false 。
boolean deleteFront() ：从双端队列头部删除一个元素。 如果操作成功返回 true ，否则返回 false 。
boolean deleteLast() ：从双端队列尾部删除一个元素。如果操作成功返回 true ，否则返回 false 。
int getFront() )：从双端队列头部获得一个元素。如果双端队列为空，返回 -1 。
int getRear() ：获得双端队列的最后一个元素。 如果双端队列为空，返回 -1 。
boolean isEmpty() ：若双端队列为空，则返回 true ，否则返回 false  。
boolean isFull() ：若双端队列满了，则返回 true ，否则返回 false 。

示例 1：
输入
["MyCircularDeque", "insertLast", "insertLast", "insertFront", "insertFront", "getRear", "isFull", "deleteLast", "insertFront", "getFront"]
[[3], [1], [2], [3], [4], [], [], [], [4], []]
输出
[null, true, true, true, false, 2, true, true, true, 4]

解释
MyCircularDeque circularDeque = new MycircularDeque(3); // 设置容量大小为3
circularDeque.insertLast(1);			        // 返回 true
circularDeque.insertLast(2);			        // 返回 true
circularDeque.insertFront(3);			        // 返回 true
circularDeque.insertFront(4);			        // 已经满了，返回 false
circularDeque.getRear();  				// 返回 2
circularDeque.isFull();				        // 返回 true
circularDeque.deleteLast();			        // 返回 true
circularDeque.insertFront(4);			        // 返回 true
circularDeque.getFront();				// 返回 4
'''

class MyCircularDeque:
    def __init__(self, k: int):
        self.num=k
        self.q1=deque()

    def insertFront(self, value: int) -> bool:
        if self.isFull():
            return False
        else:
            self.q1.insert(0,value)
            return True

    def insertLast(self, value: int) -> bool:
        if self.isFull():
            return False
        else:
            self.q1.append(value)
            return True

    def deleteFront(self) -> bool:
        if self.isEmpty():
            return False
        else:
            self.q1.popleft()
            return True

    def deleteLast(self) -> bool:
        if self.isEmpty():
            return False
        else:
            self.q1.pop()
            return True

    def getFront(self) -> int:
        if self.isEmpty():
            return False
        else:
            return self.q1[0]

    def getRear(self) -> int:
        if self.isEmpty():
            return False
        else:
            return self.q1[-1]

    def isEmpty(self) -> bool:
        if len(self.q1)==0:
            return True
        else:
            return False

    def isFull(self) -> bool:
        if len(self.q1)==self.num:
            return True
        else:
            return False

if __name__=="__main__":
    q1=MyCircularDeque(3)
    q1.insertLast()
