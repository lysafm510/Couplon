import matplotlib.pyplot as plt
import csv
from matplotlib import font_manager

font_manager.fontManager.addfont('../fonts/time-simsun.ttf')

plt.rcParams['font.sans-serif'] = 'Times New Roman + Simsun'
plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams["font.family"] = "Microsoft Yahei"
# plt.rcParams['font.sans-serif'] = ['SimHei']

path1 = "25RyR_ISO_random4"
path2 = "25RyR_ISO_random6"
path3 = "25RyR_ISO_random8"
# path4 = "25RyR_random6_DCAFSR_50%"
# path5 = "25RyR_random6_DCAFSR_100%"
paths = [path1, path2, path3]

label_list = ["4RyRs", "6RyRs", "8RyRs"]
# 文件描述
filename = "病理ISO_New"
title = ""


# *****************************************************************************
def plot(label_list, type, filename, title, paths):
    """
    绘制x:time y:concentration曲线图

    :param label_list: legend图例
    :param type: ['fn','gn']
    :param filename: 文件名前缀
    :param title: 标题前缀
    :param paths: 读取数据路径数组
    :return:
    """
    n = len(paths)
    plt.figure()
    max = 0
    save_steps = 100
    for i in range(0, n):
        x = []
        y = []
        j = 0

        with open("../data/" + paths[i] + "/avg_" + type + "_jsr.csv", 'r') as ca_csvfile1:
            plots = csv.reader(ca_csvfile1, delimiter='\t')
            for row in plots:
                x.append(j * save_steps)
                y.append(float(row[0]))
                j = j + 1
        plt.plot(x, y, linewidth=1)

        if j * save_steps > max:
            max = j * save_steps
    plt.title(type + "   " + title, fontsize=14)
    plt.legend(labels=label_list, fontsize=13)
    # plt.xlim((0, 50000))
    plt.xlim((0, max))
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.xticks([0, 10000, 20000, 30000, 40000, 50000], [0, 20, 40, 60, 80, 100])
    plt.xlabel("time(ms)", fontsize=13)
    plt.ylabel("concentration", fontsize=13)
    plt.grid(linestyle="--")
    plt.savefig("../figure/" + filename + "_" + type + ".png")
    plt.show()


if __name__ == '__main__':
    plot(label_list, "fn", filename, title, paths)
    plot(label_list, "gn", filename, title, paths)
