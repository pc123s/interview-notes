'''
写一个程序，输出从 1到n数字的字符串表示。
如果 n是3的倍数，输出“Fizz”，
如果 n 是5的倍数，输出“Buzz”
3.如果 n 同时是3和5的倍数，输出“FuzzBuzz”
'''
class solution():
    def fizzBuzz(self, n):
        for i in range(1,n):
            if i%3 and i%5==0:
                print("FuzzBuzz")
            elif i%5==0:
                print("Buzz")
            elif i%3==0:
                print("Fizz")
            else:
                print(i)

if __name__=="__main__":
    my_solution = solution()
    n = 15
    a = my_solution.fizzBuzz(n)
    print(a)
