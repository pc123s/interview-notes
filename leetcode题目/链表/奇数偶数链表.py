"""
给定单链表的头节点 head ，将所有索引为奇数的节点和索引为偶数的节点分别组合在一起，然后返回重新排序的列表。
第一个节点的索引被认为是 奇数 ， 第二个节点的索引为 偶数 ，以此类推。
请注意，偶数组和奇数组内部的相对顺序应该与输入时保持一致。
你必须在 O(1) 的额外空间复杂度和 O(n) 的时间复杂度下解决这个问题。

输入: head = [1,2,3,4,5]
输出: [1,3,5,2,4]

输入: head = [2,1,3,5,6,4,7]
输出: [2,3,6,7,1,5,4]

方法1：双制止法
设置两个头结点 pre1 pre2
pre1存储奇数 pre2存储偶数
cur为head 一个虚拟节点tmp用作移动
-1   -1      1  -> 2 ->3->4->5
pre1 pre2   cur   tmp
          count=1
-1    -1   1   2 -> 3 -> 4 -> 5
pre1 pre2 cur tmp
        count=1
-1-> 1   -1  2 ->3 ->4->5
pre1 cur    tmp
-1 -> 1   -1  2 -> 3 ->4->5
     pre1    cur tmp


方法2： 采用双指针法 标准解法
  1 -> 2 -> 3 ->4 ->5
 odd  even
 odd.next=even.nxt
  1     ->   3->4->5
 odd    2 ->
        even

        2 ->
        even
  1     ->   3->4->5

            odd
even.next=odd.next
        2 ----->
        even
  1     ->   3->4->5

            odd    even


"""
from typing import *
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head==None:
            return head
        if head.next==None or head.next.next==None: #长度为1或者2
            return head
        pre1,pre2=ListNode(-1),ListNode(-1)
        pre1_head = pre1
        pre2_head = pre2

        cur=head
        count=1
        while cur!=None:
            tmp=cur.next
            cur.next=None
            if count%2==1:#奇数
                #print(cur.val)
                pre1.next=cur
                pre1 = pre1.next
            else:
                pre2.next=cur
                pre2 = pre2.next
            cur=tmp
            count+=1
        new_head=pre1_head.next
        next_head=pre2_head.next
        while pre1_head.next:
            pre1_head=pre1_head.next
        pre1_head.next=next_head
        return new_head

    def oddEvenList1(self,head):
        if head==None:
            return head
        if head.next==None:
            return head
        odd=head #奇数节点
        even=head.next
        next_head=even
        while even!=None and even.next!=None:
            odd.next=even.next
            odd=odd.next

            even.next=odd.next
            even=even.next
        odd.next=next_head
        return head
if __name__=="__main__":
    solution = Solution()
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)
    node5 = ListNode(5)
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5
    node5.next = None
    c_head=solution.oddEvenList1(node1)
    while c_head!=None:
        print(c_head.val)
        c_head=c_head.next