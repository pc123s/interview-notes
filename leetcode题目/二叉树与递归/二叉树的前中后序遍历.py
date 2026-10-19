'''
给你二叉树的根节点 root ，返回它节点值的 前序 遍历。

输入：root = [1,null,2,3]
输出：[1,2,3]
示例 2：

输入：root = []
输出：[]
示例 3：

输入：root = [1]
输出：[1]

树中节点数目在范围 [0, 100] 内
-100 <= Node.val <= 100

进阶：递归算法很简单，你可以通过迭代算法完成吗？

方法1：递归，
递归的方法很简单，但是递归会存在python的压栈的问题，如果二叉树特别深的话是通不过的，可以看看非递归，迭代的思路

二叉树遍历 前序是：中左右 中序：左中右 后续：左右中

方法2：
迭代的方式：
           1
        /     \
       2       3
      / \       \
     4  5        6

用node记录当前节点，当前节点分别有 left right up三种状态，用栈来记录路径
这里以后续遍历为例
stack=[]
postL=[]
node=1 state=left
stack=[1]
node=2 state=left
stack=[1,2]
node=4 node.left=None state=right node.right=None state=up
state=up

postL=[4]
对stack出栈 stack=[1] parrent=2
2.left=4
node=2 state=right stack=[1,2]
node=5,state=left stck=[1,2]
node=5  node.left=None, node.right=None, state=up
state=up
postL=[4,5]

对stack出栈，stack=[1] parrent=2
2.left!=5, 说明右边也走完了，继续出栈
node=2,state=up,stack=[],parrent=1
1.left=2.state=right,node=1
node=1,state=right,stack=[3]
node=1,state=up,stack=[3]
postL=[4,5,1]

stack出栈，stack=[],parrent=3
3.left!=1,node=6,state

迭代的方式：
           1
        /     \
       2       3
      / \       \
     4  5        6
arr=[]
stack=[]
stack=[1] state=[[F,F,F]]
向左，state[-1].left=True, stack=[1,2],加入一个state
stack=[1,2] state=[[T,F,F],[F,F,F]],
向左 node=4 state[-1].left=True,stack=[1,2,4],加入一个state
stack=[1,2,4],state=[[T,F,F],[T,F,F],[F,F,F]]
向左 stack[-1].left=None state[-1].left=True. 向右 stack[-1].right=None state[-1].right=True.
否则 state[-1].left==True and state[-1].left==True, stack.pop() state.pop() 记录 arr=[4],继续判断

'''
from typing import *
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class state:
    def __init__(self):
        self.left=False
        self.right=False
class Solution:
    def __init__(self):
        self.traver_lis=[]
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root==None:
            return self.traver_lis
        def dfs(root):
            if root==None:
                return None
            self.traver_lis.append(root.val)
            dfs(root.left)
            dfs(root.right)
        dfs(root)
    def midTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root==None:
            return self.traver_lis
        def dfs(root):
            if root==None:
                return
            dfs(root.left)
            self.traver_lis.append(root.val)
            dfs(root.right)
        dfs(root)
        return self.traver_lis

    def backTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root==None:
            return self.traver_lis
        def dfs(root):
            if root==None:
                return
            dfs(root.left)
            dfs(root.right)
            self.traver_lis.append(root.val)
        dfs(root)
        return self.traver_lis

    def backTraversal1(self,root: Optional[TreeNode])->List[int]:
        if not root:
            return []

        node=root
        #设置几个状态
        leftstate=100
        rightstate=200
        upstate=300
        stack=[] #用栈来记录路径
        back_l=[] #记录后续遍历的节点
        nodestate=leftstate #初始
        while node:
            if nodestate==leftstate:
                if node.left:
                    stack.append(node)
                    nodestate=leftstate
                    node=node.left
                else:#左子树为空，状态变为右子树
                    nodestate=rightstate
            elif nodestate==rightstate:
                if node.right:
                    stack.append(node)
                    node=node.right
                    # 将其默认设为左子树遍历
                    nodestate=leftstate
                else:
                    nodestate=upstate
            else:#来到中间值了
                parent=None #设置一个None值
                back_l.append(node.val)
                #print(back_l)
                if stack:
                    parent=stack.pop()
                    if parent.left==node:
                        # 说明左子树遍历过了
                        nodestate=rightstate
                    else:#左右子树都遍历过了
                        nodestate=upstate

                    #else: #没有左子树，走的右子树

                node=parent
        return back_l
    def backTraversal2(self,root: Optional[TreeNode])->List[int]:
        if not root:
            return []
        stack_node=[root]
        stack_state=[state()]
        arr=[]
        arr1=[]
        arr2=[]
        while stack_node:
            c_state=stack_state[-1]
            c_node=stack_node[-1]
            if c_state.left==False:
                arr1.append(c_node.val)
                if c_node.left:
                    stack_state[-1].left=True
                    stack_node.append(c_node.left)
                    stack_state.append(state())
                else:
                    stack_state[-1].left=True
            elif c_state.right==False:
                arr2.append(c_node.val)
                if c_node.right:
                    stack_state[-1].right=True
                    stack_node.append(c_node.right)
                    stack_state.append(state())
                else:
                    stack_state[-1].right=True
            elif c_state.right and c_state.left:
                node=stack_node.pop()
                stack_state.pop()
                arr.append(node.val)
            else:
                pass
        print(arr1)
        print(arr2)
        print(arr)
        return arr






if __name__=="__main__":
    node1 = TreeNode("A")
    node2 = TreeNode("B")
    node3 = TreeNode("C")
    node4 = TreeNode("D")
    node5 = TreeNode("E")
    node6 = TreeNode("F")
    node7 = TreeNode("G")
    node8 = TreeNode("H")
    node9 = TreeNode("I")

    node1.left=node2
    node1.right=node3
    node2.left=node4
    node2.right=node5
    node4.left=node6
    node4.right=node7
    node7.left = node8
    node7.right = node9


    solution=Solution()
    if False:
        solution.preorderTraversal(node1)
        print(solution.traver_lis)
        solution.traver_lis=[]
        solution.midTraversal(node1)
        print(solution.traver_lis)
        solution.traver_lis=[]
        solution.backTraversal(node1)
        print(solution.traver_lis)
    if True:
        res=solution.backTraversal1(node1)
        print(res)
    if True:
        res=solution.backTraversal2(node1)
        print(res)
