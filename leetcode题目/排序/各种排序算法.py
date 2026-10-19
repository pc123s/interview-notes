'''
将介绍几个排序算法
https://zhuanlan.zhihu.com/p/512365889
https://www.cxyxiaowu.com/725.html

1、冒泡排序
两个指针，从左向右.发现后面的比前面的小，将小的换到前面  时间O(n2) 空间O（1）
2、选择排序
时间 O（n2） 空间 O(1)
首先在未排序序列中找到最小（大）元素，存放到排序序列的起始位置。
再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。
重复第二步，直到所有元素均排序完毕。

3、插入排序
将第一待排序序列第一个元素看做一个有序序列，把第二个元素到最后一个元素当成是未排序序列。
从头到尾依次扫描未排序序列，将扫描到的每个元素插入有序序列的适当位置。（如果待插入的元素与有序序列中的某个元素相等，则将待插入元素插入到相等元素的后面。）
[ 1  2  3      1  6  7 ] cur=1
       pre    cur
[ 1  2  3      3  6  7 ]
       pre               cur=1
[ 1  2  2      3  6  7 ]
    pre                  cur=1
[ 1  2  2      3  6  7 ]
    pre                  cur=1
4、归并排序
作为一种典型的分而治之思想的算法应用，归并排序的实现由两种方法：

1、自上而下的递归（所有递归的方法都可以用迭代重写，所以就有了第 2 种方法）；
2、自下而上的迭代。
因为始终都是 O(nlogn) 的时间复杂度。
1. 算法步骤
申请空间，使其大小为两个已经排序序列之和，该空间用来存放合并后的序列；
设定两个指针，最初位置分别为两个已经排序序列的起始位置；
比较两个指针所指向的元素，选择相对小的元素放入到合并空间，并移动指针到下一位置；
重复步骤 3 直到某一指针达到序列尾；
将另一序列剩下的所有元素直接复制到合并序列尾。

5、快速排序

从数列中挑出一个元素，称为 “基准”（pivot）；
重新排序数列，所有元素比基准值小的摆放在基准前面，所有元素比基准值大的摆在基准的后面（相同的数可以到任一边）。在这个分区退出之后，该基准就处于数列的中间位置。这个称为分区（partition）操作；
递归地（recursive）把小于基准值元素的子数列和大于基准值元素的子数列排序。
[2 , 2,  3 , 1 , 2 , 4 , 5 , 8]
left                       right
pivot=2
从右向左找，比pivot小的值，是1
[1 , 2,3 , 1 , 2 , 4 , 5 , 8]
 left     right
 pivot=2
nums[left] 变成小的值

# 从左向右找
[  1 , 2 ,  3 ,  1  ,  2  ,  4  ,  5  ,  8]
 left         right
 pivot=2
nums[left]<nums[pivot] left+=1

[  1 , 2 ,  3 ,  1  ,  2  ,  4  ,  5  ,  8]
          left  right
nums[right]=nums[left]
[  1 , 2 ,  3 ,  3  ,  2  ,  4  ,  5  ,  8]
          left  right

继续比较右边，left==right，此时 将mid值给left
[  1 , 2 ,  3 ,  3  ,  2  ,  4  ,  5  ,  8]
          left
          right
[  1 , 2 ,  2 ,  3  ,  2  ,  4  ,  5  ,  8]


6、计算排序
计数排序的核心在于将输入的数据值转化为键存储在额外开辟的数组空间中。作为一种线性时间复杂度的排序，计数排序要求输入的数据必须是有确定范围的整数。

以下以[ 3，5，8，2，5，4 ]这组数字来演示。
首先，我们找到这组数字中最大的数，也就是 8，创建一个最大下标为 8 的空数组 arr 。
开辟一个0-8的数组
[0  0  0  0  0  0  0  0  0]
 0  1  2  3  4  5  6  7  8
将数字放入进去
[0  0  1  1  1  2  0  0  1]
 0  1  2  3  4  5  6  7  8
然后再依次将数据取出来
[ 2 3 4 5 5 8]

 '''
import numpy as np
from typing import *
import math

def bubbleSort(arr):
    n=len(arr)
    for i in range(n-1):
        for j in range(i+1,n):
            if arr[j]<arr[i]:
                # 将其位置互相交换
                arr[i],arr[j]=arr[j],arr[i]
    return arr

# def selectionSort(arr):
#     n=len(arr)
#     for i in range(n-1):
#         minIndex=i
#         for j in range(i+1,n):
#             if arr[j]<arr[minIndex]:
#                 minIndex=j
#         if i!=minIndex:
#             arr[i],arr[minIndex]=arr[minIndex],arr[i]
#     return arr

