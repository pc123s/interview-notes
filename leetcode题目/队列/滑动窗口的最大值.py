'''
给你一个整数数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。
返回 滑动窗口中的最大值 。
示例 1：
输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
输出：[3,3,5,5,6,7]
输入：
[9,10,9,-7,-3,8,2,-6],5
返回值：
[10,10,9,8]

方法1-暴力法：采用滑动窗口 每次遍历其中的窗口，求出最大值 这个方法的时间复杂度为o(k*n)

方法2-递减队列去存储滑动窗口的最大值（队列顶端值）
时间复杂度O(n),空间复杂度O（k）
我们使用一个递减队列存储其中的最大值
1 3 -1 -3 5 3 6 7
i
queue={1}
1 3 -1 -3 5 3 6 7
  i
queue={3}

1 3 -1 -3 5 3 6 7
    i
queue={3 -1}
arr=[3]
1 3 -1 -3 5 3 6 7
        i
queue={3 -1 -3}
arr=[3,3]
1 3 -1 -3 5 3 6 7
          i
queue={5}
arr=[3,3,5]
1 3 -1 -3 5 3 6 7
            i
queue={5}
arr=[3,3,5,5]
1 3 -1 -3 5 3 6 7
              i
queue={6}
arr=[3,3,5,5,6]
1 3 -1 -3 5 3 6 7
                i
queue={7}
arr=[3,3,5,5,6,7]

方法3：其实方法3和方法2是相似的，采用一个最大栈来存储前k个元素
从k+1个元素开始往后移动，每次需要判断下，k+1的元素和 窗口的第一个元素的值
如果窗口的第一个元素比 新加入的元素小，不操作（因为不影响最大值的选择）
如果窗口的第一个元素比新加入的元素大，则需要删除当前元素

1 3 -1 -3 5 3 6 7
i    j
k=3
q={3,1} # arr=[3]

1 3 -1 -3 5 3 6 7
  i    j
k=3
q={3,1}
比较 -3和3,-3小，所以直接append
q={3,1,-3} arr=[3,3]

1 3 -1 -3 5 3 6 7
     i    j
k=3
q={3,1,-1}
比较 5和3,5比3大，维持最大栈
q={5} arr=[3,3,5]

1 3 -1 -3 5 3 6 7
       i    j
k=3
q={5}
比较 3和5,3比5小，append
q={5,3} arr=[3,3,5,5]

一直持续到完

'''
from typing import *
from collections import deque
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n=len(nums)
        # arr记录所有的结果
        arr=[]
        for i in range(n):
            j=i+k
            if j<=n:
                arr.append(max(nums[i:j]))
        return arr

    from collections import deque
    def maxSlidingWindow2(self, nums: List[int], k: int) -> List[int]:
        n=len(nums)
        q=deque()
        # 我们使用队列来制作一个最大栈
        # q={} 队列的队首放最大的元素
        arr=[] #记录滑动窗口的最大值
        for i in range(k):
            while q and q[-1]<nums[i]:
                q.pop()
            q.append(nums[i])
        arr.append(q[0])
        for j in range(k,n):
            new_num=nums[j]
            q_first=nums[j-k]
            # 最大栈的最大元素刚好是队首，将其弹出
            if q[0]==q_first:
                q.popleft()
            # j-k的值比当前值大，那么可能影响最大栈
            while q and q[-1]<new_num:
                q.pop()
            q.append(new_num)
            arr.append(q[0])
        return arr






if __name__=="__main__":
    solution=Solution()
    if True:
        arr=solution.maxSlidingWindow2([1,3,-1,-3,5,3,6,7],3)
        print(arr)
    if True:
        arr=solution.maxSlidingWindow2([9,10,9,-7,-3,8,2,-6],5)
        print(arr)
