'''
给定一个字符串 s ，请你找出其中不含有重复字符的 最长子串 的长度。示例 1:

输入: s = "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。

示例 2:
输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。

示例 3:
输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。

"abcabcbb"
方法：
滑动窗口加双指针
arr[j]代表索引为j的字符最后一次出现的索引，[i,j]代表最大字符
 a b c a b c a b
 i
 j
 初始化i,j=0,遍历j，用一个has表存储此时滑动窗口的值
 has={}
 has={a}
 a b c a b c a b
 i
   j
 has={a,b}
 a b c a b c a b
 i
    j
has={a:0,b:1,c:2}
 a b c a b c a b
 i
       j
has={a:0,b:1,c:2}
j在其中，存入[abc],更新j
has={a:3,b:1,c:2}
以 (a)bcabcbb 开始的最长字符串为 (abc)abcbb
以 a(b)cabcbb 开始的最长字符串为 a(bca)bcbb
以 ab(c)abcbb 开始的最长字符串为 ab(cab)cbb
以 abc(a)bcbb 开始的最长字符串为 abc(abc)bb
以 abca(b)cbb 开始的最长字符串为 abca(bc)bb
我们可以发现在遍历时如果abc是已经找到的最长不重复子串，那么其子字符串也是，比如abc是， bc和c也是，我们不需要每次都从开始的下一个字符来查找
所以以一个hash表计算无重复的字符，利用遍历的方式，i和j代表整个字符串的开始和结束

  a b c a b c b b
  i
      j
  i,j放在开头。hash表为空
  使用j遍历
  {a,b,c}
  a b c a b c b b
    i
        j
  当j再到a的时候此时我们找到了当前的第一个重复字串，记录abc,由于abc是无重复字串，所以bc也是，加入a还是
  a b c a b c b b
    i
          j
  {a,b,c}
  j继续向前，此时同样，j再hash中，我们需要收缩左边界。直到j所指向的元素再hash表中完全移除，并移动i指针

  参考：https://blog.algomooc.com/LeetCode/%E7%AC%AC%E5%9B%9B%E5%91%A8/%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%83%E5%A4%A9/LeetCode%203%E3%80%81%E6%97%A0%E9%87%8D%E5%A4%8D%E5%AD%97%E7%AC%A6%E7%9A%84%E6%9C%80%E9%95%BF%E5%AD%90%E4%B8%B2.html#%E4%B8%89%E3%80%81%E5%8F%82%E8%80%83%E4%BB%A3%E7%A0%81
'''

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if not s:
            return 0
        if len(s)==1:
            return 1
        i=0
        n=len(s)
        setS=set()
        max_len=0
        arr=[] #记录所有 非重复字符的长度
        for j in range(n):
            end_s=s[j]
            while end_s in setS:
                arr.append(s[i:j])
                setS.remove(s[i])
                i+=1
            # 全部移除以后，将end_s加入
            setS.add(end_s)
            max_len=max(max_len,j-i+1)
        arr.append(s[i:j+1])
        print(arr)
        return max_len


if __name__=="__main__":
    solution=Solution()
    if True:
        s="abcabcbb"
        res=solution.lengthOfLongestSubstring(s)
        print(res)
        s="bbbbb"
        res=solution.lengthOfLongestSubstring(s)
        print(res)
        s="pwwkew"
        res=solution.lengthOfLongestSubstring(s)
        print(res)
    if True:
        s = "aab"
        res = solution.lengthOfLongestSubstring(s)
        print(res)