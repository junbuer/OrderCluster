# OrderCluster
Taxi orders cluster based on shared index 

基于共享指数的出租车订单聚类

## 订单按分钟分割和距离矩阵计算
将高峰时段（7-9点）订单按每分钟分割，计算其中涉及到的所有节点的距离矩阵并保存 

## 订单共享指数计算（订单可共享程度）
共享指数针对任意两个行程$i、j$间可共享程度建立:

$$
SharedIndex[i,j] = min(SharedDis[i, j], SeqDis[i, j]) - DireDis[i, j]
$$

其中$SharedDis$为最短合乘路程，$SeqDis为顺序服务最短路程，$DireDis$是单独服务路程等于$dis[i, i+n] + dis[j, j+n]$ 

## 多维标度法
根据订单相似度即共享指数，使用多维标度法反推坐标
 
如果距离矩阵$D=(d_{ij})$为向量$\vec{X}=(x_1,...,x_n)'$中节点间距离，即$D[i,j]=||x[i]-x[j]||_2$。则称$\vec{X}为$$D$的多维标度解。

古典解法：

+ 根据$D$构造$A=(a_{ij})=(-\frac{1}{2}d_{ij}^2)$
+ 令$B=(b_{ij})$，使得$b_{ij}=a_{ij}-\overline{a_{i.}}-\overline{a_{.j}}+\overline{a_{..}}$
+ 求$B$的特征根$\lambda_1 \geq \lambda_2 \geq ...\geq \lambda_n$。$B$不应有负特征根。则有：
    $$
    a_{1,k}=\frac{\sum_{i=1}^{k}{\lambda_i}}{\sum_{i=1}^{n}{|\lambda_i|}}
    ,a_{2,k}=\frac{\sum_{i=1}^{k}{\lambda_i}}{\sum_{i=1}^{n}{\lambda_i^2}}
    $$
+ 令$\vec{X}=(x_(1),..,x_(k))$，则$\vec{X}=x_1,..,x_n$为古典解

## 层次聚类
初始化聚类，获得聚类中心即可

## 带有容量限制的keams聚类
将层次聚类得到的中心点最为keams聚类的初始中心点。聚类订单时当最近类容量已满则加入次近类，依次类推。

## 聚类结果可视化
![聚类结果可视化](https://github.com/junbuer/OrderCluster/blob/main/ClusteringFigs/2019114_cluster_7_0%E6%89%80%E6%9C%89%E8%81%9A%E7%B1%BB%E7%BB%93%E6%9E%9C.png?raw=true)
![单一类](https://github.com/junbuer/OrderCluster/blob/main/ClusteringFigs/2019114_cluster_7_0%E5%8D%95%E4%B8%80%E7%B1%BB%E7%BB%93%E6%9E%9C.png?raw=true)

### PS：`python OrderCluster`
