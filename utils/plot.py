import matplotlib.pyplot as plt
import csv

plt.rcParams["font.family"] = "Microsoft Yahei"
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

path1 = "25RyR_Random6_ISO_20%"
path2 = "25RyR_Random6_ISO_50%"
path3 = "25RyR_Random6_ISO_100%"

paths = [path1, path2, path3]
label_list = ["DCAFSR下降到1/5", "DCAFSR下降到1/4", "DCAFSR下降到1/3"]
description = "6通道_ISO刺激"


# *****************************************************************************
def plot(label_list, type, description, paths):
    """
    绘制x:time y:concentration曲线图

    :param label_list: legend图例
    :param type: ['fn','gn']
    :param description: 文件描述
    :param paths: 读取数据路径数组
    :return:
    """
    n = len(paths)
    plt.figure()
    plt.grid()
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
    plt.title(type + " _ " + description)
    plt.legend(labels=label_list)
    plt.xlim((0, 50000))
    plt.savefig("../figure/Transients_" + type + "_" + description + ".jpg")
    plt.show()


if __name__ == '__main__':
    plot(label_list, "fn", description, paths)
    plot(label_list, "gn", description, paths)
