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
from typing import *
class Solution:
    def dfs(self,res_lis:List[str],record_lis:List[int],temp_str:str,n:int,text:str):
        if len(temp_str)==n:
            res_lis.append(temp_str)
        for i in range(n):
            #print(i)
            #print(record_lis)
            if record_lis[i]==1:
                continue
            # # 如果当前值跟前一个相同，并且前一个已经在递归了
            if i!=0 and text[i]==text[i-1] and record_lis[i-1]:
                continue
            temp_str+=text[i]
            print(temp_str)
            record_lis[i]=1
            print(record_lis)

            self.dfs(res_lis,record_lis,temp_str,n,text)
            # 回溯
            # str回溯一位
            temp_str=temp_str[:-1]
            record_lis[i]=0



    def Permutation(self , str: str) -> List[str]:
        # write code here
        l=list(str)
        l.sort()
        str="".join(l)
        n=len(str)
        record=[0]*(n)
        res_l=[]
        self.dfs(res_l,record,"",n,str)
        return res_l


if __name__=="__main__":
    solution=Solution()
    if False:
        res=solution.Permutation("abc")
        print(res)
    if True:
        res=solution.Permutation("aab")
        print(res)
    if False:
        res=solution.Permutation("aabaa")
        print(res)