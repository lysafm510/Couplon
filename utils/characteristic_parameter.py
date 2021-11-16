import pandas as pd

path = "25RyR_Random6_ISO_100%"

data_frame = pd.read_csv("../data/" + path + "/avg_gn_jsr.csv", header=None)
data = data_frame[0].tolist()


def amplitude():
    # ΔF/F0

    print("最大值：%s" % max(data))
    print("最小值：%s" % min(data))
    print("最小值步数：%s" % (data.index(min(data)) * 100))

    amplitude = (max(data) - min(data)) / max(data)
    print("振幅ΔF/F0：%s" % amplitude)
    print("******************************************* ")
    print()


def t50():
    dt = 2 * 10 ** -6
    peak_time = (data.index(min(data))) * 100 * dt
    half_concentration = (max(data) - min(data)) / 2 + min(data)

    print("tRise：%s" % peak_time)
    print("峰值一半时浓度：%s" % half_concentration)

    index = 100
    while (index < len(data) and data[index] < half_concentration):
        index = index + 1
    if index == len(data):
        print("暂未回升到一半")
    else:
        left_concentration = data[index - 1]
        right_concentration = data[index]
        half_time = index * 100 * dt - (right_concentration - half_concentration) * dt / (
                right_concentration - left_concentration)
        print("t50：%s" % (half_time - peak_time))
    print("******************************************* ")
    print()


def FDHM():
    dt = 2 * 10 ** -6
    half_concentration = (max(data) - min(data)) / 2 + min(data)

    index = 0
    while (index < len(data) and data[index] > half_concentration):
        index = index + 1
    if index == len(data):
        print("暂未下降到一半")
        return
    else:
        left_concentration = data[index - 1]
        right_concentration = data[index]
        half_time1 = index * 100 * dt - (right_concentration - half_concentration) * dt / (
                right_concentration - left_concentration)
        print("下降到一半时间：%s" % half_time1)
    index = 100
    while (index < len(data) and data[index] < half_concentration):
        index = index + 1
    if index == len(data):
        print("暂未回升到一半")
        return
    else:
        left_concentration = data[index - 1]
        right_concentration = data[index]
        half_time2 = index * 100 * dt - (right_concentration - half_concentration) * dt / (
                right_concentration - left_concentration)
        print("回升到一半时间：%s" % half_time2)
    print("FDHM：%s" % (half_time2 - half_time1))


amplitude()
t50()
FDHM()
