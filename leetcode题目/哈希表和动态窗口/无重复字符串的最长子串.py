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
arr[j]代表以j结尾的字符串，[i,j]代表最大的无重复子串
 a b c a b c a b
 i
 j
 初始化i,j=0,遍历j，用一个set表存储此时滑动窗口的值
 set={}
 set={a}
 a b c a b c a b
 i
   j
 set={a,b}
 a b c a b c a b
 i
    j
set={a,b,c}
 a b c a b c a b
 i
       j
arr[j]在set中，代表此时以a为开始索引的字符串重复了，我们需要移除并扩大i,j的位置
首先arr存入当前找到的abc arr[i:j]=abc
2、确保set中的值没有重复，不断 比对set中的第一个值，直到将arr[j]的值去除
例如
arr[j]=a
set 移除a，set={b,c} i+=1，此时a不在{b,c}中了，移除结束

假如 arr[j]=c呢
那么我们需要移除2次
set 移除a set={b,c} i+=1,
set 移除b set={c} i+=1,
set 移除c set={} i+=1,
移除结束


以 (a)bcabcbb 开始的最长字符串为 (abc)abcbb
以 a(b)cabcbb 开始的最长字符串为 a(bca)bcbb
以 ab(c)abcbb 开始的最长字符串为 ab(cab)cbb
以 abc(a)bcbb 开始的最长字符串为 abc(abc)bb
以 abca(b)cbb 开始的最长字符串为 abca(bc)bb
我们可以发现在遍历时如果abc是已经找到的最长不重复子串，那么其子字符串也是，比如abc是， bc和c也是，我们不需要每次都从开始的下一个字符来查找
所以以一个hash表记录索引，直接从当前位开始就可以了

  a b c a b c b b
  i
      j
  s_len=j-i+1=3
  i,j放在开头。hash表为={a:0,b:1,c:2}
  a b c a b c b b
    i
        j
  s[j] in hash
  此时更新索引 i=has[a]+1=1
  更新hash
  hash={a:1,b:1,c:2}
  s_len=j-i+1=3-1+1=3
   a b c a b c b b
       i
           j
  此时更新索引 i=has[b]+1=2
  更新hash={a:1,b:4,c:2}
  s_len=j-i+1=4-2+1=3

  不断循环，将最大s_len记做目标值。

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

    def lengthOfLongestSubstring1(self, s: str) -> int:
        if not s:
            return 0
        if len(s)==1:
            return 1
        i=0
        n=len(s)
        d={}
        max_len=0
        arr=[] #记录所有 非重复字符的长度
        for j in range(n):
            end_s=s[j]
            if end_s in d:
                #arr.append(s[i:j])
                # 更新i
                #print(i)
                i_=d[end_s]
                # 当发现在重复字典中，且从重复索引找时，我们需要将索引向后移动
                # 如 abca has={a:0,b=1,c=2} a时，将 需要移动a+=1即b的下标
                # 如果发现i为非现有has的索引
                # 如tmmzuxt j=7，tmmzuxt {'t': 0, 'm': 2, 'z': 3, 'u': 4, 'x': 5} 此时t为0，i=2
                # 我们不需要i后移动
                if i_>=i:
                    i=i_+1
                else:
                    i=i
                #i=max(i_,i)+1
                #d[end_s]=i

            # 全部移除以后，将end_s加入
            d[end_s]=j
            s_len=j-i+1
            print(d)
            if s_len>max_len:
                arr.append(s[i:j+1])
                max_len=s_len

        print(arr)
        return max_len


if __name__=="__main__":
    solution=Solution()
    if True:
        s="abcabcbb"
        res=solution.lengthOfLongestSubstring1(s)
        print(res)
        s="bbbbb"
        res=solution.lengthOfLongestSubstring1(s)
        print(res)
        s="pwwkew"
        res=solution.lengthOfLongestSubstring1(s)
        print(res)
    if True:
        s = "tmmzuxt"
        res = solution.lengthOfLongestSubstring1(s)
        print(res)