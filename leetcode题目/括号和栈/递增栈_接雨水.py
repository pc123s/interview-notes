'''
接雨水
给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出：6
解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。
1-0-2 1 2-1-0-1
2+1+2+1+2+1+1=9

输入：height = [4,2,0,3,2,5]
输出：9
height =[4,2,3]
输出:1

height =
[6,8,5,0,0,6,5]
输出：13

height =
[0,2,0]
输出0
思路：双指针，两个指针，一个i,一个j从i+1开始向后循环，i不得从0开始，因为0接不住雨水。遇到i大，取i和j对应值得最小值，求中间数的和。再次从j开始后一轮循环。
[0 , 1 , 0 , 2 , 1 , 0 , 1 , 3 , 2 , 1 , 2 , 1 ]
     i       j
第一轮装雨水，num=min(1,2)=1
i+1->j 0+(1-0)=1
或者计算可以算为： sum([1,0])=1 len([1,0])= 2 1*2-1=1
[0 , 1 , 0 , 2 , 1 , 0 , 1 , 3 , 2 , 1 , 2 , 1 ]
             i               j
第二轮装雨水 min(2,3)=2
i+1->j  2-1+2-0+2-1=1+2+1=4
choose_num=[2,1,0,1] len(choose_num)=4 2*4-(2+1+1)=8-4=4
[0 , 1 , 0 , 2 , 1 , 0 , 1 , 3 , 2 , 1 , 2 , 1 ]
                             i           j
第三轮装雨水 此时我们发现i以后的数都是比i小的，记录到min_num=2
choose_num=[2,1,2] len(choose_num)=3 2*3-(2+1+2)=1

继续更新i i=j
[0 , 1 , 0 , 2 , 1 , 0 , 1 , 3 , 2 , 1 , 2 , 1 ]
                                         i   j

第四轮接雨水的结果为 0
此时i=j, i>n跳出循环
choose_num=[2,1,2]
2*3-5=1
最终的接雨水的结果为 1+4+1=6

方法2：使用单调递增栈的方式进行计算
https://www.algomooc.com/627.html
怎么计算呢，我们知道只有这个数比左右两边的数小才能形成一个凹槽，这个很符合递增栈的逻辑。
比如 [5,4,2,1] 2(输入)，此时2比1大，那么2,1,2形成一个凹槽，但是要注意一种情况，那就是栈顶左边的元素一定要比栈顶大才能形成凹槽，否则无法形成凹槽。比如[5,4,2,2] 3。2,2,3不是凹槽
height = [0,1,0,2,1,0,1,3,2,1,2,1] 以这个为例,并且我们在利用最小栈求面积时存在栈顶和栈尾的元素不连贯的现象。所以我们需要一个辅助数组来模拟已经形成的元素的占位空间

0 栈[0]
1 栈[0]
1比0大，可以行成凹槽，将0弹出，stack=[] 说明凹槽没有左壁,将1加入
0 栈[1,0]
2 栈[1,0]  此时2比栈尾0大，可以行成凹槽
while
    1、把0弹出 buttom=0 h=min(1,2)=1
    h=1-0
    w=index2-index1-1
    重复上面的操作，注意，弹出后要看看stack是否为空，为空代表左侧没有木桶了
res1=h*w=1
将2加进去 stack=[2]
1 栈[2,1]
0 栈[2,1,0]
1 栈[2,1,0] 1,0,1形成凹槽
while
    不断弹出 尾部为buttom
    得到res2=1
    [2,1] 1 不是凹槽跳过

3 栈[2,1,1]和3 形成凹槽，
while:
    buttom=1 h=min(1,3)=1
    w=2 res=2*(1-1)=0
    [2,1] 3
    w=4 h=min(2,3)-1=1
    res3=4
    [2] 3
    2弹出后stack为空了 不进行计算了

stack=[3]

2 栈[3,2]
1 栈[3,2,1]
2 栈[3,2,1]
while:
    h=min(2,2)=2 buttom=1
    res4=(2-1)*1=1
    stack=[3,2]
    h=min(3,2)=2
    buttom=2
    res5=(2-2)*w=0

1 [2] 全部结束

例子2 [5,4,1,2]
5 [5]
4 [5,4]
1 [5,4,1]
2 [5,4,1] h=min(1,2)=2 res=2-1=1

'''
from typing import *
class Solution:
    def trap(self, height: List[int]) -> int:
        i,j=0,0
        res=0 #记录接雨水的总量
        n=len(height)
        while i<n-1:
            is_get_num=False
            if height[i]==0:
                i+=1
                continue
            j=i+1
            min_num,j_=0,0 #如果发现当前指针比i小，我们需要搜寻后续整个空间的次大值。并记录下来
            while j<n:
                if height[j]>=height[i]:
                    choose_num=height[i+1:j]
                    #print(choose_num)
                    m=len(choose_num)*min(height[i],height[j])-sum(choose_num)
                    res+=m
                    i=j
                    is_get_num=True
                    break
                else:
                    if height[j]>=min_num:
                        min_num=height[j]
                        j_=j

                    j+=1
            #print(i, j , m)
            if not is_get_num:
                choose_num = height[i+1:j_]
                #print(choose_num)
                m = len(choose_num) * min(height[i], min_num) - sum(choose_num)
                res+=m
                i=j_
        return res


