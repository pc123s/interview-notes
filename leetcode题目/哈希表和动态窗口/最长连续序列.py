'''
给定一个未排序的整数数组 nums ，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。
请你设计并实现时间复杂度为 O(n) 的算法解决此问题。
示例 1：

输入：nums = [100,4,200,1,3,2]
输出：4
解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。
示例 2：

输入：nums = [0,3,7,2,5,8,4,6,0,1]
输出：9

思路：
1、先使用一个set数组对list进行去重。
[100,4,200,1,3,2]
2、对这个set进行遍历，找到连续数组的头
(1) 是头的标准，num-1不在这个set中。 查找是O(1)的
(2) 如果找到了，则不断对这个num+=1找到队尾

'''
from typing import *

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        set_nums=set(nums)
        len_max=0
        for num in set_nums:
            # 如果num是头，那么num-1
            if num-1 not in set_nums:
                start_=num
                # 此时start_是队头
                seq_len=1
                while start_+1 in set_nums:
                    seq_len+=1
                    start_+=1
                len_max=max(seq_len,len_max)

        return len_max

if __name__=="__main__":
    solution=Solution()
    if True:
        nums=[100,4,200,1,3,2]
        res =solution.longestConsecutive(nums)
        print(res)
    if True:
        nums=[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
        res =solution.longestConsecutive(nums)
        print(res)
