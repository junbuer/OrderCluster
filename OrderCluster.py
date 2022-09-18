'''
基于共享指数聚类订单
'''
import pandas as pd
import numpy as np
from Kmeans import kmeans
from Hierarchical import hierarchical
from DisCalculate import E_dis
import matplotlib.pyplot as plt
import matplotlib as mpl
from  copy import deepcopy
# 画图字体设置
plt.rcParams['font.sans-serif'] = ['Simhei']
plt.rcParams['axes.unicode_minus'] = False
class order_cluster():
    def __init__(self, path='', save='', C_size=0):
        '''
        :param path: 数据读取路径
        :param save: 数据保存路径
        :param C_size: 大小限制
        '''
        # 数据读取
        self.order = pd.read_csv(path + '.csv') # 乘客请求
        self.dis = np.load(path + '.npy') # 距离矩阵
        self.n = len(self.order) # 订单数量
        self.C_size = C_size # 聚类大小限制
        self.k = int(np.ceil(self.n / self.C_size)) # 类数
        # 上下车点坐标
        self.Lng = np.array(list(self.order['SLng']) + list(self.order['ELng']))
        self.Lat = np.array(list(self.order['SLat']) + list(self.order['ELat']))
        # 保存
        self.save = save
    def clustering(self):
        # 共享指数计算
        shared_index = self.shared_cal()
        # 多维标度法获得相对位置
        self.mds(shared_index)
        # 层次聚类(得到聚类中心)
        centers = hierarchical(self.shared_coord, self.k)
        # keams聚类(最终结果)
        self.clusters = kmeans(self.C_size, self.k, self.shared_coord, centers)
        # 保存聚类结果
        clusters = deepcopy(self.clusters)
        data = pd.DataFrame(columns=range(self.k))
        for i in range(self.k):
            while len(clusters[i]) < self.C_size:
                clusters[i].append(None)
            data[i] = clusters[i]
        data.to_csv(self.save + '.csv', index=False)

    # 共享指数矩阵计算
    def shared_cal(self):
        shared_index = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if j != i:
                    # 合乘 i,j,i+n,j+n; i,j,j+n,i+n; j,i,i+n,j+n; j,i,j+n,i+n
                    share = self.dis[i][j]  + self.dis[i + self.n][j + self.n] \
                            + min(self.dis[j][i + self.n] , self.dis[j][j + self.n],
                                  self.dis[i][i + self.n] , self.dis[i][j + self.n]) # i,j同方向是可能小于单独服务时间
                    # 非合乘顺序行程 i,i+n,j,j+n; j,j+n,i,i+n
                    seq = self.dis[i][i + self.n] + self.dis[j][j + self.n] \
                          + min(self.dis[i + self.n][j], self.dis[j + self.n][i])
                    # 分别服务
                    dire =  self.dis[i][i + self.n] + self.dis[j][j + self.n]
                    # 合乘指数(越小越好，小说明绕路少)
                    shared_index[i ,j] = min(share, seq) - dire

        # 相似度标准化
        min_, max_= np.min(shared_index), np.max(shared_index)
        shared_index = (shared_index - min_)/(max_ - min_)
        for i in range(self.n):
            shared_index[i, i] = 0
        # self.shared_index = sshared_index
        return shared_index

    # 多维标度法
    def mds(self, shared_index):
        shared_index_ = shared_index ** 2
        H = np.eye(self.n) - 1 / self.n
        T = -0.5 * np.dot(np.dot(H, shared_index), H)
        eigVal, eigVec = np.linalg.eig(T)
        # 订单相似度坐标
        self.shared_coord = np.dot(eigVec[:, :2], np.diag(np.sqrt(eigVal[:2])))
        self.shared_x = self.shared_coord[:, 0]# 共享x坐标
        self.shared_y = self.shared_coord[:, 1] # 共享y坐标

    # 订单可视化
    def order_plot(self, save):
        '''
        :param save: 存储路
        :return:
        '''
        plt.figure(figsize=(12, 12), dpi=200)
        # 连线
        for i in range(self.n):
            plt.plot([self.Lng[i], self.Lng[i + self.n]], [self.Lat[i], self.Lat[i + self.n]], color='k', zorder=1)
        # 起点
        plt.scatter(self.Lng[0:self.n], self.Lat[0:self.n], marker='o', color='g',s=35, label='起点', zorder=2)
        # 终点
        plt.scatter(self.Lng[self.n: ], self.Lat[self.n: ], marker='^', color='r',s=35, label='终点', zorder=2)

        # 坐标轴
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.legend(loc='best', fontsize=25)
        plt.savefig(save + '订单可视化.png')
        plt.show()

    # 多维标度结果可视化
    def mds_plot(self, save):
        '''
        :param save: 存储路径
        :return:
        '''
        plt.figure(figsize=(12, 12), dpi=200)
        # 起点
        plt.scatter(self.shared_x, self.shared_y, s=35)
        # 坐标轴
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.savefig(save + '多维标度可视化.png')
        plt.show()

    # 聚类结果显示
    def clusters_plot(self, save, c):
        '''
        :param save: 存储路径
        :param c: 类序号
        :return:
        '''
        # 聚类结果
        plt.figure(figsize=(12, 12), dpi=200)
        # cmap = plt.cm.get_cmap('Paired') # 色带设置
        for i in range(self.k):
            x, y = [self.Lng[j] for j in self.clusters[i]], [self.Lat[j] for j in self.clusters[i]]
            plt.scatter(x, y, s=35)
        # 坐标轴
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.savefig(save + '所有聚类结果.png')
        plt.show()

        # 某一个簇
        plt.figure(figsize=(12, 12), dpi=200)
        # od坐标
        cluster = self.clusters[c]
        x_o, y_o = [self.Lng[i] for i in cluster], [self.Lat[i] for i in cluster]
        x_d, y_d = [self.Lng[i + self.n] for i in cluster], [self.Lat[i + self.n] for i in cluster]
        # 连线
        for i in range(len(x_o)):
            plt.plot([x_o[i], x_d[i]], [y_o[i], y_d[i]], color='k', zorder=1)
        # 起点
        plt.scatter(x_o, y_o, marker='o', color='g', s=35, label='起点', zorder=2)
        # 终点
        plt.scatter(x_d, y_d, marker='^', color='r', s=35, label='终点', zorder=2)

        # 坐标轴
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.legend(loc='best', fontsize=25)
        plt.savefig(save + '单一类结果.png')
        plt.show()

if __name__=='__main__':
    s = 7  # 开始时间
    e = 8  # 结束时间
    c_size = 30  # 聚类大小
    for i in range(s, e):
        for j in range(1):
            path = r"G:\taxi_share\OrderByMin\2019114\2019114_{}_{}".format(i, j)  # 读取路径
            save1 = r"G:\taxi_share\OrderByMin\2019114\2019114_cluster_{}_{}".format(i, j)
            save2 = r"C:\Users\buer\Desktop\论文初稿\图\聚类\2019114_cluster_{}_{}".format(i, j)
            oc = order_cluster(path, save1, c_size)
            oc.clustering()
            # 结果可视化
            oc.order_plot(save2)
            oc.mds_plot(save2)
            oc.clusters_plot(save2, 1)









