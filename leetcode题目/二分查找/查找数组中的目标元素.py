'''
给定一个 n 个元素有序的（升序）整型数组 nums 和一个目标值 target  ，写一个函数搜索 nums 中的 target，如果目标值存在返回下标，否则返回 -1。


示例 1:

输入: nums = [-1,0,3,5,9,12], target = 9
输出: 4
解释: 9 出现在 nums 中并且下标为 4
示例 2:

输入: nums = [-1,0,3,5,9,12], target = 2
输出: -1
解释: 2 不存在 nums 中因此返回 -1

自己的答案：
以log(n)的方式查找目标值
采用双指针查找（left,right），每次计算一个中间指针 mid,注意，当mid和left或者right重合时，此时存在一个死循环，所以最好让mid移动一下

标准答案：
left重置为mid+1
right重置为right-1

'''
from typing import *
from math import ceil
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        if not nums: #nums为空
            return -1
        left,right=0,len(nums)-1 #设置两个指针分别指向两端
        while left!=right :
            mid=(left+right)//2
            if mid==left or mid==right:
                record_num=-1 #记录index
                for i in range(left,right+1):
                    if nums[i]==target:
                        record_num=i
                return record_num

            #mid=ceil((left+right)/2)
            print(left,right,mid)
            if nums[mid]>target:
                right=mid
            elif nums[mid]==target:
                return mid
            else: #nums[mid]<target
                left=mid

        if nums[left]==target:
            return left
        else:
            return -1
    # 标准答案
    def search(self, nums: List[int], target: int) -> int:

        # 二分查找法的一种写法，在左闭右闭的区间里去查找目标值

        # left 为当前区间最左侧的元素，可以获取到
        left = 0

        # right 为当前区间最右侧的元素，可以获取到
        right = len(nums) - 1

        # 在 while 循环里面，left 不断的 ++，而 right 不断的 --
        # 当 [ left , right ] 这个区间不存在元素的时候，才跳出 while 循环，也就是当 left > right 时跳出循环
        # 即当 left = right + 1 时，搜索区间没有元素了
        # 由于 left 和 right 相遇的时候指向同一个元素，这个元素是存在于 [ left , right] 区间，这个区间就一个元素
        # 所以此时 while 循环的判断可以使用等号
        while left <= right:

            # left + (right - left) / 2 和 (left + right) / 2 的结果相同
            # 但是使用 left + (right - left) / 2 可以防止由于 left 、right 同时太大，导致相加的结果溢出的问题
            # 比如数据 int 的最大值为 2,147,483,647
            # 此时，left 为 2,147,483,640
            # 此时，right 为 2,147,483,646
            # 两者直接相加超过了 2,147,483,647，产生了溢出
            mid = left + (right - left) // 2

            # 中间的元素和目标值 target 相等，直接返回下标即可
            if nums[mid] == target:
                # 直接返回下标即可
                return mid

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

        # 查找完区间中的所有元素都没有找到，返回 -1
        return -1


if __name__=="__main__":
    nums =[-1, 0, 3, 5, 9, 12]
    target =2
    solution=Solution()
    res=solution.search(nums,2)
    print(res)
