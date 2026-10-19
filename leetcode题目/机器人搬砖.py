'''
机器人只搬砖，一共有N堆砖存放在N个不同的仓库中，第i堆专中有bricks[i]块砖头，要求在8小时内搬完。
机器人每小时能搬砖的数量取决于有多少能量格，机器人一个小时中只能在一个仓库搬砖，机器人的能量格每小时补充一次且能量格只在这一个小时有效，为使得机器人损耗最小化尽量减小每次补充的能量格数
 为了保障在8小时内能完成搬砖任务，
请计算每小时给机器人充能的最小能量格数。
1、无需考虑机器人补充能量格的耗时
2、无需考虑机器人搬砖的耗时
3、机器人每小时补充能量格只在这一个小时中有效,

输入描述
第一行为一行数字 空格分割
输出描述
机器人每小时最少需要冲的能量格 ，若无法完成任务 输出-1

用例输入
30 12 25 8 19
输出
15

用例输入
10 12 25 8 19 864 17 19 20 30
输出：
-1

参考：https://csproject.icu/index.php/archives/42/
'''
import math

# 输入获取
bricks =[30,12,25,8,19]


def is_possible(energy, limit):
    """
    :param energy: 每小时可以使用的能量块数量（搬一块砖消耗一块能量）
    :param limit: 限制几小时内干完
    :return: 是否可以在limit小时内搬完所有bricks
    """
    hours_spent = 0  # 已花费的小时数

    brick_index = 0
    while brick_index < len(bricks):
        hours_spent += math.ceil(bricks[brick_index] / energy)

        # 如果搬砖过程中发现，花费时间已经超过限制，则直接返回false
        if hours_spent > limit:
            return False

        brick_index += 1

    return True


# 算法入口
def get_result():
    # 机器人每小时只能在一个仓库干活，因此给定8小时，最多只能搬完8个仓库，如果仓库数量超过8，那么肯定干不完
    if len(bricks) > 8:
        return -1

    # 每小时最多需要的能量块
    max_energy = max(bricks)

    # 如果有8个仓库，那么只能1个小时干1个仓库，且机器人每小时需要能量至少是max(bricks)，这样才能保证1个小时内把最多砖块的那个仓库搬完
    if len(bricks) == 8:
        return max_energy

    # 如果仓库数少于8个，那么此时每小时能量max(bricks)必然能在8小时内搬完所有仓库，但不是最优解
    ans = max_energy

    # 每小时最少需要的能量块
    min_energy = 1

    # 二分法
    while min_energy <= max_energy:
        # 取中间值
        mid = (min_energy + max_energy) // 2

        if is_possible(mid, 8):
            # 如果每小时充mid格能量，就能在8小时内，搬完所有砖头，则mid就是一个可能解
            ans = mid
            # 但mid不一定是最优解，因此继续尝试更小的能量块
            max_energy = mid - 1
        else:
            # 如果每小时充mid能量块，无法在8小时能完成工作，则说明每天能量块充少了，下次应该尝试充更多能量块
            min_energy = mid + 1

    return ans


# 算法调用
print(get_result())
