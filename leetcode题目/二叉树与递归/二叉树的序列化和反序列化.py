'''
297. 二叉树的序列化与反序列化

输入：root = [1,2,3,null,null,4,5]
输出：[1,2,3,null,null,4,5]
示例 2：

输入：root = []
输出：[]
示例 3：

输入：root = [1]
输出：[1]
示例 4：

输入：root = [1,2]
输出：[1,2]

方法1：序列化，用list存储，采用完全二叉树的形式，如果是None则也记录
                           5
                         /   \
                        2     6
                       /     / \
                      1     4   8
                           /   / \
                          3   7   9

二叉树以这种形式存储

5 2 1 None None None 6 4 3 None None None 8 7 None None 9 None None
反序列化采用递归的方式实现，但是需要注意的是进行反序列化的时候，需要返回对应的索引，否则索引没更新的话递归的值会失败


'''

from typing import *

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """

        arr=[]
        def dfs(root):
            if not root:
                arr.append("None")
                return arr
            arr.append(str(root.val))
            dfs(root.left)
            dfs(root.right)
        dfs(root)
        return " ".join(arr)

    def deserialize(self, data:str):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        l=data.split(" ")
        if not l:
            return None
        l1=[int(i) if i!='None' else None for i in l]
        if len(l1)==1:
            return TreeNode(l1[0])
        def deserialize1(l,index):
            if l[index]==None:
                return None,index
            root=TreeNode(l[index])
            node,index=deserialize1(l,index+1)
            root.left=node
            node,index=deserialize1(l,index+1)
            root.right=node
            return root,index
        root,index=deserialize1(l1,0)
        return root
if __name__=="__main__":
    code=Codec()
    node1 = TreeNode(1)
    node2 = TreeNode(2)
    node3 = TreeNode(3)
    node4 = TreeNode(4)
    node5 = TreeNode(5)
    node6 = TreeNode(6)
    node7 = TreeNode(7)
    node8 = TreeNode(8)
    node9 = TreeNode(9)
    node5.left = node2
    node5.right = node6
    node2.left = node1
    node6.left = node4
    node6.right = node8
    node4.left = node3
    node8.left = node7
    node8.right = node9
    l=code.serialize(node5)
    print(l)
    root=code.deserialize(l)
    print(root)
    def dfs(root):
        if not root:
            return
        print(root.val)
        dfs(root.left)
        dfs(root.right)
    dfs(root)