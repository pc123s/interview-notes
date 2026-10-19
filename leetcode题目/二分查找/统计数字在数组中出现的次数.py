'''
统计一个数字在排序数组中出现的次数。
输入: nums = [5,7,7,8,8,10], target = 8
输出: 2

输入: nums = [5,7,7,8,8,10], target = 6
输出: 0

方法还是采用二分查找，如果找到了进行前后的便利，没有找到的话。返回0
'''
from typing import *
class solution:
    def search(self,nums:List[int],target:int)->int:
        if not nums:
            return 0
        n=len(nums)
        l,r=0,n-1
        target_index=-1 #初始化一个index记录寻找到的索引
        while l<=r:
            mid=l+(r-l)//2
            if nums[mid]==target:
                target_index=mid
                break
            elif nums[mid]>target:
                r=mid-1
            else:
                l=mid+1
        count=0 #记录数字出现了几次
        if target_index==-1:
            return count
        else:
            l,r=0,0
            i=target_index
            while i>0:
                if nums[i]!=target:
                    l=i
                    break
                i-=1
            j=target_index
            while j<n:
                if nums[j]!=target:
                    r=j
                    break
                j+=1
            return r-l-1


if __name__=="__main__":
    solution=solution()
    res=solution.search([1,1,2,2,3,3,3,4,5,6],target=3)
    print(res)
    res = solution.search([0,0,1, 1, 2, 2, 3, 3, 3, 4, 5, 6], target=1)
    print(res)
    res = solution.search([0,0,1, 1, 2, 2, 3, 3, 3, 4, 5, 6], target=0)
    print(res)