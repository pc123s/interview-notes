'''
求数组的逆序数
题目：在一个排列中，如果一对数的前后位置与大小顺序相反，即前面的数大于后面的数，那么它们就称为一个逆序。一个排列中逆序的总数就称为这个排列的逆序数。
现在，给你一个N个元素的序列，请你判断出它的逆序数是多少。

比如 1 3 2 的逆序数就是1。
'''

'''
方法1 暴力解法
直接遍历
'''

def inversions_brute(l: list) -> int:
    n=len(l)
    count=0
    for i in range(n-1):
        for j in range(i+1,n):
            if l[i]>l[j]:
                count+=1
    return count

'''
方法2 树状数组
大家可以看这个教程
https://zhuanlan.zhihu.com/p/93795692
https://zhuanlan.zhihu.com/p/166127615
这个就是用来求逆序数，设一个数组为

我们需要前n个节点的和，这时我们需要一个额外空间的数组去进行维护

nums=  [0 , 2 , 1 , 1 , 3 , 2 , 3 , 4 , 5 , 6, 7 , 8 , 9 ]
bits=  [0,  1 , 2,  1 , 4 , 1 , 2 , 1 , 8,  1, 2,  1 , 4] x&-x的值,这个bite代表前n个数的和 lobit()代替
index= [0,  1 , 2,  3 , 4 , 5 , 6 , 7 , 8,  9, 10, 11 ,12]     
biTree=[0,  2 , 3,  1 , 7 , 2 , 5 , 4 , 21, 6, 13, 8 , 30] bitree[i]的值前bite[i]代表的前n个数的和

我们只需要维护这两个数组nums和bitre两个数组
这时我们的数组是树状的，当我们原数组变化时可以在任意logn的时间段更新前n个值的和

我们先看看biTree是怎么产生的。
我们先初始化一个16*[0]的数组
[0 ,0 , 0 , 0, 0, 0, 0, 0, 0, 0, ...0]
插入2 index1
2=tree[1]+2
[0 ,2,0,0,...0]
向上爬坡
2=1+bit(1)
tree[2]=tree[2]+2
[0,2,2,0,...0]
4=2+bit(2)
tree[4]=tree[4]+2
[0,2,2,0,2...0]
8=4+bit(4)
[0,2,2,0,2,0,0,0,2,...0]
依次类推
[0,2,2,0,2,0,0,0,2,...0]
其实就是当数组中一个元素发生变化时，利用bite计算附属节点来联动发生变化。

插入1 index 2 bits值为2 继续向上迭代
2
4=2+bit(2)
8=4+bit(4)
16=8+bit(8) >12 都要加1
[0,2,3,0,4,0,0,0,4,0,0,0,0]

2、树的更新
同样树的更新我们也是以bits相加算的，还是之前那个例子

nums=  [0, 3 , 1 , 1 , 3 , 2 , 3 , 4 , 5 , 6, 7 , 8 , 9 ]
bits=  [0, 1 , 2,  1 , 4 , 1 , 2 , 1 , 8,  1, 2,  1 , 4] x&-x的值,这个bite代表前n个数的和 lobit()代替
index= [0, 1 , 2,  3 , 4 , 5 , 6 , 7 , 8,  9, 10, 11 ,12]     
biTree=[0, 2 , 3,  1 , 7 , 2 , 5 , 4 , 21, 6, 13, 8 , 30] bitree[i]的值前bite[i]代表的前n个数的和

我们在进行模型的更新时，也同样采用树的方式进行相应的更新，比如
nums[1]=2  我们将2更新为3的时候，biTree需要更新
nums[1]=3 bits[1]=1 biTree[1]=3
向上迭代
1+1=2 biTree[2]=4
2+2(index+bits[2])4 biTree[4]=8

依次类推

这个例子是树状数组快速求解当前值的前n项和的方法

例2：用树状数组求逆序对
按道理5应该在第5个位置上，4在4的位置上，
我们可以想象成
一组数列nums
[5,4,10,2,3]
ranks  原先的数是第几大的元素
[4,3,5,1,2]
依次执行 query(ranks[i])  update(ranks[i],1)

对于5来说，原始位置在1，实际的位置在4，我们顺序
query(index) 代表index前面有几个数
query(4) 代表看比第四个元素小的数有几个。 query(ranks[0]=4)=0 代表nums[0]=5,数组中比5小的元素有0个
query(3)=0 代表在插入index3时，前面比index小的数是0个。因为你比3小，一定会提前被插入 


'''

class FenwickTreePc:
    def __init__(self,n,arr):
        self.n=n
        self.tree=[0]*(len(arr)+1)
        self.arr=arr

    def updateTree(self,index,value):
        '''
        下标为index的value值在树状数组进行更新
        :param index:
        直接在self.tree进行相应的更新
        '''
        while index<=self.n:
            self.tree[index]+=value
            index+=index&(-index)

    def query(self,index):
        '''
        求 树状数组0-index之间的所有数的和
        :param index:
        :param value:
        :return:
        '''
        res=0
        while index>0:
            res+=self.tree[index]
            index-=index&(-index)
        return res

nums = [2 , 1 , 1 , 3 , 2 , 3 , 4 , 5 , 6, 7 , 8 , 9 ]
tree=FenwickTreePc(len(nums),nums)
for index,value in enumerate(nums):
    tree.updateTree(index+1,value)
    print(tree.tree)

#print(tree.query(12))

# exit()
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, index, delta):
        while index <= self.n:
            self.tree[index] += delta
            index += index & -index
    def query(self, index):
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= index & -index
        return result
    def betie(self,index):
        return index&-index

def count_inversions(nums):
    n = len(nums)
    sorted_nums = sorted(enumerate(nums), key=lambda x: x[1])
    # print("排序后的数组")
    # print(sorted_nums)
    ranks = [0] * n
    for i, (index, _) in enumerate(sorted_nums):
        # index 以前的位置，i第几大的数
        #print(i)
        ranks[index] = i + 1
    #ranks代表当前数字在原先数组的顺序
    # # ranks 代表位置排序
    # print("数组的原先的rank位置")
    # print(ranks)
    fenwick_tree = FenwickTree(n)
    inversions = 0

    # for i in range(n - 1, -1, -1):
    #     print(fenwick_tree.tree)
    #     print(fenwick_tree.query(ranks[i] - 1))
    #     inversions += fenwick_tree.query(ranks[i] - 1)
    #     fenwick_tree.update(ranks[i], 1)

    print("ranks",ranks)
    for i in range(n):
        b=fenwick_tree.query(ranks[i])
        u=i-b
        print(i,nums[i],b,u)

        inversions+=u
        fenwick_tree.update(ranks[i],1)
    return inversions



if __name__=="__main__":
    print("暴力解法#################")
    test_l=[[1,3,2],[3,4,7],[6,5,4,3,2,1],[1,4,7,8,5,3]]
    for l in test_l:
        count=inversions_brute(l)
        print(count)


    # print(bit)
    #print("##############树状数组##############")
    # 示例
    # 示例
    print("##############树状数组#########")
    nums=[2,1,1,3,2,3,4,5,6,7,8,9]

    n=len(nums)
    nums = [2,10,5,3,1]
    print(nums)
    inversions = count_inversions(nums)
    print("逆序对的数量：", inversions)

    nums = [3, 1, 5, 9, 10]
    print(nums)
    inversions = count_inversions(nums)
    print("逆序对的数量：", inversions)
    # tree=FenwickTree(n)
    # for i in range(0,n+1):
    #     print("index",i)
    #     print("bites",tree.betie(i))
    # tree.update1()