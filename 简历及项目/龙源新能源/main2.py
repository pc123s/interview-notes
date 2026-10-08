'''
考试题目2

["2023/1/1 0:05", "2023/1/1 0:10", "2023/1/1 0:15", "2023/1/1 0:25"]

["2023/1/1 0:05", "2023/1/1 0:10", "2023/1/1 0:15","2023/1/1 0:20", "2023/1/1 0:25"]
     1                  1                   1             0                   1

'''
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from scipy import interpolate
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import mean_squared_error
from model import *
import torch.nn.functional as F
def linerinsertNull(df,col:str):
    '''
    缺失值填充函数
    :param df:
    :param col:
    :return:
    '''
    fill_records=list(df[col])
    fill_records1 = [np.nan if x is None else x for x in fill_records]
    # 创建一个时间序列索引
    index = np.arange(len(fill_records1))

    # 找到非缺失值的索引和对应的值
    known_indexes = index[~np.isnan(fill_records1)]
    known_values = np.array(fill_records1)[~np.isnan(fill_records1)]

    # 使用线性插值来填充缺失值
    interpolated_func = interpolate.interp1d(known_indexes, known_values, kind='linear')
    interpolated_values = interpolated_func(index)
    df[col]=interpolated_values
    return df
def calculate_time_difference(dtime_list,true_val,diff_gap):
        time_diff_list = []
        result=[]
        new_true_val=[]
        for i in range(len(dtime_list) - 1):
            c_val=true_val[i]
            time1 = datetime.strptime(dtime_list[i], "%Y/%m/%d %H:%M")
            time2 = datetime.strptime(dtime_list[i + 1], "%Y/%m/%d %H:%M")
            diff = (time2 - time1).total_seconds() / 60  # 差值转换为分钟
            if diff > diff_gap:
                #time_diff_list.append(dtime_list[i]+dtime_list[i+1])
                num_segments = int(diff / diff_gap)
                segment_duration = timedelta(minutes=diff_gap)
                #result.append(dtime_list[i])
                for j in range(num_segments):
                    segment_start = time1 + j * segment_duration
                    segment_start_1=segment_start.strftime("%Y/%m/%d %H:%M")
                    if segment_start_1==dtime_list[i]:
                        new_true_val.append(c_val)
                    else:
                        new_true_val.append(None)
                    time_diff_list.append(diff)
                    result.append(segment_start_1)

            else:
                result.append(time1.strftime("%Y/%m/%d %H:%M"))
                new_true_val.append(c_val)
                time_diff_list.append(diff)

        result.append(dtime_list[-1])
        #fill_records.append(1)
        new_true_val.append(true_val[-1])
        time_diff_list.append(5)

        #print(len(result))
        #print(len(new_true_val))
        #print(len(time_diff_list))
        return result,new_true_val,time_diff_list

def hasRightTimeSeq(df,time_col,seq_len):
    df[time_col] = pd.to_datetime(df[time_col])
    #print(Y_test_data)
    #exit()
    # 提取日期并按日期进行分组
    grouped = df.groupby(df[time_col].dt.date).size()
    #print(grouped)
    is_every_day_complete = all(grouped == seq_len)
    print("每天是否有288个数据点:", is_every_day_complete)
    # 找到不是288个数据点的日期
    incomplete_days = grouped[grouped != seq_len]
    print(f"不是每天有{seq_len}个数据点的日期：")
    for date, count in incomplete_days.items():
        print(f"日期：{date}，数据点数量：{count}")
def calc_precison(y,y_pred):
    # 计算 y 和 y_pred 之间的平方差
    y=y.cpu()
    y_pred= y_pred.cpu()

    squared_diff = (y - y_pred) ** 2
    n = 96
    gap = 99000
    # 计算平方和
    squared_sum = torch.sum(squared_diff)
    #print(squared_sum)
    sqrt_sum = np.sqrt(squared_sum.detach().numpy())
    res = sqrt_sum / (gap * np.sqrt(n))
    return 1-res
