'''
https://leetcode.cn/problems/3u1WK4/description/

https://leetcode.cn/problems/3u1WK4/ 具体题目详见这个
这道题比较容易想到的是，创建一个hash表，然后循环依次A，将A的所有节点添加至Hash表中。 再循环依次B，每次判断B的当前节点是否在hash表中。 代码如下：

作者：清风Python
链接：https://leetcode.cn/problems/3u1WK4/solutions/980575/shua-chuan-jian-zhi-offer-day12-lian-bia-m5nz/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
方法1：是采用哈希表的方式进行查找的

1->1->4->3->2->1

1->2->

方法2：利用hash表的话空间复杂度为O(n)，如果要用O（1）的方法的话可以用另一种方法
假设相交前A链表的长度为x,B链表的长度为z
两个链表相交的点为图中的w
相交后共同的长度为y。
我们分别创建p1、p2两个指针指向A、B
当p1或者p2走到头时，则将指针重新指向另外的一个链表。
当p1、p2相等时终止，返回p1或p2就是第一个相交节点。
因为p1、p2走过的路程都是x+y+z！

即如果两个链表有交点的话一定是在整个w，那么两个链表所走过的路程一定是相等的

作者：清风Python
链接：https://leetcode.cn/problems/3u1WK4/solutions/980575/shua-chuan-jian-zhi-offer-day12-lian-bia-m5nz/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        d = {}
        while headA:
            d[headA] = headA
            headA = headA.next
        while headB:
            if d.get(headB):
                return headB
            headB = headB.next
        return None
    def getIntersectionNode1(self, headA: ListNode, headB: ListNode) -> ListNode:
        x,y=headA,headB
        while x!=y:
            if x:
                x=x.next
            else:
                x=headB
            if y:
                y=y.next
            else:
                y=headA
        return x

if __name__=="__main__":
    node1=ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)
    node5 = ListNode(5)
    node6 = ListNode(6)
    node7 = ListNode(7)
    node8 = ListNode(8)
    node1.next=node2
    node2.next = node3
    node3.next = node4
    node4.next = node5
    node5.next = node6
    node7.next = node5
    node=Solution().getIntersectionNode(node1,node7)
    print(node.val)
    node=Solution().getIntersectionNode1(node1,node7)
    print(node.val)
