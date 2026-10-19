'''
给定一个链表，返回链表开始入环的第一个节点。 从链表的头节点开始沿着 next 指针进入环的第一个节点为环的入口节点。如果链表无环，则返回 null。
为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。注意，pos 仅仅是用于标识环的情况，并不会作为参数传递到函数中。
说明：不允许修改给定的链表。
输入：head = [3,2,0,-4], pos = 1
输出：返回索引为 1 的链表节点
解释：链表中有一个环，其尾部连接到第二个节点。

输入：head = [1,2], pos = 0
输出：返回索引为 0 的链表节点
解释：链表中有一个环，其尾部连接到第一个节点。

思路：怎么判断是否有环呢，我的思路是从头遍历这个链表，记录每次的值，后续遍历时如果发现前面的值存在就存在环，这种思路发现不行，环是一段连续的值一样
方法1：哈希表寻找
这种使用python的list直接遍历就行寻找就行
方法2：快慢指针
slow和fast指针
https://leetcode.cn/problems/c32eOV/solutions/980499/shua-chuan-jian-zhi-offer-day12-lian-bia-lv78/
详见题解
https://leetcode.cn/problems/c32eOV/solutions/977000/jian-zhi-offer-ii-022-lian-biao-zhong-hu-8f1m/

'''
from types import *

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def trans_node_n(self,head,n):
        cout=0
        while head:
            if cout==n:
                return head
            head=head.next
            cout+=1
    def get_n_nodeval(self,head,k):
        cout=0
        arr=[]
        while head:
            arr.append(head.val)
            head=head.next
            cout+=1
            if k==cout:
                break
        return arr
    def trans_node_100(self,head):
        cout=0
        while head:
            print(head.val)
            head=head.next
            cout+=1
            if cout==100:
                break

    def detectCycle(self, head: ListNode) -> ListNode:
        # 使用哈希表
        seen = []

        while head:
            if head in seen:
                return head
            else:
                seen.append(head)
            head = head.next

        return None
    def detectCycle1(self, head: ListNode) -> ListNode:
        #双指针
        slow=head
        fast=head
        while fast and fast.next:
            fast=fast.next.next
            slow=slow.next
            if fast==slow:
                print(fast.val, slow.val)
                temp=head
                while temp!=slow:
                    temp=temp.next
                    slow=slow.next
                return temp
        return None


if __name__=="__main__":
    node1=ListNode(3)
    node2=ListNode(2)
    node3=ListNode(0)
    node4=ListNode(-4)
    node1.next=node2
    node2.next=node3
    node3.next=node4
    node4.next=node2
    s=Solution()
    s.detectCycle1(node1)
