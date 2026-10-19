'''
给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。
请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。
示例 1:
输入: [3,2,1,5,6,4] 和 k = 2
输出: 5

排序后倒数第二个是5

示例 2:
输入: [3,2,3,1,2,4,5,5,6] 和 k = 4
输出: 4

排序后倒数第四个是4

思路1:排序然后计算k
这个时间复杂度为O（nlog(n)）

思路2：
采用快排的思路

https://leetcode.cn/problems/xx4gT2/solutions/1398893/shu-zu-zhong-de-di-k-da-de-shu-zi-by-lee-6doi/
作者：随便发挥
链接：https://zhuanlan.zhihu.com/p/695980029
'''
from typing import *
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        n = len(nums)
        l = 0
        r = n - 1
        while True:
            idx = self.partition(nums, l, r)
            if idx == k - 1:
                return nums[idx]
            elif idx < k - 1:
                l = idx + 1
            else:
                r = idx - 1


    #----左右挖坑互填
    def partition(self, nums: List[int], l: int, r: int) -> int:
        pivot = nums[l]
        while l < r:
            while l < r and nums[r] <= pivot:
                r -= 1
            nums[l] = nums[r]
            while l < r and nums[l] >= pivot:
                l += 1
            nums[r] = nums[l]

        nums[l] = pivot
        return l

作者：HanXin
链接：https://leetcode.cn/problems/xx4gT2/solutions/943011/cpython3java-1da-gen-dui-diao-ku-2shou-l-ctnx/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。