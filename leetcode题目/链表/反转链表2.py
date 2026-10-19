'''
反转链表 II

给你单链表的头指针 head 和两个整数 left 和 right ，其中 left <= right 。请你反转从位置 left 到位置 right 的链表节点，返回 反转后的链表 。

输入：head = [1,2,3,4,5], left = 2, right = 4
输出：[1,4,3,2,5]
示例 2：

输入：head = [5], left = 1, right = 1
输出：[5]


提示：

链表中节点数目为 n
1 <= n <= 500
-500 <= Node.val <= 500
1 <= left <= right <= n
'''

from typing import *
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def trans_node(self,head):
        while head:
            print(head.val)
            head=head.next
    def reverse_node(self,head,k):
        cur,pre=head,None
        for i in range(k):
            temp = cur.next
            cur.next = pre
            pre = cur
            cur = temp
        return pre,cur
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        cout=1
        temp_head=head
        k=right-left+1
        pre1=None #反转left的前一个node
        behind=None # right的后一个node
        left_node,right_node=None,None
        if k==1:
            return temp_head
        # 对left=1的情况单独对待
        if left==1:
            right_node=head
            head_pre,behind=self.reverse_node(head,k)
            right_node.next=behind
            return head_pre
        # 找出 pre1,behind,left_node,right_node
        while temp_head:
            if cout==left-1:
                pre1=temp_head
                left_node=temp_head.next
            if cout==right:
                right_node=temp_head
                behind=temp_head.next
                break
            temp_head=temp_head.next
            cout+=1
        # 相当于反转整个链表

        cur=left_node
        pre,cur=self.reverse_node(cur,k)
        pre1.next=pre
        left_node.next = behind
        return head

if __name__=="__main__":
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)
    node5 = ListNode(5)
    node6 = ListNode(6)
    node7 = ListNode(7)
    node8 = ListNode(8)
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5
    node5.next = node6
    node6.next = node7
    node7.next = node8
    node8.next = None
    solution=Solution()
    head=solution.reverseBetween(node1,1,8)
    solution.trans_node(head)

