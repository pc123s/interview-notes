from queue import Queue
from typing import List
'''
示例 1：

输入：digits = "23"
输出：["ad","ae","af","bd","be","bf","cd","ce","cf"]
示例 2：

输入：digits = ""
输出：[]
示例 3：

输入：digits = "2"
输出：["a","b","c"]
https://leetcode.cn/problems/letter-combinations-of-a-phone-number/description/
思路：
使用两个队列来承接结果
q1 q2
q1 为最终承接队列
q2 为临时的缓存队列
将数据喂入 数字对应的字符喂入q1,
q1弹出字符喂入q2,
q2弹出字符拼接数字对应的字符喂入q1

最后输出q1,如果不想用
'''
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        q1 = Queue()  # 一个承接拼接的值
        q2 = Queue()  # 一个承接拼接的结果
        q1.put("")
        dic_ = {"1": "", "2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv",
                "9": "wxyz"}
        for i in digits:
            str_ = dic_[i]
            print(str_)
            if i=="1":
                continue
            while not q1.empty():
                a = q1.get()
                for _ in str_:
                    print(a + _)
                    q2.put(a + _)
            while not q2.empty():
                q1.put(q2.get())
        l = []
        while not q1.empty():
            l.append(q1.get())
        return l
    def letterCombinations1(self, digits: str) -> List[str]:
        if not digits:
            return ""
        q1 = Queue()  # 一个承接拼接的值
        q2 = Queue()  # 一个承接拼接的结果
        dic_ = {"1": "", "2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv",
                "9": "wxyz"}
        q1.put("")
        for i in digits:
            str_put=dic_[i]
            if str_put=="":
                continue
            while not q1.empty():
                c_char = q1.get()
                for char in str_put:
                    #c_char += char
                    #print(c_char)
                    #print(c_char+char)
                    q2.put(c_char+char)
            while not q2.empty():
                q1.put(q2.get())
        l=[]
        while not q1.empty():
            l.append(q1.get())
        return l

if __name__=="__main__":
    solution = Solution()
    print(solution.letterCombinations1('123'))
    print(solution.letterCombinations1(''))
    print(solution.letterCombinations1('456'))
