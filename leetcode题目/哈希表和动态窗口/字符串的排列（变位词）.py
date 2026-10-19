'''
给定两个字符串 s1 和 s2，写一个函数来判断 s2 是否包含 s1 的某个变位词。

换句话说，第一个字符串的排列之一是第二个字符串的 子串 。

示例 1：

输入: s1 = "ab" s2 = "eidbaooo"
输出: True
解释: s2 包含 s1 的排列之一 ("ba").
示例 2：

输入: s1= "ab" s2 = "eidboaoo"
输出: False
https://leetcode.cn/problems/MPnaiL/description/


两种思路：
1、对s1进行全排列，然后一个一个在s2找，找到就有
思路2：hash表 滑动窗口
2、利用hash表加滑动窗口去找。
'''
import collections
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        m, n = len(s1), len(s2)
        if m > n:
            return False
        cnt = collections.Counter(s1)  # 哈希表：记录需要匹配到的各个字符的数目
        need = m  # 记录需要匹配到的字符总数【need=0表示匹配到了】

        for right in range(n):

            # 窗口右边界
            ch = s2[right]  # 窗口中新加入的字符
            if ch in cnt:  # 新加入的字符ch位于s1中
                if cnt[ch] > 0:  # 此时新加入窗口中的字符ch对need有影响
                    need -= 1
                cnt[ch] -= 1

            # 窗口左边界
            left = right - m
            if left >= 0:
                ch = s2[left]
                if ch in cnt:  # 刚滑出的字符位于s1中
                    if cnt[ch] >= 0:  # 此时滑出窗口的字符ch对need有影响
                        need += 1
                    cnt[ch] += 1

            if need == 0:  # 找到了一个满足题意的窗口
                return True

        return False

