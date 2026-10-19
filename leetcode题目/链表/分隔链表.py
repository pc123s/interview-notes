'''
给你一个头结点为 head 的单链表和一个整数 k ，请你设计一个算法将链表分隔为 k 个连续的部分。
每部分的长度应该尽可能的相等：任意两部分的长度差距不能超过 1 。这可能会导致有些部分为 null 。
这 k 个部分应该按照在链表中出现的顺序排列，并且排在前面的部分的长度应该大于或等于排在后面的长度。
返回一个由上述 k 部分组成的数组。

输入：head = [1,2,3], k = 5
输出：[[1],[2],[3],[],[]]
解释：
第一个元素 output[0] 为 output[0].val = 1 ，output[0].next = null 。
最后一个元素 output[4] 为 null ，但它作为 ListNode 的字符串表示是 [] 。


输入：head = [1,2,3,4,5,6,7,8,9,10], k = 3
输出：[[1,2,3,4],[5,6,7],[8,9,10]]
解释：
输入被分成了几个连续的部分，并且每部分的长度相差不超过 1 。前面部分的长度大于等于后面部分的长度。
'''
from types import *
# Definition for singly-linked list.
from typing import *
import math
import copy
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def calc_listnode_len(self,head):
        count=0
        head1=copy.deepcopy(head)
        while head1:
            head1=head1.next
            count+=1
        return count
    def transnode(self,head):
        while head:
            print(head.val)
            head=head.next
    def splitListToParts(self, head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:
        n=self.calc_listnode_len(head)
        print(n)
        #print(n)
        #self.transnode(head)
        if k>n:
            #将链表分隔成单个的子链表，不够的用null链表填充
            arr=[]
            for i in range(n):
                val=head.val
                head=head.next
                node=ListNode(val)
                arr.append(node)
            for i in range(k-n):
                arr.append(head)
        else:
            arr=[]
            m1=n%k
            m2=n//k

            print(m1,m2)
            head1=ListNode()
            cur,pre=head,None
            for i in range(m1):
                arr.append(cur)
                for j in range(m2+1):
                    pre=cur
                    cur=cur.next
                if pre:
                    pre.next=None
            #将链表分隔，第一个为m1,其余分成m2
            for i in range(k-m1):
                arr.append(cur)
                pre=None
                for j in range(m2):
                    pre = cur
                    cur = cur.next
                if pre:
                    pre.next=None
        return arr

if __name__=="__main__":
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)
    node5 = ListNode(5)
    # node6 = ListNode(6)
    # node7 = ListNode(7)
    # node8 = ListNode(8)
    # node9 = ListNode(9)
    # node10 = ListNode(10)

    node1.next=node2
    node2.next=node3
    node3.next=node4
    node4.next=node5
    # node5.next=node6
    # node6.next=node7
    # node7.next=node8
    # node8.next=node9
    # node9.next=node10
    s=Solution()
    arr=s.splitListToParts(node1,3)
    for node in arr:
        while node:
            print(node.val)
            node=node.next