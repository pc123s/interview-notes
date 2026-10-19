'''
有一列字符串，对字符串中的异位字符串进行获取和排列
示例 1:

输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
输出: [["bat"],["nat","tan"],["ate","eat","tea"]]
示例 2:

输入: strs = [""]
输出: [[""]]
示例 3:

输入: strs = ["a"]
输出: [["a"]]

异字母那么他们的字符串在排序以后一定是一样的
比如 eat和ate 排序后都是eat
'''
from typing import *
from collections import defaultdict
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        mp=defaultdict(list)
        print(mp)
        for str in strs:
            str_="".join(sorted(str))
            mp[str_].append(str)
        print(mp)
        return list(mp.values())
    def groupAnagrams1(self,strs:List[str]):
        mp=defaultdict(list)
        for str in strs:
            str_="".join(sorted(str))
            mp[str_].append(str)
        str_lis=[value for key,value in mp.items()]
        return str_lis

if __name__=="__main__":
    solution=Solution()
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    str_lis=solution.groupAnagrams(strs)
    print(str_lis)