class Solution1:
    def trap(self, height: List[int]) -> int:
        stack=[] #存储一个单调递增栈
        res=0 #记录所有的雨水
        for i,h in enumerate(height):
            if not stack:
                stack.append(i)
            #栈顶元素比递增栈的栈顶元素小,入栈
            elif height[i]<height[stack[-1]]:
                stack.append(i)
            # 如果栈顶元素等于递增栈的栈顶元素，无法形成凹槽，入栈
            elif height[i]==height[stack[-1]]:
                stack.append(i)
            # 情况三：此时的的元素大于栈顶元素，有可能形成凹槽
            # 注意是有可能形成，因为比如栈中的元素是 2 、2 ，此时的元素是 3，那么是无法形成凹槽的
            else:
                while stack and height[i]>height[stack[-1]]:
                    # bottom=stack[-1]
                    # 将栈顶元素弹出
                    bottom=stack.pop()
                    if stack:
                        #这里要注意，为什么可以默认[2,2] 3这样的左凹槽也是存在的呢，，其实如果左凹槽和bottom的值一样也不要紧，因为这时 h为0,计算的面积值也为0
                        # 所以这里每次进行递增栈时先对左右的凹槽高度进行计算。
                        h=min(height[stack[-1]],height[i])-height[bottom]
                        w=i-stack[-1]-1
                        res+=(h*w)
                stack.append(i)
        return res
'''
方法3， 接雨水主要是构建凹槽
height = [0,1,0,2,1,0,1,3,2,1,2,1]
用这个数组来看 如果我能确定左右两边的最高高度，那么久很容易求出来接雨水的数量
leftmax代表所有点左边的最高高度,rightmax代表点i及右边的最高高度
height = [0,1,0,2,1,0,1,3,2,1,2,1]
leftmax =[0,1,1,2,2,2,2,3,3,3,3,3]
rightmax=[3,3,3,3,3,3,3,3,2,2,2,1]
0:res=min(0,3)-0=0
1:res=min(1,3)-1=0
0:res=min(1,3)-0=1
2:res=min(2,3)-2=0
1:res=min(2,3)-1=1
0:res=min(2,3)-0=2
1:res=min(2,3)-1=1
3:res=min(3,3)-3=0
2:res=min(2,3)-2=0
1:res=min(3,2)-1=1
2:res=min(3,2)-2=0
1:res=min(3,1)-1=0  
结果为：1+1+2+1+1=6
leftmax[i]=max(leftmax[i-1],height[i])
rightmax[i]=max(height[i],rightmax[i+1])
'''
class Solution2:
    def trap(self, height: List[int]) -> int:
        n=len(height)
        leftMax=[height[0]]+[0]*(n-1)
        rightMax=[0]*(n-1)+[height[-1]]
        for i in range(1,n):
            leftMax[i]=max(leftMax[i-1],height[i])
        for i in range(n-2,-1,-1):
            rightMax[i]=max(rightMax[i+1],height[i])
        res=sum([min(leftMax[i],rightMax[i])-height[i] for i in range(n)])
        return res
if __name__=="__main__":
    solution=Solution2()
    if True:
        res=solution.trap([0,1,0,2,1,0,1,3,2,1,2,1])
        print(res)
    if True:
        res = solution.trap([4,2,0,3,2,5])
        print(res)
    if True:
        res = solution.trap([6,8,5,0,0,6,5])
        print(res)
    if True:
        res = solution.trap([5,4,1,2])
        print(res)
    if True:
        res = solution.trap([0,2,0])
        print(res)