'''
最长公共子序列

给定两个字符串 text1 和 text2，返回这两个字符串的最长 公共子序列 的长度。如果不存在 公共子序列 ，返回 0 。

一个字符串的 子序列 是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串。

例如，"ace" 是 "abcde" 的子序列，但 "aec" 不是 "abcde" 的子序列。
两个字符串的 公共子序列 是这两个字符串所共同拥有的子序列。

示例 1：

输入：text1 = "abcde", text2 = "ace"
输出：3
解释：最长公共子序列是 "ace" ，它的长度为 3 。
示例 2：

输入：text1 = "abc", text2 = "abc"
输出：3
解释：最长公共子序列是 "abc" ，它的长度为 3 。
示例 3：

输入：text1 = "abc", text2 = "def"
输出：0
解释：两个字符串没有公共子序列，返回 0 。

方法：动态规划
提到删除，我想到的就是编辑距离。编辑距离是删除 替换 和添加这个只是删除。我们先来做个表格

      "" a ab adc abcd abcde
""    0  0  0  0   0    0
a     0  1  1  1   1    1
ac    0  1  1  2   2    2
ace   0  1  1  2   2    3
text1[i]==text[j]
dp[i][j]=dp[i-1][j-1]+1 因为最后一个字符相等，等于text1[:i-1]和text2[:j-1]前一个的最长序列+1即可
text1[i]!=text[j]
dp[i][j]=max(dp[i-1][j],dp[i-1][j])

abbsada
absaa
       "" a ab abb abbs abbsa abbsad abbsada
""     0  0  0  0   0    0     0       0
a      0  1  1  1   1    1     1       1
ab     0  1  2  2   2    2     2       2
abs    0  1  2  2   3    3     3       3
absa   0  1  2  2   3    4     4       4
absaa  0  1  2  2   3    4     4       5


text1 = "jmjkbkjkv"
text2 = "bsbininm"
    "" b s b i n i n m
""  0  0 0 0 0 0 0 0 0
j   0  0 0 0 0 0 0 0 0
m   0  0 0 0 0 0 0 0 1
j   0  0 0 0 0 0 0 0 1
k   0  0 0 0 0 0 0 0 1
b   0  1 1 1 1 1 1 1 1
k   0  1 1 1 1 1 1 1 1
j   0  1 1 1 1 1 1 1 1
k   0  1 1 1 1 1 1 1 1
v   0  1 1 1 1 1 1 1 1

'''
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m=len(text1)
        n=len(text2)
        dp=[[0]*(n+1) for _ in range(m+1)]

        res=""
        LastLen=0
        for i in range(1,m+1):
            for j in range(1,n+1):
                if text1[i-1]==text2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                    if dp[i][j]>LastLen:
                        res+=text1[i-1]
                        LastLen=dp[i][j]
                else:
                    dp[i][j]=max(dp[i-1][j],dp[i][j-1])
        print(dp)
        print(res)
        return dp[m][n]



if __name__=="__main__":
    solution=Solution()
    if True:
        text1 = "abbsada"
        text2 = "absaa"
        res=solution.longestCommonSubsequence(text1,text2)
        print(res)
    if True:
        text1 = "abcde"
        text2 = "ace"
        res=solution.longestCommonSubsequence(text1,text2)
        print(res)
    if True:

        text1 = "jmjkbkjkv"
        text2 = "bsbininm"
        res = solution.longestCommonSubsequence(text1, text2)
        print(res)

