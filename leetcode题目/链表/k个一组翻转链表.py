'''
给你链表的头节点 head ，每 k 个节点一组进行翻转，请你返回修改后的链表。
k 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 k 的整数倍，那么请将最后剩余的节点保持原有顺序。
你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。
输入：head = [1,2,3,4,5], k = 2
输出：[2,1,4,3,5]

输入：head = [1,2,3,4,5], k = 3
输出：[3,2,1,4,5]

采用 start end pre三个指针进行迭代
k=2

 -1  ->  1   ->  2   ->  3  ->  4  ->  5
 pre    start
 end

 -1  ->  1   ->  2   ->  3  ->  4  ->  5
 pre    start
                end     next

-1         1   ->  2      3 -> 4 ->5
pre      start    end    next
-1         2   ->  1      3 -> 4 ->5
pre       end     start    next

-1   ->    2   ->  1  ->  3 -> 4 ->5
pre      start    end    next
-1   ->    2   ->  1  ->  3 -> 4 ->  5
         start    end
                  pre    next


# 这里需要注意指针的赋值
1  2
a  b
a=b 如果a和b是指针的话，其实是a指向b的位置，
1 2
  a


'''
from typing import *
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head==None or head.next==None:
            return head
        # 设置一个虚拟的指针
        vir=ListNode(-1)
        # -1 -> 1 -> 2- >3 ->4
        vir.next=head
        pre=vir
        start=vir.next  #设定一开始的start位置
        end=vir
        while end!=None:
            for i in range(k):
                # 循环时发现end为None说明已经超出界限了
                if end==None:
                    break
                else:
                    end=end.next
            if end==None:
                break

            ## 不为None的情况,设置next指针
            next=end.next

            # 断开中间区域
            pre.next=None
            end.next=None
            # 反转链表,此时start和end的位置已经改变了
            self.reverseListNode(start)

            # #######测试1
            # temp=end
            # while temp!=None:
            #     print("test",temp.val)
            #     temp=temp.next
            # #######测试2
            # temp=start
            # while temp!=None:
            #     print("test1",temp.val)
            #     temp=temp.next

            # print(end.val)


            # 再进行连接
            pre.next=end
            start.next=next

            # 重新进行pre和start end进行赋值
            pre=start
            start=pre.next
            end=pre
        #
        return vir.next

    def reverseListNode(self,head:Optional[ListNode]):
        '''
        None 1->2->3->4
        pre  cur
        None <- 1    2 -> 3 -> 4
        pre    cur  temp
        None <- 1    2 -> 3 -> 4
                pre  cur

        :param head:
        :return:
        '''
        pre=None
        cur=head
        while cur!=None:
            temp=cur.next
            cur.next=pre
            pre=cur
            cur=temp
        return pre
if __name__=='__main__':
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
    pre= solution.reverseKGroup(node1,2)
    while pre!=None:
        print(pre.val)
        pre=pre.next