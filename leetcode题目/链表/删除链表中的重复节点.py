'''
删除链表中重复的结点
https://www.nowcoder.com/exam/oj/ta?page=1&tpId=13&type=13
输入：
{1,2,3,3,4,4,5}
返回值：
{1,2,5}
输入：
{1,1,1,8}
返回值：
{8}
链表默认值从小到大

思路：采用hash表进行存储。pre和cur.pre指向cur.如果发现存在于hash表中，则移动cur指针.否则pre.next=cur

-1   1  2  3  3  4  4  5
pre cur
1 {1}
-1-> 1
pre cur
2 {1 2}
-1-> 1  -> 2
     pre  cur

3 {1 2 3}
-1-> 1  -> 2 -> 3
          pre  cur

3 {1 2 3} 重复 cur=cur.next
-1-> 1  -> 2 -> 3 ->3
          pre      cur
4 {1 2 3} 非重复
-1-> 1  -> 2 -> 4
          pre  cur
pre.next=cur
4 {1 2 3 4} 非重复
-1-> 1  -> 2 -> 4->5
          pre     cur

這種方法的话会，会让重复的也在其中，正确的是利用双指针去进行排除 pre cur cur_nex三个指针

当发现cur和cur_next的值是一样的，让cur移动，知道 cur和cur_next不一致。 此时pre.nex=cur_next
-1   1  2  3  3  4  4  5
-1  1  2
p   c c_n
-1  1  2  3
    p  c c_n
-1  1  2  3  3
       p  c c_n
-1  1  2  3  3  4
       p     c c_n


'''

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
class Solution:
    def deleteDuplication(self , pHead: ListNode) -> ListNode:
        '''
        1 2 3 3 4 5
        :param pHead:
        :return:
        '''
        # write code here
        if pHead == None:
            return None
        res = ListNode(0)
        # 在链表前加一个表头
        res.next = pHead
        cur=pHead
        pre=res
        while cur!=None and cur.next!=None:
            if cur.val==cur.next.val:
                while cur and cur.next:
                    if cur.val!=cur.next.val:
                        break
                    else:
                        cur=cur.next
                pre.next=cur.next
                cur=cur.next
            else:
                pre=cur
                cur=cur.next
        # 返回时去掉表头
        return res.next

    def deleteDuplication_pc(self, pHead: ListNode) -> ListNode:
        # write code here
        pre1 = pre = ListNode(-1)
        cur = pHead
        d = {}
        while cur:
            if cur.val not in d:
                d[cur.val] = 1
                pre.next = cur
                pre = cur
                cur = cur.next
            else:
                cur = cur.next
        pre.next = cur
        return pre1.next
    def tranverseNode(self,head):
        while head:
            print(head.val)
            head=head.next

if __name__=="__main__":
    if False:
        node1 = ListNode(1)
        node2 = ListNode(2)
        node3 = ListNode(3)
        node4 = ListNode(3)
        node5 = ListNode(4)
        node6 = ListNode(5)
        node1.next=node2
        node2.next=node3
        node3.next=node4
        node4.next=node5
        node5.next=node6
        solution=Solution()
        node_=solution.deleteDuplication(node1)
        solution.tranverseNode(node_)
    if True:
        node1 = ListNode(1)
        node2 = ListNode(2)
        node3 = ListNode(3)
        node4 = ListNode(3)
        node5 = ListNode(4)
        node6 = ListNode(4)
        node7 = ListNode(5)

        node1.next=node2
        node2.next=node3
        node3.next=node4
        node4.next=node5
        node5.next=node6
        node6.next=node7

        solution=Solution()
        node_=solution.deleteDuplication(node1)
        solution.tranverseNode(node_)