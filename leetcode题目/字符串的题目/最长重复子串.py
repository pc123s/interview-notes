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

banana的后缀数组为
b
anana
nana
ana
na
a
排序后为
a
ana
anana
banana
na
nana
那么这个重复子串就在这个相邻的字符串之中,且有公共前缀
现在问题转化为怎么快速求数组的最长公共前缀了。这个就要用到后缀数组。
其中后缀数组的几个概念：
rank[i] 代表以i开头的后缀数组在排序完成以后在排序数组的位置
sa[i] 代表排序完成以后，第i个排序数组在原先后缀数组的位置
有sa[rank[i]]=rank[sa[i]]=i
后缀数组：
['banana', 'anana', 'nana', 'ana', 'na', 'a']
排序数组：
['a', 'ana', 'anana', 'banana', 'na', 'nana']
rk=[3, 2, 5, 1, 4, 0]
sa=[5, 3, 1, 0, 4, 2]
height 数组的定义
lcp最大公共前缀
height[i]=lcp(sa[i],sa[i-1])
即第 i 名的后缀与它前一名的后缀的最长公共前缀
并且 height[rk[i]]>=height[rk[i-1]]-1
做法：
每次求i开头的前缀 和 sa[rk[i]-1]开头的前缀
k=0
比如i=0
对应i=0 和 i=1的前缀
banana anana
相同就k++,否则跳出 这里没有相同k=0 height[rank[0]]=height[3]=0
继续比较
i=1
对应i=1 和 i=3
anana 和 ana
k=0,比较k=3
height[rank[1]]=height[2]=3
i=2
k=2（根据引理从2开始计算就行）
对应i=2 和 i=4
nana na

后缀数组 lcp:https://zhuanlan.zhihu.com/p/574091889
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
                print(i+k,sa[rk[i] - 1]+k)
                print(s[sa[rk[i] - 1]+k])
                while s[i + k] == s[sa[rk[i] - 1] + k]:
                    k += 1
                height[rk[i]] = k

        return rk, sa, height
    def longestDupSubstring1(self, s: str) -> str:
        rk, sa, height = self.suffixArray(s)
        mh = max(height)
        start = sa[height.index(mh)]
        return s[start : start + mh]
    def longestDupSubstring2(self,s:str)->str:
        n=len(s)
        arr=[s[i:] for i in range(n)]
        arr.sort()
        rank_dic={} #记录之前位置的字典
        for i in range(n):
            rank_dic[s[i:]]=i
        rank_dic=dict(sorted(rank_dic.items(),key=lambda k:k[0]))
        print(rank_dic)
        print(arr)
        max_Len=-9999
        maxSubstr=""
        for i in range(n-1):
            s1=arr[i]
            s2=arr[i+1]
            if len(s1)>len(s2):
                s1,s2=s2,s1
            k=len(s1)
            for j in range(k):
                if s1[j]==s2[j]:
                    j+=1
                else:
                    break
            if j>max_Len:
                maxSubstr=s1[:j]
                max_Len=j
            # if s1 in s2:
            #     print(s1,s2)
            #     k=s2.index(s1)
            #     print(rank_dic[s1],rank_dic[s2]+k)
            #     if rank_dic[s1] != (rank_dic[s2]+k):
            #         if len(s1)>max_Len:
            #             maxSubstr=s1
            #             max_Len=len(s1)
        print(maxSubstr)
        return maxSubstr

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
    if True:
        s="nnpxouomcofdjuujloanjimymadkuepightrfodmauhrsy"
        solution.longestDupSubstring2(s)