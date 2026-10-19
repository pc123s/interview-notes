'''
给你一个字符串 s ，考虑其所有 重复子串 ：即 s 的（连续）子串，在 s 中出现 2 次或更多次。这些出现之间可能存在重叠。
返回 任意一个 可能具有最长长度的重复子串。如果 s 不含重复子串，那么答案为 "" 。

输入：s = "banana"
输出："ana"
ana是其中的一个子串，且重复了两次

示例 2：

输入：s = "abcd"
输出：""

先看暴力法
首先确定一个start和length
length初始化为1
bnana，递增的求后续的数组是否在后一个子串中。
s=banana
i=0, sub=s[i:i+length]=b b是否在anan中
i=1, sub=s[i:i+length]=a a是否在nana中
发现在，ok,length+=1
length=2,sub=an,在
length=3,sub=ana,在（记录i和start）
lenth=4,sub=anan，不在打破循环，记录这个值
复杂度O（n2）

方法2：https://leetcode.cn/problems/longest-duplicate-substring/solutions/2558849/python-7chong-jie-fa-he-ji-han-hou-zhui-lh03v/
'''
from  typing import *
class Solution:
    def longestDupSubstring(self, s: str) -> str:
        start, length = 0, 1
        for i in range(len(s)):
            while s[i : i+length] in s[i+1 : ]:
                start = i
                length += 1
        res=s[start: start + length - 1]
        print(res)
        return res
    def suffixArray(self,s: str) -> (List[int], List[int], List[int]):
        n = len(s)
        sa = sorted(range(n), key=lambda i: s[i:])
        print(sa)
        '''
        sa=[5, 3, 1, 0, 4, 2]
        arr = [s[i:] for i in range(n)]
        print(arr)
        ['banana', 'anana', 'nana', 'ana', 'na', 'a']
        arr.sort()
        print(arr)
        ['a', 'ana', 'anana', 'banana', 'na', 'nana']
        sa[i] 子串排序为i的子串以前在数组子串的中的位置
        print(rk)
        [3, 2, 5, 1, 4, 0]
        '''
        rk = [0] * n
        for i in range(n):
            rk[sa[i]] = i
        print(rk)
        height = [0] * n
        k = 0
        s += '#'
        for i in range(n):
            if rk[i]:
                if k > 0:
                    k -= 1
                while s[i + k] == s[sa[rk[i] - 1] + k]:
                    k += 1
                height[rk[i]] = k

        return rk, sa, height
    def longestDupSubstring1(self, s: str) -> str:
        rk, sa, height = self.suffixArray(s)
        mh = max(height)
        start = sa[height.index(mh)]
        return s[start : start + mh]

if __name__=="__main__":
    solution=Solution()
    if False:
        s="banana"
        solution.longestDupSubstring(s)
        s="bananananan"
        solution.longestDupSubstring(s)
    if True:
        s="banana"
        solution.suffixArray(s)