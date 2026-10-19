from itertools import product
import random
# 定义超参数空间
param_grid = {
    'n_estimators': [10, 50, 100],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}
# 生成所有参数组合
def generate_param_combinations(param_grid):
    keys, values = zip(*param_grid.items())
    print(keys)
    print(values)
    #exit()
    for combination in product(*values):
        yield dict(zip(keys, combination))


param_dist = {
    'n_estimators': (10, 200),
    'max_depth': (1, 20),
    'min_samples_split': (2, 20),
    'min_samples_leaf': (1, 20),
    'bootstrap': [True, False]
}


def random_search(param_dist, n_iter=100):
    best_score = 0
    best_params = None
    for _ in range(n_iter):
        params = {
            'n_estimators': random.randint(*param_dist['n_estimators']),
            'max_depth': random.randint(*param_dist['max_depth']),
            'min_samples_split': random.randint(*param_dist['min_samples_split']),
            'min_samples_leaf': random.randint(*param_dist['min_samples_leaf']),
            'bootstrap': random.choice(param_dist['bootstrap'])
        }

        print(params)

if __name__ == '__main__':
    if False:
        iters=generate_param_combinations(param_grid)
        for iter in iters:
            print(iter)
    if True:
        random_search(param_dist)