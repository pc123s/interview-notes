'''
给定一个长度为 n 的整数数组 height 。有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i]) 。

找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

返回容器可以储存的最大水量。

说明：你不能倾斜容器。


输入：[1,8,6,2,5,4,8,3,7]
输出：49
解释：图中垂直线代表输入数组 [1,8,6,2,5,4,8,3,7]。在此情况下，容器能够容纳水（表示为蓝色部分）的最大值为 49。
示例 2：

输入：height = [1,1]
输出：1

方法1  暴力法 两个指针循环遍历，计算每次的长度*高度，找出最大值

方法2： 贪心算法
[1,8,6,2,5,4,8,3,7]
用这个list举例
res=w*h
left right分别指向列表的两端，这时长度是一定的，n=9
那么 此时的面积为 1=min(1,7)，我们向内移动指针 w减小，如果移动长的柱子，那么面积一定会减小
如果移动短的柱子，面积还有可能变大。所以这里需要移动较短的柱子并记录 面积的最大值



参考：https://www.algomooc.com/587.html
'''
from typing import *
class Solution:
    def maxArea(self, height: List[int]) -> int:
        if not height:
            return 0
        if len(height)==1:
            return height[0]
        n=len(height)
        # 两个指针循环
        max_num=-9999999999999  #记录最大面积的值
        for i in range(n-1):
            for j in range(i+1,n):
                a,b=height[i],height[j]
                res=min(a,b)*(j-i)
                if res>max_num:
                    max_num=res
        return max_num
    def maxArea1(self, height: List[int]) -> int:
        if not height:
            return 0
        if len(height) == 1:
            return height[0]
        n=len(height)
        left,right=0,n-1
        # 左指针和右指针不相遇
        max_num=-999999999 #记录最大值
        while left!=right:
            a,b=height[left],height[right]
            w=right-left
            res=min(a,b)*w
            if res>max_num:
                max_num=res
            if height[left]>height[right]:
                right-=1
            else:
                left+=1
        return max_num
if __name__=='__main__':
    height=[1, 8, 6, 2, 5, 4, 8, 3, 7]
    solution=Solution()
    res=solution.maxArea1(height)
    print(res)
    height = [1,1]
    res=solution.maxArea1(height)
    print(res)
