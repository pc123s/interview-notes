'''
给你一个单链表的头节点 head ，请你判断该链表是否为回文链表。如果是，返回 true ；否则，返回 false 。

输入：head = [1,2,2,1]
输出：true

输入：head = [1,2]
输出：false
回文链表的含义，从左向右看和从右向左看都是一样的
想法，设置一个虚拟节点
 1  ->  2 -> 3 -> 3 -> 3 -> 2 -> 1
cur                             end_cur

三个节点 pre cur next pre和cur来反转链表， next来比较和cur的值，如果相等就存下来
方法1：从左到右遍历一遍。 arr记录下来，然后反转对比一样就是回文 （笨办法）
方法2：使用快慢指针的方法，
slow 为慢指针每次走一步
fast 为快指针每次走两步
当fast为None的时候有两种
当链表为奇数
1->2-> 3 -> 2 -> 1
      slow         fast

1-> 2  ->  2 -> 1
   slow        fast
1-> 2 ->2 -> 2 ->2 -> 1
       slow          fast
此时slow对应的链表 以前的链表 和 之后的链表（反转） 遍历应该值完全一样

1-> 2     2 -> 1
   slow        fast
1-> 2 ->2  2 ->2 -> 1
       slow          fast


'''
from typing import *
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        if head==None:
            return False
        # 一个长度的链表
        if head.next==None:
            return False
        tmp=head
        slow=head
        fast=head
        triger=1
        while True:
            if fast.next==None:
                # 偶数
                triger=1
                break
            if fast.next.next==None:
                # 奇数
                triger=2
                break
            slow=slow.next
            fast=fast.next.next
        #设置左右节点
        rightHead,leftHead=None,None
        if triger==1:
            rightHead = slow.next
            slow.next=None
            leftHead = self.reverseList(tmp)
            leftHead=leftHead.next
        else: #偶数
            rightHead=slow.next
            slow.next=None
            leftHead=self.reverseList(tmp)

        while leftHead!=None:
            print("line61",leftHead.val,rightHead.val)
            if leftHead.val!=rightHead.val:
                return False
            leftHead=leftHead.next
            rightHead=rightHead.next

        return True
    def isPalindrome1(self, head: Optional[ListNode]) -> bool:
        if head==None:
            return False
        # 一个长度的链表
        if head.next==None:
            return False
        # 设置两个节点
        slow=head
        fast=head

        # 当fast走到末尾时
        while fast.next!=None and fast.next.next!=None:
            slow=slow.next
            fast=fast.next.next
        #设置左右节点
        # 无论奇数 偶数都反转右边
        tmp=slow.next
        # 反转右边。
        rightHead=self.reverseList(tmp)
        leftHead=head
        # 奇数右边短一点
        while rightHead!=None:
            print("line61",leftHead.val,rightHead.val)
            if leftHead.val!=rightHead.val:
                return False
            leftHead=leftHead.next
            rightHead=rightHead.next

        return True

    def reverseList(self,head):
        '''
        反转链表
        :param head:
        :return:
        None    1 -> 2 -> 3 -> 4 ->5
        pre    cur
        设立一个tmp节点
        '''
        if head==None:
            return head
        if head.next==None:
            return head
        pre=None
        cur=head
        while cur!=None:
            tmp=cur.next
            cur.next=pre
            pre=cur
            cur=tmp
        return pre

if __name__=="__main__":
    solution = Solution()
    node1 = ListNode(1)
    node2 = ListNode(1)
    node3 = ListNode(3)
    node3_1 = ListNode(3)
    node4 = ListNode(2)
    node5 = ListNode(1)
    node1.next = node2
    node2.next = node3
    #node3.next = node3_1
    node3.next = node4
    node4.next = node5
    node5.next = None
    #head=solution.reverseList(node1)
    # while head!=None:
    #     print(head.val)
    #     head=head.next
    print(solution.isPalindrome1(node1))