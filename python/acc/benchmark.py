import time
import random
from timeit import timeit
import timeit, functools

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

        # 遍历求均线
        sum_tick = 0
        for tick in data_window:
            sum_tick += tick
        ma.append(sum_tick/ma_length)

    # 返回数据
    return ma

# 运行测试
#start = time.time()

# for i in range(test_times):
#     result = ma_basic(data, ma_length)
#
# time_per_test = (time.time()-start)/test_times
# time_per_point = time_per_test/(data_length - ma_length)
#
# print u'单次耗时：%s秒' %time_per_test
# print u'单个数据点耗时：%s微秒' %(time_per_point*1000000)
# print u'最后10个移动平均值：', result[-10:]

if __name__ == "__main__" :
    data = []
    data_length = 100000    # 总数据量
    ma_length = 500         # 移动均线的窗口
    test_times = 10         # 测试次数

    for i in range(data_length):
        data.append(random.randint(1, 100))

    t = timeit.Timer(functools.partial(ma_basic, data, ma_length))

    print(t.timeit(test_times))
