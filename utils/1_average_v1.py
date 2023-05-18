# 求fn、gn平均值
# @ version: 1.0

import numpy as np
import linecache
import os

# 修改读取数据路径
path = "20221001_1RyR"


def get_avg_line():
    data = np.loadtxt("../data/" + path + "/blink/fn/Fn_00000000.csv")
    return len(data)


def average(line, save_file, pattern):
    with open("../data/" + path + "/" + save_file, "w") as file_object:
        for filename in os.listdir("../data/" + path + "/blink/" + pattern):
            data = linecache.getline("../data/" + path + "/blink/" + pattern + "/" + filename, line)
            file_object.write(data)


if __name__ == '__main__':
    length = get_avg_line()

    average(length - 3, "avg_fn_jsr.csv", "fn")
    average(length - 3, "avg_gn_jsr.csv", "gn")
    average(length - 2, "i_ca_rsr.csv", "fn")
    average(length - 1, "i_ca_fsr.csv", "fn")
