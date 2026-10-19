'''
给你一个满足下述两条属性的 m x n 整数矩阵：
每行中的整数从左到右按非严格递增顺序排列。
每行的第一个整数大于前一行的最后一个整数。
给你一个整数 target ，如果 target 在矩阵中，返回 true ；否则，返回 false 。
输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
输出：true

输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
输出：false

方法1：利用循环遍历的方式查找，这个方法是可以的，但是比较慢

方法2：从列开始找，先找开头的第一个数字，然后在行数字中利用二分查找寻找目标数字

注意n的位置
'''
from typing import *
class Solution:
    def half_find(self,nums,target):
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] == target:
                return True
            elif nums[mid] > target:
                r = mid - 1
            elif nums[mid] < target:
                l = mid + 1
        return False
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m=len(matrix)
        n=len(matrix[0])
        if m==1:
            if n==1:
                return matrix[0][0]==target
            else:
                nums=matrix[0]
                return self.half_find(nums,target)
        index=-1 #确定数字在第几行,初始化-1
        for i in range(m):
            if matrix[i][0]<=target and matrix[i][n-1]>=target:
                index=i
        print(index)
        if index==-1:
            return False
        nums=matrix[index]
        return self.half_find(nums,target)

if __name__=="__main__":
    solution=Solution()
    if False:
        matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
        target = 2
        isBool=solution.searchMatrix(matrix,target)
        print(isBool)
    if False:
        matrix = [[1]]
        target = 1
        isBool=solution.searchMatrix(matrix,target)
        print(isBool)
    if False:
        matrix = [[1],[3]]
        target = 3
        isBool=solution.searchMatrix(matrix,target)
        print(isBool)
    if True:
        matrix = [[1,3]]
        target = 3
        isBool=solution.searchMatrix(matrix,target)
        print(isBool)
