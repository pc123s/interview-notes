''' 给你一个字符串 croakOfFrogs，它表示不同青蛙发出的蛙鸣声（字符串 "croak" ）的组合。由于同一时间可以有多只青蛙呱呱作响，所以 croakOfFrogs 中会混合多个 “croak” 。
请你返回模拟字符串中所有蛙鸣所需不同青蛙的最少数目。
要想发出蛙鸣 "croak"，青蛙必须 依序 输出 ‘c’, ’r’, ’o’, ’a’, ’k’ 这 5 个字母。如果没有输出全部五个字母，那么它就不会发出声音。如果字符串 croakOfFrogs 不是由若干有效的 "croak" 字符混合而成，请返回 -1 。
输入：croakOfFrogs = "croakcroak" 输出：1 解释：一只青蛙 “呱呱” 两次
输入：croakOfFrogs = "crcoakroak" 输出：2 解释：最少需要两只青蛙，“呱呱” 声用黑体标注 第一只青蛙 "crcoakroak" 第二只青蛙 "crcoakroak"
输入：croakOfFrogs = "croakcrook" 输出：-1 解释：给出的字符串不是 "croak" 的有效组合。 字符串长度1-10000
思路，这个其实是一个顺序的声音序列。
使用字典记录每个字母的值，如果是顺序的，则前面字典的字母数量一定大于后面
'''
from typing import *
class Solution:
    def minNumberOfFrogs(self, croakOfFrogs: str) -> int:
        dic_={}
        for _ in croakOfFrogs:
            dic_[_]=dic_.get(_,0)+1
        #dic_["c"]!=dic_["r"]!=dic_["o"]!=dic_["a"]!=dic_["k"] 这种写法是错误的
        # 这一写法代表 croak四个字母在字典的值都不相等 为True，否则为False
        # a,b,c=1,1,2  a!=b!=c False  a,b,c=1,2,3 a!=b!=c True
        if not dic_["c"]==dic_["r"]==dic_["o"]==dic_["a"]==dic_["k"]:
            return -1
        dic_['c']=dic_['r']=dic_['o']=dic_['a']=dic_['k']=0
        # 记录场上最多的方块数
        res=0
        for char in croakOfFrogs:
            dic_[char]+=1
            if (dic_["c"] >= dic_["r"] >= dic_["o"] >= dic_["a"]>= dic_["k"]):
                if dic_["c"] >= dic_["r"] >= dic_["o"] >= dic_["a"]>= dic_["k"]>=1:
                    #在消除时看场上最大的方块数
                    res=max(dic_['c'],res)
                    for _ in "croak":
                        dic_[_]-=1
            else:
                return -1
        return res
solution=Solution()
print(solution.minNumberOfFrogs('croakcroak'))
print(solution.minNumberOfFrogs('crcoakroak'))
print(solution.minNumberOfFrogs('croakcrook'))
print(solution.minNumberOfFrogs('okcracakroroakacckor'))