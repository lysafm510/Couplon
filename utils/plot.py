import matplotlib.pyplot as plt
import csv
from matplotlib import font_manager

font_manager.fontManager.addfont('../fonts/time-simsun.ttf')

plt.rcParams['font.sans-serif'] = 'Times New Roman + Simsun'
plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams["font.family"] = "Microsoft Yahei"
# plt.rcParams['font.sans-serif'] = ['SimHei']

path1 = "25RyR_random6_DCAFSR_20%"
path2 = "25RyR_random6_DCAFSR_25%"
path3 = "25RyR_random6_DCAFSR_33%"
path4 = "25RyR_random6_DCAFSR_50%"
path5 = "25RyR_random6_DCAFSR_100%"
paths = [path1, path2, path3, path4, path5]

label_list = ["DCAFSR下降到20%", "DCAFSR下降到25%", "DCAFSR下降到33%", "DCAFSR下降到50%", "DCAFSR下降到100%"]
# 文件描述
filename = "钙瞬变_6通道"
title = "6通道"


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
    plt.legend(labels=label_list, fontsize=10, loc=2)
    plt.xlim((0, 50000))
    # plt.xlim((0, max))
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.grid(linestyle="--")
    plt.savefig("../figure/" + filename + "_" + type + ".png")
    plt.show()


if __name__ == '__main__':
    plot(label_list, "fn", filename, title, paths)
    plot(label_list, "gn", filename, title, paths)
