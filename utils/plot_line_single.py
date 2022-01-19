import matplotlib.pyplot as plt
import csv
from matplotlib import font_manager

font_manager.fontManager.addfont('../fonts/time-simsun.ttf')

plt.rcParams['font.sans-serif'] = 'Times New Roman + Simsun'
plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams["font.family"] = "Microsoft Yahei"
# plt.rcParams['font.sans-serif'] = ['SimHei']

path = "25RyR_random6_DCAFSR_100%"

# 文件描述
filename = "ppt"
title = "ISO病理"


# *****************************************************************************
def plot(type, filename, title, path):
    """
    绘制x:time y:concentration曲线图
    :param type: ['fn','gn']
    :param filename: 文件名前缀
    :param title: 标题前缀
    :param path: 读取数据路径
    :return:
    """

    save_steps = 100

    plt.figure()

    x = []
    y = []
    j = 0

    with open("../data/" + path + "/avg_" + type + "_jsr.csv", 'r') as ca_csvfile1:
        plots = csv.reader(ca_csvfile1, delimiter='\t')
        for row in plots:
            x.append(j * save_steps)
            y.append(float(row[0]))
            j = j + 1
    plt.plot(x, y, linewidth=1)

    # plt.title(type + "   " + title, fontsize=14)
    plt.xlim((0, 50000))
    # plt.xlim((0, j * save_steps))
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.grid(linestyle="--")
    plt.xticks([0, 10000, 20000, 30000, 40000, 50000], [0, 0.02, 0.04, 0.06, 0.08, 0.1])
    plt.xlabel("time(s)", fontsize=13)
    plt.ylabel("concentration", fontsize=13)
    plt.savefig("../figure/" + filename + "_" + type + ".png")
    plt.show()


if __name__ == '__main__':
    plot("fn", filename, title, path)
    plot("gn", filename, title, path)
