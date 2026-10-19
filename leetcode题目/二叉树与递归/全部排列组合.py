'''
自己项目中遇到的问题，这里记录下
加入有个list,list中可能嵌套list，其中为数字，如何找出list中所有数字的排列组合
例如 test_list=[[1,2,3],[1],[2,3,4],[5,6,7]]
找出这个test_list的所有排列组合
'''
# 方法1：采用itertools，product方法
import itertools
test_list=[[1,2,3],[1],[2,3,4],[5,6,7]]
combinations = list(itertools.product(*test_list))
print(combinations)

# 方法2：采用递归和回溯算法
def get_combinations(test_list, index, curr_comb, all_comb):
    '''
    :param test_list:表示要生成排列组合的列表
    :param index:表示当前处理的子列表的索引
    :param curr_comb:表示当前已经生成的排列组合
    :param all_comb:表示所有已经生成的排列组合
    :return:
    在上面的代码中，我们定义了一个名为get_combinations的递归函数，用于生成给定列表的所有排列组合。
    在函数的主体中，首先判断如果当前处理的子列表的索引已经到达列表的末尾，即所有子列表都已经处理完毕，
    就将当前已经生成的排列组合添加到all_comb列表中，并返回。
    如果还有子列表需要处理，则遍历当前子列表中的所有元素，并将每个元素添加到当前排列组合中，然后递归调用get_combinations函数处理下一个子列表。
    在递归返回后，我们需要将已经添加的元素从当前排列组合中弹出，以便处理其他可能的排列组合。
    '''
    if index == len(test_list):
        all_comb.append(curr_comb[:])
        return
    for elem in test_list[index]:
        curr_comb.append(elem)
        print(curr_comb)
        get_combinations(test_list, index+1, curr_comb, all_comb)
        curr_comb.pop()



if __name__=="__main__":
    if True:
        test_list = [[1,2,3],[1],[2,3,4],[5,6,7]]
        all_combinations = []
        get_combinations(test_list, 0, [], all_combinations)
        print(all_combinations)
    if True:
        test_list=[["a","b","c"],["a","b","c"],["a","b","c"]]
        all_combinations = []
        get_combinations(test_list, 0, [], all_combinations)

        print(all_combinations)
    if True:
       test_list = [["(",")"], ["(",")"], ["(",")"],["(",")"], ["(",")"], ["(",")"]]
       all_combinations = []
       get_combinations(test_list, 0, [], all_combinations)

       print(all_combinations)