'''
解法1：
双指针
例如
None  1    ->  2  ->  3  ->  4  -> 5  -1
 pre  cur                             next
None  1    ->  2  ->  3  ->  4  -> 5
 pre  cur     next

None <-  1      2  ->  3  ->  4  -> 5
 pre    cur    next
None <-  1      2  ->  3  ->  4  -> 5
                      next
        pre    cur
None <-  1  <- 2       3  ->  4  -> 5
                      next
        pre    cur
...
None <-  1  <- 2  <-3  <- 4 <- 5
                                          next
                        pre   cur

解法2：
 1->2->3->4->5    None
cur                pre
 1->  2 -> 3  -> 4  -> 5   None
cur  tmp                    pre

None <-     1    2 -> 3  -> 4  -> 5
pre        cur  tmp
pre和cur前移
None <-     1    2 -> 3  -> 4  -> 5
pre        cur  tmp
           pre  cur

'''
from types import *
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        # cur 记录当前迭代到哪个链表了
        # 以指针的形式迭代 cur->pre这样的指针形式来迭代所有的数据
        cur=head
        pre=None
        while cur!= None:
            tmp=cur.next
            cur.next=pre
            pre=cur
            cur=tmp
        return pre
    def reverseList_pc(self, head: ListNode) -> ListNode:
        # cur 记录当前迭代到哪个链表了
        # 以指针的形式迭代
        current=head
        arr=[]
        while current!=None:
            arr.append(ListNode(current.val))
            current=current.next

        arr1=arr[::-1]

        for i in range(len(arr1)-1):
            j=i+1
            node1=arr[i]
            node2=arr[j]
            node1.next=node2
        if node2:
            node2.next=None
        head = arr1[0]
        return head

    def reverseList_pc2(self, head: ListNode) -> ListNode:
        '''
                 1 -> 2 -> 3 -> 4 -> 5
         pre    cur
         None <- 1    2 -> 3 -> 4 -> 5
         pre    cur  tmp
         None <- 1    2 -> 3 -> 4 -> 5
                pre  cur


        :param head:
        :return:
        '''
        if head==None:
            return head
        if head.next==None:
            return head
        pre=None
        cur=head
        while cur:
            tmp=cur.next
            cur.next=pre
            pre=cur
            cur=tmp
        return pre



# 定义一个示例链表
def traverse_linked_list(head):
    current = head
    while current is not None:
        print(current.val)  # 打印当前节点的值
        current = current.next  # 移动到下一个节点
if __name__=="__main__":
    solution=Solution()
    node1=ListNode(1)
    node2=ListNode(2)
    node3=ListNode(3)
    node4=ListNode(4)
    node5=ListNode(5)
    node1.next=node2
    node2.next=node3
    node3.next=node4
    node4.next=node5
    node5.next=None

    #traverse_linked_list(node1)
    #print(node1.val)
    node=Solution().reverseList_pc2(node1)
    traverse_linked_list(node)

