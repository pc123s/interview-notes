from typing import *

def mergeSort(nums:List[int])->List[int]:
    n=len(nums)
    if n<2:
        print(nums)
        return nums
    mid=(0+n)//2
    left_part=mergeSort(nums[0:mid])
    right_part=mergeSort(nums[mid:n])
    return merge(left_part,right_part)
def merge(left,right):
    arr=[] #存储
    while left and right:#left和right不为空
        if left[0]<right[0]:
            arr.append(left.pop(0))
        else:
            arr.append(right.pop(0))
    if left:
        arr.extend(left)
    if right:
        arr.extend(right)
    return arr
'''
[  2     1   3    4    6      5 ]
  left                      right
  mid
  nums[right]>nums[mid]  right-=1
[  2     1   3    4    6      5 ]
  left                right
  mid
  nums[right]>nums[mid]  right-=1
  
[  2     1   3    4    6      5 ]
  left           right
  mid
  nums[right]>nums[mid]  right-=1

[  1      2   3    4    6      5 ]
  left  right
        mid
  pviot=2 
  nums[right]<nums[mid]  
  pivot=nums[mid]
  nums[mid]=nums[right]
  nums[mid]=pivot
  mid=right
移动左边


'''
def partion(nums,left,right)->int:
    '''
    对nums的左边和右边进行排序
    :param nums:
    :param left:
    :param right:
    :return:
    返回选择排序比较好的位置
    '''
    pivot=nums[left]
    while left<right:
        while left<right and nums[right]>=pivot:
            right-=1
        # nums[right] 比pivot小应该放左边
        nums[left]=right
        while left<right and nums[left]<=pivot:
            left+=1
        nums[right]=nums[left]
    nums[left]=pivot
    return left

def quickSort(nums,left,right):
    if left>=right:
        return
    mid=partion(nums,left,right)
    quickSort(nums,left,mid-1)
    quickSort(nums,mid+1,right)
    return nums





if __name__=="__main__":
    nums=[3,2,1,3,4,5]
    arr=mergeSort(nums)
    print(arr)
    nums = [3, 2, 1, 3, 4, 5]
    arr=quickSort(nums,0,len(nums)-1)
    print(arr)