'''

示例 1：

输入：nums = [1,1,2]
输出：2, nums = [1,2,_]
解释：函数应该返回新的长度 2 ，并且原数组 nums 的前两个元素被修改为 1, 2 。不需要考虑数组中超出新长度后面的元素。
示例 2：

输入：nums = [0,0,1,1,1,2,2,3,3,4]
输出：5, nums = [0,1,2,3,4]
解释：函数应该返回新的长度 5 ， 并且原数组 nums 的前五个元素被修改为 0, 1, 2, 3, 4 。不需要考虑数组中超出新长度后面的元素。

思路1：采用双指针的方式，跟冒泡排序的双指针一样，i和j，i指向当前元素，j指向需要去重的元素。这种的时间复杂度为O(n2)
思路2：采用hash表进行去重。
一个set表存储已经出现的元素，如果后续有元素存在的话，则将其置为_,然后二次循环将_删除

[1,1,2,2,3,3,4,4]
[1,_,2,_,3,_,4,_]
再将_删除


'''
from typing import *
from collections import defaultdict

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        mp=defaultdict(int)
        n=len(nums)
        for index,num in enumerate(nums):
            if num in mp:
                nums[index]="_"
            else:
                mp[num]=1
        return [str_ for str_ in nums if str_!="_"]


if __name__=="__main__":
    solution=Solution()
    if True:
        nums=[1,1,2]
        res=solution.removeDuplicates(nums)
        print(res)
    if True:
        nums = [0,0,1,1,1,2,2,3,3,4]
        res = solution.removeDuplicates(nums)
        print(res)