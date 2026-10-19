'''
给你一个按照非递减顺序排列的整数数组 nums，和一个目标值 target。请你找出给定目标值在数组中的开始位置和结束位置。
如果数组中不存在目标值 target，返回 [-1, -1]。
你必须设计并实现时间复杂度为 O(log n) 的算法解决此问题。

示例 1：

输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]
示例 2：

输入：nums = [5,7,7,8,8,10], target = 6
输出：[-1,-1]
示例 3：

输入：nums = [], target = 0
输出：[-1,-1]

log(n)的复杂度
做法一样，还是采用二分查找，只不过找到以后向前和向后搜索一下

'''

from typing import *


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
            if not nums:
                return [-1,-1]
            # if len(nums)==1:
            #     if nums[0]==target:
            #         return [0,0]
            #     else:
            #         return [-1,-1]

            # 二分查找法的一种写法，在左闭右闭的区间里去查找目标值

            # left 为当前区间最左侧的元素，可以获取到
            left = 0

            # right 为当前区间最右侧的元素，可以获取到
            right = len(nums) - 1
            n=len(nums)

            # 在 while 循环里面，left 不断的 ++，而 right 不断的 --
            # 当 [ left , right ] 这个区间不存在元素的时候，才跳出 while 循环，也就是当 left > right 时跳出循环
            # 即当 left = right + 1 时，搜索区间没有元素了
            # 由于 left 和 right 相遇的时候指向同一个元素，这个元素是存在于 [ left , right] 区间，这个区间就一个元素
            # 所以此时 while 循环的判断可以使用等号
            while left <= right: #=号对当前判断一次

                # left + (right - left) / 2 和 (left + right) / 2 的结果相同
                # 但是使用 left + (right - left) / 2 可以防止由于 left 、right 同时太大，导致相加的结果溢出的问题
                # 比如数据 int 的最大值为 2,147,483,647
                # 此时，left 为 2,147,483,640
                # 此时，right 为 2,147,483,646
                # 两者直接相加超过了 2,147,483,647，产生了溢出
                mid = left + (right - left) // 2

                # 中间的元素和目标值 target 相等，直接返回下标即可
                if nums[mid] == target:
                    left,right=mid,mid #向左或者向右搜索
                    #先搜索左边
                    while left>=0 and nums[left]==target :
                        left-=1
                    while  right<n and nums[right]==target:
                        right+=1
                    return [left+1,right-1]


                # 中间的元素大于了目标值 target
                # 1、数组为有序数组，比如为递增数组
                # 2、数组中不存在重复元素
                # 由于该数组存在以上两个特点，所以 [ mid , right ] 这个区间中的所有元素都大于目标值 target
                # 因此，缩小查找区间为 [ left , mid - 1]
                elif nums[mid] > target:
                    # 也就是说缩小之后的区间最右侧位置为 mid - 1
                    right = mid - 1

                # 中间的元素小于了目标值 target
                # 1、数组为有序数组，比如为递增数组
                # 2、数组中不存在重复元素
                # 由于该数组存在以上两个特点，所以 [ left , mid ] 这个区间中的所有元素都小于目标值 target
                # 因此，缩小查找区间为 [ mid + 1 , right]
                elif nums[mid] < target:
                    # 也就是说缩小之后的区间最左侧位置为 mid + 1
                    left = mid + 1

            # if nums[left]==target:
            #     return [left,left]
            # else:
            # 查找完区间中的所有元素都没有找到，返回 -1
            return [-1,-1]


s=Solution()
l=s.searchRange([1,2,3,3,4,5],3)
print(l)
l=s.searchRange([1],1)
print(l)

# l=s.searchRange([5,7,7,8,8,10],8)
# print(l)
# l=s.searchRange([1,2,3,3,4,5],6)
# print(l)
# l=s.searchRange([],6)
# print(l)