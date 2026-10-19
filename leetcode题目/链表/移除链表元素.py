'''
给你一个链表的头节点 head 和一个整数 val ，请你删除链表中所有满足 Node.val val 的节点，并返回 新的头节点 。


输入：head = [1,2,6,3,4,5,6], val = 6
输出：[1,2,3,4,5]
示例 2：

输入：head = [], val = 1
输出：[]
示例 3：

输入：head = [7,7,7,7], val = 7
输出：[]

移除的节点有两种情况。
1、移除的是头节点
2、移除的是其它节点
对于移除其它节点这种情况，我们可以让它的前一个节点指向移除节点的下一节点来解决。


'''
from typing import *


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        # 需要移除的是头节点
        if head==None:
            return None
        # 建一个虚拟的ListNode
        virtualNode=ListNode(-1)

        virtualNode.next=head

        # 设置一个指针，指向此时的虚拟节点
        # pre：-1->1->1->2

        pre=virtualNode
        cur=head
        while cur!=None:
            if cur.val==val:
                # 如果相等就让虚拟的头节点等于下个节点
                pre.next=cur.next
            else:
                # 让pre后移一个位置
                pre=cur


            # 不断的移动节点
            cur=cur.next
        #遍历所有的节点以后，返回虚拟节点的下一个节点

        return virtualNode.next

    def tranverseNode(self,head:Optional[ListNode])->List[int]:
        arr=[]
        while head!=None:
            arr.append(head.val)
            head=head.next
        print(arr)
        return arr

if __name__=='__main__':
    node1=ListNode(1)
    node2=ListNode(2)
    node3=ListNode(2)
    node4=ListNode(3)
    node5=ListNode(4)
    node6=ListNode(5)

    node1.next=node2
    node2.next=node3
    node3.next=node4
    node4.next=node5
    node5.next=node6
    solution=Solution()
    node=solution.removeElements(node1,2)
    solution.tranverseNode(node)