if True:
    def fill_series_y():
        # 真实值时间填充
        data=pd.read_csv("./data/笔试题2/真实值.csv")
        new_row_data = {'dtime': '2023/1/1 0:00', 'instant': 2236.4521}
        new_row_df = pd.DataFrame([new_row_data])
        data = pd.concat([new_row_df, data], ignore_index=True)

        n=data.shape[0]
        time_l=data["dtime"]
        instant=data["instant"]
        time_l_1=[]
        for date_string in time_l:
            date_obj = datetime.strptime(date_string, "%Y/%m/%d %H:%M")
            #time_l_1.append(date_obj)
            time_l_1.append(date_obj.strftime("%Y/%m/%d %H:%M"))
        #print(time_l_1[:5])
        #exit()

        instant=list(instant)
        result,new_true_val,diff=calculate_time_difference(time_l_1,instant,5)
        true_val=[]
        #for i in range
        data=pd.DataFrame({"time":result,"value":new_true_val,"diff":diff})
        data=linerinsertNull(data,"value")
        print("y_data缺失值填充结束")
        return data

    #data.to_csv("./diff1.csv")
    #print(res)


if True:
    def fill_series_x():
        # 对输入值进行时间填充
        input_data=pd.read_csv("./data/笔试题2/输入值.csv")

        column_l=list(input_data.columns)
        #print(column_l)
        column_l.remove("dtime")
        #print(column_l)
        ## 进行时间的填充
        time_l=list(input_data["dtime"])
        time_add_l=[]
        new_arr=[]
        for col in column_l:
            col_val=list(input_data[col])
            time_add_l,new_val,_=calculate_time_difference(time_l,col_val,60)
            new_arr.append(new_val)
        column_l.insert(0,"dtime")
        new_arr.insert(0,time_add_l)
        new_input_data=pd.DataFrame(dict(zip(column_l, new_arr)))
        #print(new_input_data)

        ##对数据进行缺失值的填充
        column_l.remove("dtime")
        for col in column_l:
            new_input_data=linerinsertNull(new_input_data,col)
        print("X_data缺失值填充结束")
        return new_input_data
    #new_input_data.to_csv("input_data_new.csv")

