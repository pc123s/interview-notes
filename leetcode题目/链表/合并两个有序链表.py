'''
https://leetcode.cn/problems/merge-two-sorted-lists/description/
输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]
示例 2：

输入：l1 = [], l2 = []
输出：[]
示例 3：

输入：l1 = [], l2 = [0]
输出：[0]

思路：设置双指针法，一个指向链表1 a 一个指向链表2 b
1 2 4
a
1 3 4
b

用一个虚拟指针拼接， 较小的先拼接，指针后移，其余不动
-1
1 2 4
a
1 3 4
b
a<=b     -1->1
1 2 4
  a
1 3 4
b
b<a -1->1->1
以此类推
'''
from typing import *
import copy
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        pre1=pre=ListNode(-1)
        #pre1=pre
        a=list1
        b=list2
        while a and b:
            if a.val<=b.val:
                pre.next=a
                a=a.next
            else:
                pre.next=b
                b=b.next
            pre=pre.next

        if a:
            pre.next=a
        if b:
            pre.next=b
        return pre1.next
    def tranverseNode(self,head):
        while head:
            print(head.val)
            head=head.next
if __name__=="__main__":
    node1=ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(4)
    node4 = ListNode(1)
    node5 = ListNode(3)
    node6 = ListNode(4)
    node1.next=node2
    node2.next=node3
    node4.next=node5
    node5.next=node6
    solution=Solution()
    head=solution.mergeTwoLists(node1,node4)
    solution.tranverseNode(head)
