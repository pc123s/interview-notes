'''
有很多线段的起点和终点，其中有的有重叠部分，计算这些线段的有效长度，去除其中的重复部分。
num_list1=[[1,3],[2,7],[9,11],[13,20],[15,30]]
有效长度为 1-3 2-7->1-7=6 9-11=2 13-20,15-30->13-30
6+2+17=25
num_list2=[[1,3],[2,6],[11,12],[10,13]]
1-3,2-6=1-6=5 11-12,10-13=10-13=3
5+3=8
'''
from typing import *
class Solution():
    def find_vaild_length(self,num_list):
        # 排序
        num_list.sort()
        n=len(num_list)
        arr=[]
        i,j=0,1 #计算相交的长度
        set_l=0
        print(num_list)
        while i<n-1:
            a, b=num_list[i][0],num_list[i][1]
            c, d=num_list[j][0],num_list[j][1]
            if b>=c:#相交
                if b>=d: #c-d为焦点
                    set_l+=(d-c)
                else:
                    set_l+=(b-c)
            else:
                #不相交
                pass
            i+=1
            j+=1
        sum_l=sum([i[1]-i[0] for i in num_list])
        return sum_l-set_l
if __name__=="__main__":
    solution=Solution()
    num_list1 = [[1, 3], [2, 7], [9, 11], [13, 20], [15, 30]]
    res1=solution.find_vaild_length(num_list1)
    print(res1)
    num_list2 = [[1, 3], [2, 6], [11, 12], [10, 13]]
    res2=solution.find_vaild_length(num_list2)
    print(res2)