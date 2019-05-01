# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
#计算企业之间的距离
from math import radians, cos, sin, asin, sqrt
import numba as nb

@nb.jit("float32(float32, float32, float32, float32)")
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000

def cal_k(one_indu, d, k, n, h):
    if '纬度' in one_indu.columns:
        for i in range(n-1):
            lat1 = float(one_indu.纬度[i])
            lng1 = float(one_indu.经度[i])
            for j in range(i+1, n):
                lat2 = float(one_indu.纬度[j])
                lng2 = float(one_indu.经度[j])
                dis = haversine(lng1, lat1, lng2, lat2)/1000
                k = k + np.exp(-(d - dis)**2/(2*(h**2))) + np.exp(-(d + dis)**2/(2*(h**2)))
    elif 'LNGB' in one_indu.columns:
        for i in range(n-1):
            lat1 = float(one_indu.LATB[i])
            lng1 = float(one_indu.LNGB[i])
            for j in range(i+1, n):
                lat2 = float(one_indu.LATB[j])
                lng2 = float(one_indu.LNGB[j])
                dis = haversine(lng1, lat1, lng2, lat2)/1000
                k = k + np.exp(-(d - dis)**2/(2*(h**2))) + np.exp(-(d + dis)**2/(2*(h**2)))
    k = k/(n*(n-1)*h)
    return k

year_list = ['2003', '2004','2005','2006','2007','2008','2009','2010','2011','2012','2013']
indu_list = ["14", "27", "28", "37", "40"]
path = './input/'

def cal_metrics(year, indu):
        file_path = path + year + '.xlsx'
        one_df = pd.read_excel(file_path, sheet_name=indu)
        d = np.linspace(0, 500, 1000).T
        k = np.linspace(0, 0, 1000).T
        h = 1
        n = one_df.shape[0]
        ks = cal_k(one_df, d, k, n, h)
        iter_num = 50    #随机采样100次
        o = np.zeros((1000, iter_num))
        for i in range(iter_num):
            print(year + '\t' + indu + '\t' + str(i))
            kk = np.linspace(0, 100, 1000)
            one_indu_r = one_df.sample(frac=1, replace=True).reset_index(drop=True)
            one_indu_k = cal_k(one_indu_r, d, kk, n, h)
            o[:, i] = one_indu_k
        up_95 = []
        down_95 = []
        up_99 = []
        down_99 = []
        for line in o:
            up_95.append(np.percentile(np.array(line),95))
            down_95.append(np.percentile(np.array(line),5))
            up_99.append(np.percentile(np.array(line),99))
            down_99.append(np.percentile(np.array(line),1))

        result = pd.DataFrame({'up_局部':up_95, 'down_局部':down_95, 'k':ks, 'up_全局':up_99, 'down_全局':down_99})
        save_file_name = './output/' + year + '_年行业_' + indu + '.xlsx'
        result.to_excel(save_file_name, index=False)
        #fig = plt.figure(figsize=(20, 6))
        #plt.plot(d, ks, 'r-', )
        #plt.plot(d, result['up_局部'].values, 'b--')  #蓝色，局部95
        #plt.plot(d, result['down_局部'].values, 'b--') #蓝色，局部5
        #plt.plot(d, result['up_全局'].values, 'k-.')  #黑色，全局99
        #plt.plot(d, result['down_全局'].values, 'k-.')  #黑色，全局1
        #plt.show()
        #fig_name =  year + '年行业' + indu + '.png'
        #fig.savefig(fig_name, dpi=300)

if __name__ == "__main__" :

    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)
    for year in year_list:
        for indu in indu_list:
            pool.apply_async(cal_metrics, (year, indu))
    pool.close()
    pool.join()
