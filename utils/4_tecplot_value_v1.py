import os
import numpy as np
import pandas as pd

GRID_PATH = "25RyR_radius_0.8_center4_0501"
DATA_PATH = "20220517_random8_DCAFSR_33"
TYPE = "gn"

# ************************************************************************
grid = np.loadtxt("../parameters/grid/blink/" + GRID_PATH + "/gridt.dat", dtype=np.float64)
NP = len(grid)
PX = grid[:, 0]
PY = grid[:, 1]

nod = np.loadtxt("../parameters/grid/blink/" + GRID_PATH + "/nod.dat", dtype=np.int64)
NE = len(nod)
NOD = nod.T

os.makedirs("../tecplot_data/" + DATA_PATH)
for filename in os.listdir("../data/" + DATA_PATH + "/blink/" + TYPE):
    df = pd.read_csv("../data/" + DATA_PATH + "/blink/" + TYPE + "/" + filename, dtype=str, header=None)
    value = np.array(df.iloc[:, 0]).astype('float64')

    zone_name = filename[:11]
    with open("../tecplot_data/" + DATA_PATH + "/" + zone_name + ".plt", "w") as plt_file:
        plt_file.write("TITLE = \"Example: 2D Finite-Element Data\"" + "\n")
        plt_file.write("VARIABLES=\"X\",\"Y\",\"VALUE\"" + "\n")
        # N 表示结点个数，E表示单元个数，F=FEPOINT表示数据以有限元方式组织，ET表示单元类型为三角形
        plt_file.write(
            "ZONE T=\"" + zone_name + "\" N=" + str(NP) + ", E=" + str(NE) + ", F=FEPOINT, ET=TRIANGLE" + "\n")
        # 数据第一部分：结点数据。前两列对应结点坐标X和Y，第三列为结点处的值。
        for i in range(NP):
            plt_file.write(str(PX[i]) + " ")
            plt_file.write(str(PY[i]) + " ")
            plt_file.write(str(value[i]) + "\n")
        # 数据第二部分：单元数据。每一行定义一个单元。
        for j in range(NE):
            plt_file.write(str(NOD[0, j]) + " ")
            plt_file.write(str(NOD[1, j]) + " ")
            plt_file.write(str(NOD[2, j]) + "\n")
    print(zone_name)
