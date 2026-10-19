'''
给定两个字符串 s 和 p，找到 s 中所有 p 的 变位词 的子串，返回这些子串的起始索引。不考虑答案输出的顺序。

变位词 指字母相同，但排列不同的字符串。



示例 1：

输入: s = "cbaebabacd", p = "abc"
输出: [0,6]
解释:
起始索引等于 0 的子串是 "cba", 它是 "abc" 的变位词。
起始索引等于 6 的子串是 "bac", 它是 "abc" 的变位词。
 示例 2：

输入: s = "abab", p = "ab"
输出: [0,1,2]
解释:
起始索引等于 0 的子串是 "ab", 它是 "ab" 的变位词。
起始索引等于 1 的子串是 "ba", 它是 "ab" 的变位词。
起始索引等于 2 的子串是 "ab", 它是 "ab" 的变位词。
思路1：
使用p长度的一个滑动窗口，对p和滑动窗口进行排序，如果存在就用arr添加
s="cbaebabacd" p="abc"
i=0 j=3
c b a e b a b a c d  abc
i     j
cba->abc
abc==abc arr.append(0)
c b a e b a b a c d  abc
  i     j
abe abc!=abe i+=1 j+=1
这种方法也可以，但是会发现时间复杂度过高

'''
from typing import *
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        arr1, arr2, lg, ret = [0] * 26, [0] * 26, len(p), []
        if lg > len(s):
            return []
        for i in range(lg):
            arr1[ord(p[i]) - ord('a')] += 1
            arr2[ord(s[i]) - ord('a')] += 1
        print(arr1)
        print(arr2)
        if arr1 == arr2:
            ret.append(0)
        for i in range(lg,len(s)):
            arr2[ord(s[i]) - ord('a')] += 1
            arr2[ord(s[i - lg]) - ord('a')] -= 1
            if arr1 == arr2:
                ret.append(i - lg + 1)
        return ret
    def findAnagrams1(self, s: str, p: str) -> List[int]:
        m=len(p)
        n=len(s)
        if len(p)>len(s):
            return []
        arr=[]
        p_="".join(sorted(p))
        for i in range(n-m+1):
            s_=s[i:i+m]
            s1="".join(sorted(s_))
            if s1==p_:
                arr.append(i)
        return arr

if __name__=="__main__":
    solution=Solution()
    if True:
        s="cbaebabacd"
        p="abc"
        arr=solution.findAnagrams(s,p)
        print(arr)
    if True:
        s = "abab"
        p = "ab"
        arr = solution.findAnagrams1(s, p)
        print(arr)