def selectSort(arr):
    '''
    在i之前的序列是顺序的，后面非顺序
    :param arr:
    :return:
    '''
    n=len(arr)
    for i in range(n):
        minIndex=i
        for j in range(i+1,n):
            if arr[j]<arr[minIndex]:
                minIndex=j
        if i!=minIndex:
            arr[i],arr[minIndex]=arr[minIndex],arr[i]
    return arr

def insertSort(arr):
    n=len(arr)
    for i in range(1,n):
        preIndex=i-1
        cur=arr[i]
        while i>=0 and arr[preIndex]>cur:
            arr[preIndex+1]=arr[preIndex]
            preIndex-=1
        arr[preIndex]=cur
    return arr

# 归并排序
def merge(left,right):
    res=[]
    while left and right:
        if left[0]<right[0]:
            res.append(left.pop(0))
        else:
            res.append(right.pop(0))
    if left:
        res.extend(left)
    if right:
        res.extend(right)
    return res
def mergeSort(arr):
    if len(arr)<2:
        return arr
    n=len(arr)
    middle=np.floor(n//2)
    middle=int(middle)
    left,right=arr[:middle],arr[middle:]
    left_part=mergeSort(left)
    right_part=mergeSort(right)
    res=merge_pc(left_part,right_part)
    return res

def merge_pc(left,right):
    arr=[]
    while left and right:
        if left[0]<right[0]:
            arr.append(left.pop(0))
        else:
            arr.append(right.pop(0))
    if left:
        arr.extend(left)
    if right:
        arr.extend(right)
    return arr
def mergeSort_pc(arr):
    if len(arr)<2:
        return arr
    n=len(arr)
    middle=math.ceil(n/2)
    left,right=arr[:middle],arr[middle:]
    print(left,right)
    left=mergeSort_pc(left)
    right=mergeSort_pc(right)
    res=merge_pc(left,right)
    return res
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:

        for x in range(len(nums)):
            print(nums[x])

        self.quickSort(nums, 0 , len(nums) - 1)
        print("------")
        for x in range(len(nums)):
            print(nums[x])

        return None
    def QuickSort(self,arr:List[int],left:int,right:int):
        if left>=right:
            return
        mid=self.parition(arr,left,right)
        self.QuickSort(arr,mid+1,right)
        self.QuickSort(arr,left,mid-1)

        return arr

    def parition(self,arr,left,right):
        pivot=arr[left]
        while left<right:
            # 从右边开始找
            while left<right and arr[right]>=pivot:
                right-=1
            # right所在的指针比pivot小
            arr[left]=arr[right]
            while left<right and arr[left]<=pivot:
                left+=1
            # left的指针比pivot大
            arr[right]=arr[left]
        # 放入中间值
        arr[left]=pivot
        return left
    def partion_pc(self,arr,left,right):
        '''
        p=5
        5 2 1 4 5 8 9
        l           r
        9 8 5 4
        4 2 1 4 5 8 9
        l     r
        4 2 1 4
        4 2 1 4 5 8 9
              r
              l
        l和r相遇
        arr[l]=pivot

        :param arr:
        :param left:
        :param right:
        :return:
        '''
        pivot=arr[left]
        while left<right:
            while left<right and arr[right]>=pivot:
                right-=1
            arr[left]=arr[right]
            while left<right and arr[left]<=pivot:
                left+=1
            arr[right]=arr[left]
        arr[left]=pivot
        return left
    def Quicksort_pc(self,arr,left,right):
        if left>=right:
            return
        mid=self.partion_pc(arr,left,right)
        print(mid)
        self.Quicksort_pc(arr,mid+1,right)
        self.Quicksort_pc(arr,left,mid-1)
        return arr
def countSort(arr):
    maxValue=max(arr)
    indexArr=[0 for i in range(maxValue+1)] # 设置0-maxValue下标的数组
    for i in arr:
        indexArr[i]+=1
    res=[]
    for index,num in enumerate(indexArr):
        if num!=0:
            res.extend([index]*num)
    return res







if __name__=="__main__":
    arr=[4,3,1,2,4,5,8]
    # if True:
    #     arr1=bubbleSort(arr)
    #     print(arr1)
    # if True:
    #     arr1=selectionSort(arr)
    #     print(arr1)
    # if True:
    #     arr1=insertSort(arr)
    #     print(arr1)
    # if True:
    #     arr1=mergeSort(arr)
    #     print(arr1)
    if True:
        solution=Solution()
        #arr1=solution.QuickSort(arr,0,len(arr)-1)
        arr1=solution.Quicksort_pc(arr,0,len(arr)-1)
        print(arr1)
    if False:
        arr1=countSort(arr)
        print(arr1)
    if False:
        arr=selectSort(arr)
        print(arr)
    if True:
        arr=mergeSort_pc(arr)
        print(arr)
