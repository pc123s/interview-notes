'''
返回值描述：
输出所有和为S的连续正数序列。序列内按照从小至大的顺序，序列间按照开始数字从小到大的顺序
示例1
输入：
9
返回值：[[2,3,4],[4,5]]
输入：
0
返回值：[]
分别看是几位正整数
2位 9/2=4.5 4.5向下取整 4 2/2=1 4-(1-1)
3为 9//2=3  3为平均数，分别向前和后延伸3//2=1
4位 9/(4/2)=4.5

我们发现，如果是连续的奇数，那么中间的数就是平均值，如果是连续的偶数，那么中间的数为偶数序列为n 中间的值为中间两数相加= sum/(n/2),n=2除外
偶数，那么向外推，
比如 18  4个序列， 18/(4/2)=9 9//2=4 4-(4/2-1)=3 3 4 5 6
20 20/(4/2)=10 10是偶数就不是
中间是和就会出现几种情况：
中间的和不是整数：
1、比如20/3
2、中间是整数，
（1）奇数
偶+奇 4+5 5+6，即我们的和一定是个奇数，才能有效，比如和为10,这不是两个连续数相加的结果
（2）偶数
无效



12
2位 12/2=6 不行
3为 12//3=4  4为平均数，分别向前延伸3//2=1位 3 4 5
4位 12//3=4 不行
5位 12/5=2.4
6位 12/6=2
位数不会超过12根号 6

18
4位 18/(4/2)=9  4+5



'''
from  typing import *
import math
class Solution:
    def FindContinuousSequence(self , sum: int) -> List[List[int]]:
        if sum==1:
            return []
        a=math.sqrt(sum)
        n=math.ceil(a)
        res=[]
        for i in range(n+1,1,-1):
            conti_l=self.findContinueL(sum,i)
            if conti_l:
                res.append(conti_l)
        return res
    def findContinueL(self,sum,n)->List:
        arr=[]
        if self.isOdd(n):
            half_n=n/2
            res=sum/half_n

            if res==sum//half_n:
                if not self.isOdd(res):#是奇数
                    b=res//2
                    c=n/2-1
                    start_num=int(b-c)
                    if start_num<=0:
                        return []
                    for i in range(start_num,start_num+n):
                        arr.append(i)
            else:
                #非整数
                return []
        else: #是奇数的连续序列
            res=sum/n
            if res!=sum//n:#非整数
                return arr
            else:#整数
                half_n=n//2
                start_num=int(res-half_n)
                if start_num <= 0:
                    return []
                for i in range(start_num,start_num+n):
                    arr.append(i)
        return arr

    def isOdd(self,num):
        if num%2==0:
            return True
        else:
            return False
if __name__=="__main__":
    solution=Solution()
    if False:
        res=solution.FindContinuousSequence(9)
        print(res)
    if False:
        res=solution.FindContinuousSequence(12)
        print(res)
    if False:
        res=solution.FindContinuousSequence(4)
        print(res)
    if False:
        res=solution.FindContinuousSequence(15)
        print(res)
    if True:
        res=solution.FindContinuousSequence(15)
        print(res)