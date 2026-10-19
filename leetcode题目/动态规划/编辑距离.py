'''
给你两个单词 word1 和 word2， 请返回将 word1 转换成 word2 所使用的最少操作数  。

你可以对一个单词进行如下三种操作：

插入一个字符
删除一个字符
替换一个字符

示例 1：

输入：word1 = "horse", word2 = "ros"
输出：3
解释：
horse -> rorse (将 'h' 替换为 'r')
rorse -> rose (删除 'r')
rose -> ros (删除 'e')
示例 2：

输入：word1 = "intention", word2 = "execution"
输出：5
解释：
intention -> inention (删除 't')
inention -> enention (将 'i' 替换为 'e')
enention -> exention (将 'n' 替换为 'x')
exention -> exection (将 'n' 替换为 'c')
exection -> execution (插入 'u')



         ""  h  ho  hor  hors horse
""       0   1  2   3     4     5
r        1   1
ro       2
ror      3
rors     4
rorse    5

dp[i-1][j] 表示删除操作 dp[i][j-1]表示插入操作，dp[i-1][j-1]表示替换操作
设word1为长字符
word1= horse
           i
word2= rorse
           j
如果是替换，那么比较i-1和j-1的结果就行，因为i和j指向的字符肯定是相同（被替换了）
删除word1,i-1那么比较 i-1和j的值

插入
插入相当于将word2的字符插入到word1后面
word1 appleo
          i
word2 hello
          j
此时为了抵消字符的影响，将i和j的指向同时消除，
word1 apple
          i
word2 hell
         j
比较 i 和 j-1
所以这个bp很简单， min(dp[i-1][j-1],dp[i-1][j],dp[i][j-1])+1  word1[i]!word[j]
                想等则 dp[i][j]=dp[i-1][i-j]

'''
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m=len(word1)+1
        n=len(word2)+1
        dp=[[0]*n for i in range(m)]
        for i in range(m):
            dp[i][0]=i
        for j in range(n):
            dp[0][j]=j
        for i in range(1,m):
            for j in range(1,n):
                if word1[i-1]==word2[j-1]:
                    dp[i][j]=dp[i-1][j-1]
                else:
                    dp[i][j]=min(dp[i-1][j-1],dp[i][j-1],dp[i-1][j])+1
        print(dp)
        return dp[m-1][n-1]


if __name__=='__main__':
    solution=Solution()
    res=solution.minDistance("horse","ros")
    print(res)