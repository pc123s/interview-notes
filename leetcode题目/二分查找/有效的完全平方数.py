'''
给你一个正整数 num 。如果 num 是一个完全平方数，则返回 true ，否则返回 false 。

完全平方数 是一个可以写成某个整数的平方的整数。换句话说，它可以写成某个整数和自身的乘积。

不能使用任何内置的库函数，如  sqrt 。

示例 1：

输入：num = 16
输出：true
解释：返回 true ，因为 4 * 4 = 16 且 4 是一个整数。
示例 2：

输入：num = 14
输出：false
解释：返回 false ，因为 3.742 * 3.742 = 14 但 3.742 不是一个整数。

提示：
1 <= num <= 231 - 1
思路1：
1 4 9 16 25 36
1 2 3 4  5  6

采用二分查找，我们可以发现如果是完全平方数，那么一定右n*n=m.只要确定了n就可以，我们同样可以发现，除了1以外，所有的完全平方数都是小于2/m的
所以这个可以采用二分查找进行迭代。
'''
from math import ceil
class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        l,r=0,num
        threhold=ceil(num/2)
        while l<=r:
            mid=l+(r-l)//2
            if mid*mid==num:
                return True
            elif mid*mid>num:
                r=mid-1
            elif mid>threhold:
                return False
            else:
                l=mid+1
        return False
    def isperfectSquare1(self,num)->bool:
        l,r=0,num
        threhold=ceil(num/2)
        while l<=r:
            mid=l+(r-l)//2
            if mid*mid==num:
                return True
            elif mid*mid>num:
                r=mid-1
            elif mid>threhold:
                return False
            else:
                l=mid+1
        return False
if __name__=="__main__":
    solution=Solution()
    res=solution.isperfectSquare1(16)
    print(res)
    res = solution.isperfectSquare1(24)
    print(res)