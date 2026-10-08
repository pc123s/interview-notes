'''
数据的处理接口
'''
import pandas as pd
import xgboost as xgb
from sklearn.metrics import r2_score, mean_squared_error
data=pd.read_excel("./data/笔试题1/笔试题1数据.xlsx")
print(data.head(5))
x=data["真实值"]
y=data["模拟值"]
train_x=x[:3072]
train_y=y[:3072]
eval_x=x[3216:]
eval_y=x[3216:]
train_x=train_x.to_frame()
train_y=train_y.to_frame()
print(train_x)
print(train_y)
print(train_x.shape)
print(train_y.shape)
# 模型训练与网格搜索
if False:
    mse_value=9999
    max_depth=[3, 5, 6, 7, 9, 12, 15, 17, 25] #选择3最优
    subsample=[0.25,0.5,0.75,1]
    learning_rate=[0.01, 0.015, 0.025, 0.05, 0.1]
    for i in range(len(max_depth)):
        for j in range(len(subsample)):
            for z in range(len(learning_rate)):
                learning_rate_value=learning_rate[z]
                max_depth_value=max_depth[i]
                subsample_value=subsample[j]
                reg_mod = xgb.XGBRegressor(
                    n_estimators=2000,
                    learning_rate=learning_rate_value,
                    subsample=subsample_value,
                    colsample_bytree=1,
                    max_depth=max_depth_value,
                    gamma=0.05,
                    reg_alpha=0.1
                )
                # train_x=list(train_x)
                # train_y=list(train_y)
                reg_mod.fit(train_x,train_y,verbose=True)
                #exit()
                #print(eval_x)
                y_pred = reg_mod.predict(eval_x)
                #print(y_pred)

                r2 = r2_score(eval_y, y_pred)
                #print('r2_score:{0}'.format(r2))
                mse = mean_squared_error(eval_y, y_pred)
                #print('mse:{0}'.format(mse))
                if mse<mse_value:
                    print('r2_score:{0}'.format(r2))
                    print('mse:{0}'.format(mse))
                    print(f"max_depth:{max_depth_value},subsample:{subsample_value},learning_rate:{learning_rate_value}")
                    mse_value=mse
# max_depth:3,subsample:1,learning_rate:0.025
if True:
    reg_mod = xgb.XGBRegressor(
        n_estimators=10000,
        learning_rate=0.025,
        subsample=1,
        colsample_bytree=1,
        max_depth=3,
        gamma=0.05,
        reg_alpha=0.1
    )
    # train_x=list(train_x)
    # train_y=list(train_y)
    reg_mod.fit(train_x, train_y, verbose=True)
    # exit()
    # print(eval_x)
    y_pred = reg_mod.predict(eval_x)
    print(y_pred)

    r2 = r2_score(eval_y, y_pred)
    mse = mean_squared_error(eval_y, y_pred)
    print('mse:{0}'.format(mse))