'''
描述
数字以 0123456789101112131415... 的格式作为一个字符序列，在这个序列中第 2 位（从下标 0 开始计算）是 2 ，第 10 位是 1 ，第 13 位是 1 ，以此类题，请你输出第 n 位对应的数字。
https://www.nowcoder.com/practice/29311ff7404d44e0b07077f4201418f5?tpId=13&tqId=2285751&ru=%2Fpractice%2Fe8a1b01a2df14cb2b228b30ee6a92163&qru=%2Fta%2Fcoding-interviews%2Fquestion-ranking&sourceUrl=%2Fexam%2Foj%2Fta%3Fpage%3D1%26tpId%3D13%26type%3D13
示例1
输入：0
返回值：0
示例2
输入：2
返回值：2
输入：10
返回值：1
示例4
输入：13
返回值：1

输入在0-9
10-1
10,100
比如10 对应的 10的1
11 对应的10 的0
12 对应的11的1
13 对应11的1
14 对应12的1
15 对应12的2
16 对应13的1
17 对应13的3
0-9 每1位对应1位，共有9位 0<=n<=9
10-99 是每两位对应1位，共有180位  9+1<=n<=9+9*(10^1)*2 10<=n<=9+180
100-999 每3位对应1位，共有900*3=2700位  189+1<=n<=189+9*(10^2)*3 190<=n<=2700+189
1000-9999 每4位对应1位，共有9000*4 同样可以确定完这个的上下限


输入n 我们先判断其范围
具体为
设置两个数 0,9和digit
digit=0 代表 n的数字在1位  除此以外还能算出 对应的上下限 0-9
digit=1 代表n的数字是2位    10 189
digit=2 代表n的数字是3位... 190 2700+189
(n-190)/digit= 可以得到整数和余数，整数代表第几个数字，余数代表后面的字符
比如 17 （17-10）/2=3..1 代表是13的第二个数字那么就是3


'''

class Solution:
    def findNthDigit(self , n: int) -> int:
        # write code here
        # a,b=1,10
        if 0<=n and n<=9:
            return n
        digit=0
        down,up=0,9
        while True:
            print(up, down)
            if n>=down and n<=up:
                break
            else:
                digit+=1
                down=up+1
                up=up+9*(10**digit)*(digit+1)
        gap=n-down
        a,b=divmod(gap,digit+1)
        a=1*(10**digit)+a
        a_=str(a)
        print(a_,b)
        #print(a_[b])
        print(a_[b])
        return a_[b]
if  __name__=="__main__":
    solution=Solution()
    if False:
        solution.findNthDigit(9)
    if False:
        solution.findNthDigit(1000000)
    if True:
        solution.findNthDigit(1000000000)
