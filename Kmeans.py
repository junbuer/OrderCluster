'''
带有容量限制的keanms算法
'''
import copy
from DisCalculate import E_dis
import numpy as np

def kmeans(C_size, k, coord, centers, end=0):
    '''
    :param C_size: 容量限制
    :param k: 类数
    :param coord: 节点坐标
    :param centers: 中心点坐标
    :param end: 终止条件
    :return:
    '''
    # 订单数量
    n = len(coord)
    # 上一次的中心点
    old_centers = np.zeros(centers.shape)
    # 计算新旧中心点距离
    iteration_flag = np.linalg.norm(old_centers - centers, axis=1) # 1为横向
    # 聚类请求
    while np.max(iteration_flag) > end:
        clusters = [[] for i in range(k)] # 聚类结果保存
        dis = E_dis(coord, centers) # 节点与中心点距离计算[n * k]
        # label = np.argmin(dis, axis=1)
        for i in range(n):
            # clusters[label[i]].append(i)
            # 对节点到中心点距离升序排序
            c = dict(zip(range(k), dis[i]))
            c = sorted(c.items(), key=lambda x:x[1])
            # 节点归类，如果最近的类已满，则分到次近的类
            ind = 0  # 最近类
            while len(clusters[c[ind][0]]) >= C_size:
                ind += 1
            clusters[c[ind][0]].append(i)
        # 保存中心点
        old_centers = copy.deepcopy(centers)
        # 更新中心点
        for i in range(k):
            cnt_coord = np.array([coord[j] for j in clusters[i]])
            centers[i] = np.average(cnt_coord, axis=0)
        # 计算新旧中心点距离
        iteration_flag = np.linalg.norm(old_centers - centers, axis=1)
    return clusters







