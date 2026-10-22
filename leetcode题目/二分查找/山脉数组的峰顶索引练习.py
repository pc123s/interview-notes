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
        n=len(arr)
        l,r=0,n-1
        while l<r:
            mid=l+(r-l)//2
            if arr[mid]>=arr[mid-1] and arr[mid]>=arr[mid+1]:
                return mid
            if arr[mid]<arr[l]:
                r=mid+1
            else:
                l=mid+1
        return l

if __name__=="__main__":
    solution=Solution()
    print(solution.peakIndexInMountainArray([0,1,0]))
    print(solution.peakIndexInMountainArray([0,2, 1, 0]))
    print(solution.peakIndexInMountainArray([0,10,5, 0]))
    print(solution.peakIndexInMountainArray([0,1,2,3,4]))
    print(solution.peakIndexInMountainArray([4,3,2,1,0]))


