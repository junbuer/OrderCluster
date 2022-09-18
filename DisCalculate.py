'''
距离计算模块：欧式距离，曼哈顿距离，经纬度距离
'''
from scipy.spatial.distance import cdist
from numpy import  radians, sin, cos, arcsin, sqrt
import numpy as np
#计算经纬度距离
def H_dis(lon1, lat1, lon2, lat2):
    # 将十进制转为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    aa = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * arcsin(sqrt(aa))
    r = 6371  # 地球半径，千米
    return c * r * 1000

# 计算欧式距离(欧式距离矩阵)
def E_dis(p1, p2):
    return cdist(p1, p2)




