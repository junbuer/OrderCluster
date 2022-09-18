'''
层次聚类，初始聚类返回中心即可
'''
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
def hierarchical(coord, k):
    '''
    :param coord: 节点坐标
    :param k: 聚类数量
    :return: 每个类的聚类中心
    '''
    z = linkage(coord, method='centroid') # 中心点距离
    f = fcluster(z, t=k, criterion='maxclust') # 聚类结果提取t为最大分类数
    # 分类结果
    clusters = [[] for i in range(k)]
    for i in range(len(f)):
        clusters[f[i] - 1].append(i)
    # 聚类中心
    centers = []
    for i in range(k):
        cnt_coord = np.array([coord[j] for j in clusters[i]])
        centers.append(np.average(cnt_coord, axis=0))
    return np.array(centers)




