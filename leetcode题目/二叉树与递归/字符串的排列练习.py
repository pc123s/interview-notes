'''

输入一个长度为 n 字符串，打印出该字符串中字符的所有排列，你可以以任意顺序返回这个字符串数组。
例如输入字符串ABC,则输出由字符A,B,C所能排列出来的所有字符串ABC,ACB,BAC,BCA,CBA和CAB。 但里面 不能有重复元素。
数据范围：
n<10
要求：空间复杂度
O(n!)，时间复杂度O(n!)

输入：
"ab"
返回值：
["ab","ba"]
返回["ba","ab"]也是正确的

输入：
"aab"
返回值：
["aab","aba","baa"]

输入：
"abc"
返回值：
["abc","acb","bac","bca","cab","cba"]

思路1：用一个list去记录已经拼接的字符（记录重复字符），用递归的方式去拼接字符串，当达到制定的长度时停止递归
比如 abc ->set abc
弹出三次
a b c
a b c
a b c
分别组成树，但是在连接为树的时候，要注意，已经弹出的字符不能再进行二次拼接，所以我们需要一个list[0,1] 哪些被占用了
a b c [0,0,0]
i
第一轮递归
i=0 ""+a="a"  [1,0,0]
第二轮递归 i=0的基础上
i=0 1被占用
i=1 ab [1,1,0]
i=2 ac [1,0,1]
第三轮递归
i=0 i=1(被占用) i=2 abc
i=0 i=2（被占用） i=1 acb

aab
   a     a    b
  a b   a b  a a
 b   a  b a  a  a
if i!=0 and text[i]==text[i-1] and record_lis[i-1]
看看这一行代码什么意思

a
[1, 0, 0]
aa
[1, 1, 0]
aab #这个不行
[1, 1, 1]
ab
[1, 0, 1]
aba #这个也不行
[1, 1, 1]
a
[0, 1, 0]
aa
[1, 1, 0]
aab
[1, 1, 1]
ab
[0, 1, 1]
aba
[1, 1, 1]
b
[0, 0, 1]
ba
[1, 0, 1]
baa # 这个也不行
[1, 1, 1]
ba
[0, 1, 1]
baa
[1, 1, 1]

即我在递归途中发现跟前面的字符重复了，为了保证非重复性，怎么做呢，先对字符串进行排序，这样就能保证重复的字符串
都在一起，且只被排列一次
'''



rest = "abc"

from typing import *
class Solution:
    def permutation(self,s):
        res=[]
        def dfs(path,rest):
            # 剩余拼接的字符串
            if len(rest)==0:
                res.append(path)
                return
            used = set()
            for i in range(len(rest)):
                if rest[i] in used:
                    continue
                used.add(rest[i])
                # rest[:i]+rest[i+1:] 这代表删除rest中的第i个字符。
                dfs(path+rest[i],rest[:i]+rest[i+1:])

        dfs("", s)
        return res




for i in range(len(rest)):
    print("选中:", rest[i], "剩下:", rest[:i] + rest[i+1:])

if __name__=="__main__":
    solution=Solution()
    if True:
        res=solution.permutation("abc")
        print(res)