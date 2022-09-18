'''
订单分割
'''
from DisCalculate import H_dis
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
path = r'G:\taxi_data\出租车数据\od\2019114_od_整理.csv'
data = pd.read_csv(path)
s = 7 # 开始时间
e = 9 # 结束时间

# 早高峰时段订单按分钟分割
def divide(data):
    for i in range(s, e):
        for j in range(60):
            save = r"G:\taxi_share\OrderByMin\2019114\2019114_{}_{}.csv".format(i, j) # 保存路径
            d = data[(data['Hours']==i) & (data['Mins'] == j)]
            # d.to_csv(save, index=False, encoding='utf8')

# 每分钟请求的距离矩阵
def dis_cal(path, save):
    d = pd.read_csv(path)
    n = len(d) # 请求数

    # 拼接上下车点坐标
    lon = np.array(list(d['SLng']) + list(d['ELng']))
    lat = np.array(list(d['SLat']) + list(d['ELat']))
    # 距离矩阵
    dis = np.zeros((2 * n, 2 * n))
    for i in range(n):
        dis[i] =  H_dis(lon[i], lat[i], lon, lat)
    # np.save(save, dis)
    print(len(lon))
    return dis

if __name__ == '__main__':
    # divide(data)

    for i in range(s, e):
        for j in range(60):
            path = r"G:\taxi_share\OrderByMin\2019114\2019114_{}_{}.csv".format(i, j)  # 读取路径
            save = r"G:\taxi_share\OrderByMin\2019114\2019114_{}_{}.npy".format(i, j) # 读取路径
            dis = dis_cal(path, save)
    print(dis)

    # dis = np.load(r"G:\taxi_share\OrderByMin\2019114\2019114_7_0.npy")
    # print(dis.shape)


