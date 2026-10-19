'''
给定两个大小分别为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。请你找出并返回这两个正序数组的 中位数 。
算法的时间复杂度应该为 O(log (m+n)) 。

输入：nums1 = [1,3], nums2 = [2]
输出：2.00000
解释：合并数组 = [1,2,3] ，中位数 2

输入：nums1 = [1,2], nums2 = [3,4]
输出：2.50000
解释：合并数组 = [1,2,3,4] ，中位数 (2 + 3) / 2 = 2.5

输入：nums1 = [0,0], nums2 = [0,0]
输出：0.00000

输入：nums1 = [2], nums2 = []
输出：2.00000

方法1：归并排序。
这个时间复杂度为O(M+N)
但是也通过了

方法2：已知两个数组是两个升序的数组，能不能 不通过归并的方式来确定中位数的值呢，答案是可以的

https://www.algomooc.com/1428.html
https://zhuanlan.zhihu.com/p/675463009
例1：
如果是中位数一定满足 i+j=(m+n+1)//2
我们首先确定第一个位置，即i的位置，那么
j=(m+n+1)//2-i
此时我们的目标是 LMAX1<=RMIN1
LMAX2<=RMIN2

k=(m+n+1)//2=5
nums1= [7, 8,  9 ,10 ]    i的左边为[7] i的右边为[8,9,10]
        l          r
           i
nums2=[1, 2,  2,  4,  5, 6]   j=5-1=4 j的左边为 [1,2,2,4] j的右边为[5,6]
                      j

Lmax1>=Rmin2 Lmax2<=Rmin1 不满足条件(Lmax1<=Rmin2 Lmax2<=Rmin1)
由于Lmax1>=Rmin2所以，r=i-1 (缩小左界)

nums1= [7, 8,  9 ,10 ]    i的左边为[] i的右边为[7,8,9,10]
        l
        r
        i
nums2=[1, 2,  2,  4,  5, 6]   j=5-1=4 j的左边为 [1,2,2,4] j的右边为[5,6]
                      j
Lmax1>=Rmin2 Lmax2<=Rmin1 不满足条件(Lmax1<=Rmin2 Lmax2<=Rmin1)
向左收缩区间 r=i-1 ,此时跳出循环。

i j分别代表两个区间 nums1[:i+1]  nums1[:j+1] 代表左区间，如果为奇数，则为i和j指向的最大值，如果为偶数，c1=max(nums1[i],nums2[j])，由于i退出了边界，所以Lmax1=-9999(指定一个最小值即可)

例2：
k=5
nums1=[1, 2, 3, 4 ]
       l        r
          i
nums2=[5, 6, 7, 8, 9]
             j
Lmax1<=Rmin2 Lmax2>=Rmin1(不满足条件)
由于 Lmax1<=Rmin2 l=i+1

nums1=[1, 2, 3, 4 ]
             l  r
             i
nums2=[5, 6, 7, 8, 9]
          j
Lmax1<=Rmin2 Lmax2>=Rmin1(不满足条件)
l=i+1

nums1=[1, 2, 3, 4 ]
                l,r
                 i
nums2=[5, 6, 7, 8, 9]
       j

Lmax1<=Rmin2 Lmax2>=Rmin1(不满足条件)
l=i+1
移出边界，此时 LMax1=4 Rmin1=99999 (设置一个极大的数)

注意，这个方法也适用于其中一个数组为空的情况
nums1=[]
nums2=[1,2,3,4]

l,r=0,0
i=0 指向0的位置，左边刚好为[]
'''
from typing import *
class Solution:
    def findMedianSortedArrays1(self, nums1: List[int], nums2: List[int]) -> float:
        newnums = []
        i, j = 0, 0
        # 归并排序
        while i < len(nums1) and j < len(nums2):
            if nums1[i] < nums2[j]:
                newnums.append(nums1[i])
                i += 1
            else:
                newnums.append(nums2[j])
                j += 1
        if i == len(nums1):
            newnums += nums2[j:]
        else:
            newnums += nums1[i:]

        # 计算中位数
        length = len(nums1) + len(nums2)
        if length % 2 == 0:
            return (newnums[length // 2] + newnums[length // 2 - 1]) / 2
        else:
            return newnums[length // 2]

    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # 判断nums1和nums2为空的情况
        if len(nums1)>len(nums2):
            nums1,nums2=nums2,nums1
        m,n=len(nums1),len(nums2)
        l,r=0,m
        k=(m+n+1)//2
        while l<=r:
            i=l+(r-l)//2
            j=k-i
            Lmax1= -99999 if i==0 else nums1[i-1]
            Rmin1= 99999 if i==m else nums1[i]
            Lmax2=-99999 if j==0 else nums2[j-1]
            Rmin2=99999 if j==n else nums2[j]

            # 符合条件递归结束
            if Lmax1<=Rmin2 and Lmax2<=Rmin1:
                c1 = max(Lmax1, Lmax2)
                c2 = min(Rmin1,Rmin2)

                if (m+n)%2==0:
                    return (c1+c2)/2
                else:
                    return c1
            elif Lmax1<=Rmin2:
                l=i+1
            else:
                r=i-1



if __name__=="__main__":
    solution=Solution()
    if False:
        nums1 = [1, 2, 2, 4, 5,6]
        nums2 = [7,8,9,10]

        res=solution.findMedianSortedArrays(nums1,nums2)
        print(res)
    if False:
        nums1 =[1, 3]
        nums2=[2]
        res=solution.findMedianSortedArrays(nums1,nums2)
        print(res)
    if False:
        nums1 =[1, 2]
        nums2=[3,4]
        res=solution.findMedianSortedArrays(nums1,nums2)
        print(res)
    if False:
        nums1=[]
        nums2=[1,2]
        res=solution.findMedianSortedArrays(nums1,nums2)
        print(res)
    if True:
        nums1 =[3]
        nums2=[-2,-1]
        res = solution.findMedianSortedArrays(nums1, nums2)
        print(res)