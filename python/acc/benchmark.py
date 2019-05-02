import time
import random
from timeit import timeit
import timeit, functools
import numpy as np
import numba
import multiprocessing
import sys

# 计算500期的移动均线，并将结果保存到一个列表里返回
def ma_basic(data, ma_length):

    # 用于保存均线输出结果的列表
    ma = []

    # 计算均线用的数据窗口
    data_window = data[:ma_length]

    # 测试用数据（去除了之前初始化用的部分）
    test_data = data[ma_length:]

    # 模拟实盘不断收到新数据推送的情景，遍历历史数据计算均线
    for new_tick in test_data:
        # 移除最老的数据点并增加最新的数据点
        data_window.pop(0)
        data_window.append(new_tick)

        # 遍历求均值
        sum_tick = 0
        for tick in data_window:
            sum_tick += tick
        ma.append(sum_tick/ma_length)

    return ma

def ma_numpy_wrong(data, ma_length):
    ma = []
    data_window = data[:ma_length]
    test_data = data[ma_length:]

    for new_tick in test_data:
        data_window.pop(0)
        data_window.append(new_tick)

        # 使用numpy求均值，注意这里本质上每次循环都在创建一个新的numpy数组对象，开销很大
        data_array = np.array(data_window)
        ma.append(data_array.mean())

    return ma

def ma_numpy_right(data, ma_length):
    ma = []
    # 用numpy数组来缓存计算窗口内的数据
    data_window = np.array(data[:ma_length])

    test_data = data[ma_length:]

    for new_tick in test_data:
        # 使用numpy数组的底层数据偏移来实现数据更新
        data_window[0:ma_length-1] = data_window[1:ma_length]
        data_window[-1] = new_tick
        ma.append(data_window.mean())

    return ma

@numba.jit
def ma_numba(data, ma_length):
    ma = []
    data_window = data[:ma_length]
    test_data = data[ma_length:]

    for new_tick in test_data:
        data_window.pop(0)
        data_window.append(new_tick)
        sum_tick = 0
        for tick in data_window:
            sum_tick += tick
        ma.append(sum_tick/ma_length)

    return ma

def ma_cache(data, ma_length):
    ma = []
    data_window = data[:ma_length]
    test_data = data[ma_length:]

    # 缓存的窗口内数据求和结果
    sum_buffer = 0

    for new_tick in test_data:
        old_tick = data_window.pop(0)
        data_window.append(new_tick)

        # 如果缓存结果为空，则先通过遍历求第一次结果
        if not sum_buffer:
            sum_tick = 0
            for tick in data_window:
                sum_tick += tick
            ma.append(sum_tick/ma_length)

            # 将求和结果缓存下来
            sum_buffer = sum_tick
        else:
            # 这里的算法将计算复杂度从O(n)降低到了O(1)
            sum_buffer = sum_buffer - old_tick + new_tick
            ma.append(sum_buffer/ma_length)

    return ma

if __name__ == "__main__" :

    data_length = 100000    # 总数据量
    # 生成测试数据
    data = []
    for i in range(data_length):
        data.append(random.randint(1, 100))
    ma_length = 500         # 移动均值的窗口
    test_times = 10         # 测试次数

    t_basic = timeit.Timer(functools.partial(ma_basic, data, ma_length))
    t_numpy_wrong = timeit.Timer(functools.partial(ma_numpy_wrong, data, ma_length))
    t_numpy_right = timeit.Timer(functools.partial(ma_numpy_right, data, ma_length))
    t_numba = timeit.Timer(functools.partial(ma_numba, data, ma_length))
    t_cache_algorithm = timeit.Timer(functools.partial(ma_cache, data, ma_length))

    print("basic :\t" + str(t_basic.timeit(test_times)))
    print("numpy wrong :\t" + str(t_numpy_wrong.timeit(test_times)))
    print("numpy right :\t" + str(t_numpy_right.timeit(test_times)))
    print("numba :\t" + str(t_numba.timeit(test_times)))
    print("cache algorithm :\t" + str(t_cache_algorithm.timeit(test_times)))

    start = time.time()
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)
    result = []
    for j in range(test_times):
        result.append(pool.apply_async(ma_basic, (data, ma_length)))

    pool.close()
    pool.join()
    elapsed = time.time() - start
    print("multiprocessing with basic algorithm :\t" + str(elapsed))

    start = time.time()
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)
    result = []
    for j in range(test_times):
        result.append(pool.apply_async(ma_cache, (data, ma_length)))

    pool.close()
    pool.join()
    elapsed = time.time() - start
    print("multiprocessing with cache algorithm :\t" + str(elapsed))
