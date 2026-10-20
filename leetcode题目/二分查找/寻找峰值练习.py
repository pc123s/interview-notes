from typing import *
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        while l<r:
            mid=l+(r-l)//2
            if nums[mid]<=nums[mid+1]:
                l=mid+1
            else:
                r=mid-1
        return l

if __name__=="__main__":
    solution=Solution()
    if True:
        index=solution.findPeakElement([1,2,3,1])
        print(index)
        index=solution.findPeakElement([1,2,1,3,5,6,4])
        print(index)
        index=solution.findPeakElement([3,1,2])
        print(index)
        index=solution.findPeakElement([6,5,4,3,2,3,2])
        print(index)