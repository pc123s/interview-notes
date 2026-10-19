'''
打印链表
输入一个链表的头节点，按链表从尾到头的顺序返回每个节点的值（用数组返回）。
输入：
{1,2,3}
复制
返回值：
[3,2,1]

思路，设置一个虚拟节点，将链表都指向这个虚拟节点，并返回

'''
from typing import *
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def printListFromTailToHead(self , listNode: ListNode) -> List[int]:
        # write code here
        if not listNode:
            return []

        arr=[]
        while listNode:
            arr.append(listNode.val)
            listNode=listNode.next
        return arr[::-1]

if __name__=="__main__":
    solution=Solution()
    node1=ListNode(1)
    node2=ListNode(2)
    node3=ListNode(3)
    node1.next=node2
    node2.next=node3
    res=solution.printListFromTailToHead(node1)
    print(res)