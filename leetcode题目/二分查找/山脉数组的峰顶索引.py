'''
存在 i（0 < i < arr.length - 1）使得：
arr[0] < arr[1] < ... arr[i-1] < arr[i]
arr[i] > arr[i+1] > ... > arr[arr.length - 1]
给你由整数组成的山脉数组 arr ，返回满足 arr[0] < arr[1] < ... arr[i - 1] < arr[i] > arr[i + 1] > ... > arr[arr.length - 1] 的下标 i 。

你必须设计并实现时间复杂度为 O(log(n)) 的解决方案。


示例 1：

输入：arr = [0,1,0]
输出：1
示例 2：

输入：arr = [0,2,1,0]
输出：1
示例 3：

输入：arr = [0,10,5,2]
输出：1

提示：
3 <= arr.length <= 105
0 <= arr[i] <= 106
题目数据保证 arr 是一个山脉数组

要求log(n)的时间复杂度

方法为二分查找，和寻找峰值的那道题的结果是一样的。
'''
from typing import *
class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        if len(arr)==3:
            return 1
        l,r=0,len(arr)-1
        while l<=r:
            mid=l+(r-l)//2
            if arr[mid]>arr[mid+1] and arr[mid]>arr[mid-1]:
                return mid
            if mid==0 and arr[mid]>arr[mid+1]:
                return mid
            if mid==len(arr)-1 and arr[mid]>arr[mid-1]:
                return mid
            elif arr[mid]>arr[mid+1]:
                r=mid-1
            elif arr[mid]<arr[mid+1]:
                l=mid+1