if True:
    def fill_na_and_split_data(data_x,data_y):
        # 截取一年的数据
        new_input_data = data_x.drop_duplicates(subset=['dtime'])
        train_data=new_input_data[:8760]
        test_data=new_input_data[8760:10200]
        dev_data = new_input_data[10200:10224]
        #print(dev_data)
        #exit()

        #hasRightTimeSeq(test_data,time_col="dtime",seq_len=24)
        #exit()

        #print(train_data)
        #print(test_data)
        #exit()
        # 选择训练集
        seg=24
        train_data_arr=[]
        for i in range(0,train_data.shape[0],seg):
            seq_data=train_data.iloc[i:i+seg,1:]
            #
            #list_data = [seq_data[col].tolist() for col in seq_data.columns]
            list_data=seq_data.values.tolist()
            #print(list_data)
            train_data_arr.append(list_data)
            #exit()
        test_data_arr=[]
        for i in range(0, test_data.shape[0], seg):
            seq_data = test_data.iloc[i:i + seg, 1:]
            #
            # list_data = [seq_data[col].tolist() for col in seq_data.columns]
            list_data = seq_data.values.tolist()
            # print(list_data)
            test_data_arr.append(list_data)

        dev_data_arr=[]
        #dev_data.reset_index(inplace=True)
        for i in range(0, dev_data.shape[0], seg):
            seq_data = dev_data.iloc[i:i + seg, 1:]
            #
            # list_data = [seq_data[col].tolist() for col in seq_data.columns]
            list_data = seq_data.values.tolist()
            # print(list_data)
            dev_data_arr.append(list_data)

        print(f"当前训练集共有{len(train_data_arr)}个数据,测试集有{len(test_data_arr)}个数据,验证集有{len(dev_data_arr)}个数据")

        #对Y进行截取
        Y_train_data=data_y[:105120]
        #Y_train_data['time'] = pd.to_datetime(Y_train_data['time'])
        Y_test_data = data_y[105120:122400]
        Y_dev_data = data_y[122400:122688]
        #Y_test_data['time'] = pd.to_datetime(Y_test_data['time'])
        #print(Y_dev_data)
        #exit()

        seg=96
        time_gap=3 # y是5分钟一个间隔，所以这里采用15分钟进行采样
        # Y_data_arr=[]
        arr=[] #记录96个点的list
        Y_trin_arr=[] # 记录所有seq的arr
        count=0
        for i in range(0,Y_train_data.shape[0],3):
            count += 1
            arr.append(Y_train_data["value"][i])
            if count%seg==0 and count!=0:
                Y_trin_arr.append(arr)
                arr=[]
        arr=[]
        Y_test_arr=[]
        count=0
        Y_test_data.reset_index(inplace=True)
        for i in range(0, Y_test_data.shape[0], 3):
            count += 1
            arr.append(Y_test_data["value"][i])
            if count % seg == 0 and count != 0:
                Y_test_arr.append(arr)
                arr = []
        arr=[]
        Y_dev_arr=[]
        count=0
        Y_dev_data.reset_index(inplace=True)
        for i in range(0, Y_dev_data.shape[0], 3):
            count += 1
            arr.append(Y_dev_data["value"][i])
            if count % seg == 0 and count != 0:
                Y_dev_arr.append(arr)
                arr = []
        print("数据集划分完成")
        return (train_data_arr,test_data_arr,dev_data_arr),(Y_trin_arr,Y_test_arr,Y_dev_arr)
    def train() :
        # 选用cpu还是gpu
        # 定义模型
        # 初始化模型
        flag=False
        model=trans_LSTMModel().to(device)
        # 定义损失函数和优化器
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(),lr=learning_rate)

        # 训练模型

        best_test_mse=float("inf")
        num_epochs = 20000
        for epoch in range(num_epochs):
            model.train()
            optimizer.zero_grad()
            outputs = model(X_train_tensor)
            loss = criterion(outputs, y_train_tensor)
            loss.backward()
            optimizer.step()
            if epoch%500==0:
                # 测试模型
                model.eval()
                with torch.no_grad():
                    y_pred_tensor = model(X_test_tensor)
                    rmse = np.sqrt(mean_squared_error(y_test_tensor.cpu().numpy(), y_pred_tensor.cpu().numpy()))
                    print("测试集上的均方根误差（RMSE）：", rmse)
                    if rmse<best_test_mse:
                        last_improve=epoch
                        best_test_mse=rmse
                        print("测试集上的最佳的均方均方根误差（RMSE）：", rmse)
                        torch.save(model.state_dict(),"./model_2/LSTM_transformer_test.ckpt")
                    if epoch-last_improve>require_imporve:
                        print("no optimization for a long time,auto-stoping")
                        flag=True
                        break

                print(f"Epoch [{epoch + 1}/{num_epochs}], train_Loss: {loss.item()},best_mse:{best_test_mse}")
                if flag:
                    break
    def test():
        model = trans_LSTMModel().to(device)
        model.load_state_dict(torch.load("./model_2/LSTM_transformer.ckpt"))
        model.eval()
        predict_dev = model(X_dev_tensor)
        precison = calc_precison(predict_dev, y_dev_tensor)
        print(precison)
if __name__=="__main__":

    y_data=fill_series_y()
    x_data=fill_series_x()
    (train_data_arr,test_data_arr,dev_data_arr),(Y_train_arr,Y_test_arr,Y_dev_arr)=fill_na_and_split_data(x_data,y_data)
    # 数据处理完成后开始建模
    X_train=np.array(train_data_arr)
    X_test=np.array(test_data_arr)
    X_dev=np.array(dev_data_arr)
    Y_train=np.array(Y_train_arr)
    Y_test = np.array(Y_test_arr)
    Y_dev=np.array(Y_dev_arr)


    #exit()
    # print(X_train.shape)
    # print(X_test.shape)
    # print(X_dev.shape)
    # print(Y_train.shape)
    # print(Y_test.shape)
    # print(Y_dev.shape)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32).to(device)
    y_train_tensor = torch.tensor(Y_train, dtype=torch.float32).to(device)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32).to(device)
    y_test_tensor = torch.tensor(Y_test, dtype=torch.float32).to(device)
    X_dev_tensor = torch.tensor(X_dev, dtype=torch.float32).to(device)
    y_dev_tensor = torch.tensor(Y_dev, dtype=torch.float32).to(device)


    if False: # 是否进行训练,训练好则不需要训练了
        train()
    if True:
        test()


    # 加载模型进行验证
