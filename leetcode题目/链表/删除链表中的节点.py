'''
描述
给定单向链表的头指针和一个要删除的节点的值，定义一个函数删除该节点。返回删除后的链表的头节点。

1.此题对比原题有改动
2.题目保证链表中节点的值互不相同

输入：
{2,5,1,9},5
返回值：
{2,1,9}
说明：
给定你链表中值为 5 的第二个节点，那么在调用了你的函数之后，该链表应变为 2 -> 1 -> 9
示例2
输入：
{2,5,1,9},1
返回值：
{2,5,9}
给定你链表中值为 1 的第三个节点，那么在调用了你的函数之后，该链表应变为 2 -> 5 -> 9

思路：定义两个指针，pre和cur
如果，cur的值不等于输入的值，那么pre和cur指针后移，否则cur的指针后移，pre指向cur

-1 2  5  1 9
p  c
-1 2  5  1 9
   p  c
c=5
cur后移
-1 2  5  1 9
   p     c

'''
from typing import *
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def deleteNode(self , head: ListNode, val: int) -> ListNode:
        res=ListNode(-1)
        res.next=head
        pre=res
        cur=head
        while cur!=None:
            if cur.val==val:
                cur=cur.next
                pre.next=cur
            else:
                pre=cur
                cur=cur.next

        return res.next
    def tranverseNode(self,head):
        while head:
            print(head.val)
            head=head.next
if __name__=="__main__":
        node1 = ListNode(1)
        node2 = ListNode(2)
        node3 = ListNode(3)
        node4 = ListNode(4)
        node5 = ListNode(5)
        node1.next=node2
        node2.next=node3
        node3.next=node4
        node4.next=node5
        solution=Solution()
        node_=solution.deleteNode(node1,3)
        solution.tranverseNode(node_)