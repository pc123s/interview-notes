'''
示例 1：

输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
解释：链表数组如下：
[
  1->4->5,
  1->3->4,
  2->6
]
将它们合并到一个有序链表中得到。
1->1->2->3->4->4->5->6
示例 2：

输入：lists = []
输出：[]
示例 3：

输入：lists = [[]]
输出：[]

1、暴力法
每次比较list中的node，选择其中最小值向pre插入（pre为一个-99999的指针，）每次每次选用cur指标代表当前节点，next代表下一节点
如果cur.val比pre小，则 cur->None next->... pre加入cur，否则 cur->next(还原)
没迭代一次将pre后移。当list所有为None遍历结束。

2、遍历排序

x 每次用一个新的节点-1 对两个listNode循环比较，比如 大的后插入，小的先插入。将其接在新的节点之后


'''
from typing import *
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        pre=ListNode(-999999999)
        bkpre = pre
        n=len(lists)
        while not all(i==None for i in lists):
            index=0 #记录当前循环的最小值
            minNum=999999999999
            for i in range(n):

                if lists[i] and lists[i].val <minNum:

                    index=i
                    minNum=lists[i].val

            #print(index)
            cur=lists[index]
            next=cur.next
            cur.next=None
            pre.next=cur
            lists[index]=next
            pre=pre.next

        return bkpre.next

    def mergeKLists1(self, lists: List[ListNode]) -> ListNode:
        x = None
        for y in lists:
            x = self.merge(x, y)
        return x

    def merge(self, a: ListNode, b: ListNode) -> ListNode:
        dummy = ListNode(-1)
        x = dummy
        while a and b:
            if a.val < b.val:
                x.next = a
                a = a.next
            else:
                x.next = b
                b = b.next
            x = x.next
        if a:
            x.next = a
        if b:
            x.next = b
        return dummy.next



if __name__=="__main__":
    solution=Solution()
    node1=ListNode(2)
    node2 = ListNode(3)
    node3=ListNode(1)
    node4=ListNode(2)
    node1.next=node2
    arr=[node1,node3,node4]
    res=solution.mergeKLists1(arr)
    while res:
        print(res.val)
        res=res.next