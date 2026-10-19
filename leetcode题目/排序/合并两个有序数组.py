'''
给你两个按 非递减顺序 排列的整数数组 nums1 和 nums2，另有两个整数 m 和 n ，分别表示 nums1 和 nums2 中的元素数目。
请你 合并 nums2 到 nums1 中，使合并后的数组同样按 非递减顺序 排列。
注意：最终，合并后数组不应由函数返回，而是存储在数组 nums1 中。为了应对这种情况，nums1 的初始长度为 m + n，其中前 m 个元素表示应合并的元素，后 n 个元素为 0 ，应忽略。nums2 的长度为 n 。
示例 1：
输入：nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
输出：[1,2,2,3,5,6]
解释：需要合并 [1,2,3] 和 [2,5,6] 。
合并结果是 [1,2,2,3,5,6] ，其中斜体加粗标注的为 nums1 中的元素。
示例 2：
输入：nums1 = [1], m = 1, nums2 = [], n = 0
输出：[1]
解释：需要合并 [1] 和 [] 。
合并结果是 [1] 。
示例 3：

输入：nums1 = [0], m = 0, nums2 = [1], n = 1
输出：[1]
解释：需要合并的数组是 [] 和 [1] 。
合并结果是 [1] 。
注意，因为 m = 0 ，所以 nums1 中没有元素。nums1 中仅存的 0 仅仅是为了确保合并结果可以顺利存放到 nums1 中。

方法：
设置两个索引 i 和 j 分别指向 nums1 和 nums2 的有效元素的尾部，从它们的尾部开始向前遍历，同时设置索引 cur 指向 nums1 的最末尾，在每次遍历过程中，
比较 i 和 j 指向的元素值大小，把大的元素填充到 cur 的位置，填充完毕说明那个元素已经放置在它应该放置的位置，不需要在管它了，把 cur 向前移动，同时把 i 或者 j 向前移动，
继续比较 i 和 j 指向的元素值大小，把大的元素填充到 cur 的位置。

先从空缺处开始填充
[1 ,2 ,3 ,0 0 0]  [2 ,5 ,6]
       i                 j
[1 ,2 ,3 ,0  0  6 ]  [2 ,5 ,6]
       i    cur         j

[1 ,2 ,3 ,0  5  6 ]  [2 ,5 ,6]
       i  cur         j


'''
from typing import *
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        if not nums1:
            return nums2
        if not nums2:
            return nums1
        if m==0:
            for i in range(n):
                nums1[i]=nums2[i]
            return nums1
        if n==0:
            return nums1
        i=m-1
        j=n-1
        cur=m+n-1
        # i和j
        while j>-1 and i>-1:
            if nums1[i]<=nums2[j]:
                nums1[cur]=nums2[j]
                cur-=1
                j-=1
            else:
                nums1[cur]=nums1[i]
                i-=1
                cur-=1
            #print(nums1)
        if j>=0: #将j的数据插入进行
            for i in range(0,j+1):
                nums1[i]=nums2[i]
        return nums1


if __name__=="__main__":
    solution=Solution()
    # nums1=[1,2,3,5,6,0]
    # nums2=[3]
    # nums=solution.merge(nums1,5,nums2,1)
    # print(nums)
    #
    # nums1=[1,3,3,3,6,7,0,0,0]
    # nums2=[3,3,3]
    # nums=solution.merge(nums1,6,nums2,3)
    # print(nums)

    nums1 = [4, 5, 6, 0, 0, 0]
    nums2 = [1,2,3]
    nums = solution.merge(nums1, 3, nums2, 3)
    print(nums)

    nums1 = [1, 2, 3, 0, 0, 0]
    nums2 = [4,5,6]
    nums = solution.merge(nums1, 3, nums2, 3)
    print(nums)

    nums1 = [0]
    nums2 = [1]
    nums = solution.merge(nums1, 0, nums2, 1)
    print(nums)

    nums1 = [2,0]
    nums2 = [1]
    nums = solution.merge(nums1, 1, nums2, 1)
    print(nums)