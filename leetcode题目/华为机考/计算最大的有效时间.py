'''
给定一个由 6 位数字组成的数组，返回可以设置的符合 24 小时制的最大时间。

24 小时格式为 "HH:MM" ，其中 HH 在 00 到 23 之间，MM 在 00 到 59 之间。最小的 24 小时制时间是 00:00 ，而最大的是 23:59 。从 00:00 （午夜）开始算起，过得越久，时间越大。

以长度为 5 的字符串，按 "HH:MM" 格式返回答案。如果不能确定有效时间，则返回空字符串。



示例 1：

输入：arr = [1,2,3,4,5,6]
输出："23:56:41"
解释：有效的 24 小时制时间是 "12:34"，"12:43"，"13:24"，"13:42"，"14:23"，"14:32"，"21:34"，"21:43"，"23:14" 和 "23:41" 。这些时间中，"23:41" 是最大时间。
示例 2：

输入：arr = [5,5,5,5,5,5]
输出：""
解释：不存在有效的 24 小时制时间，因为 "55:55" 无效。

示例 3：

输入：arr = [0,0,0,0,0,0]
输出："00:00:00"

思路：分别计算6个位数的数字可能

1 找出<=2的最大数 数组remove掉
2 if 1位为0,1，则找出不小于9的数 否则找出<=3的数
3 找出<=5的最大数
4 找出<=9的最大数
5 找出<=5的最大数
6 找出<=5的最大数

'''
from typing import *
class Solution:
    def largetTimeDigit(self,arr:List):
        a,b,c,d,e,f=0,0,0,0,0,0
        res1=self.findMaxN(arr,2)
        if res1==-1:
            return ""
        a=res1
        arr.remove(a)
        if a<2:
            res2=self.findMaxN(arr,9)
            if res2==-1:
                return ""
            b=res2
            arr.remove(b)
        else:
            res2=self.findMaxN(arr,3)
            if res2==-1:
                return ""
            b=res2
            arr.remove(b)

        res3 = self.findMaxN(arr, 5)
        if res3==-1:
            return ""
        else:
            c=res3
            arr.remove(c)

        res4 = self.findMaxN(arr, 9)
        if res4 == -1:
            return ""
        else:
            d = res4
            arr.remove(d)

        res5 = self.findMaxN(arr, 5)
        if res5 == -1:
            return ""
        else:
            e = res5
            arr.remove(e)

        res6 = self.findMaxN(arr, 9)
        if res6 == -1:
            return ""
        else:
            f = res6
            arr.remove(f)

        return f"{a}{b}:{c}{d}:{e}{f}"

    def findMaxN(self,arr,n):
        max_num=-9999
        for i in arr:
            if i<=n and i>max_num:
                max_num=i
        if max_num==-9999:
            return -1
        else:
            return max_num



if __name__=="__main__":
    solution=Solution()
    if True:
        arr=[5,4,2,2,3,4]
        #res=solution.findMaxN(arr,1)
        #print(res)
        res=solution.largetTimeDigit(arr)
        print(res)
    if True:
        arr = [9, 9, 9, 9, 9, 9]
        # res=solution.findMaxN(arr,1)
        # print(res)
        res = solution.largetTimeDigit(arr)
        print(res)
