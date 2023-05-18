import os
import numpy as np
import pandas as pd

GRID_PATH = "25RyR_radius_0.8_random25_0623"

# ************************************************************************
grid = np.loadtxt("../parameters/grid/blink/" + GRID_PATH + "/gridt.dat", dtype=np.float64)
NP = len(grid)
PX = grid[:, 0]
PY = grid[:, 1]

nod = np.loadtxt("../parameters/grid/blink/" + GRID_PATH + "/nod.dat", dtype=np.int64)
NE = len(nod)
NOD = nod.T

NPOCH = np.loadtxt('../parameters/grid/blink/' + GRID_PATH + '/npoch.dat', dtype=np.int64)

if not os.path.exists("../tecplot_data/" + GRID_PATH + "_NPOCH"):
    os.makedirs("../tecplot_data/" + GRID_PATH + "_NPOCH")

with open("../tecplot_data/" + GRID_PATH + "_NPOCH/NPOCH.plt", "w") as plt_file:
    plt_file.write("TITLE = \"Example: 2D Finite-Element Data\"" + "\n")
    plt_file.write("VARIABLES=\"X\",\"Y\",\"VALUE\"" + "\n")
    # N 表示结点个数，E表示单元个数，F=FEPOINT表示数据以有限元方式组织，ET表示单元类型为三角形
    plt_file.write("ZONE T=\"NPOCH\" N=" + str(NP) + ", E=" + str(NE) + ", F=FEPOINT, ET=TRIANGLE" + "\n")

    # 数据第一部分：结点数据。前两列对应结点坐标X和Y，第三列为结点处的值。
    for i in range(NP):
        plt_file.write(str(PX[i]) + " ")
        plt_file.write(str(PY[i]) + " ")
        plt_file.write(str(NPOCH[i]) + "\n")

    # 数据第二部分：单元数据。每一行定义一个单元。
    for j in range(NE):
        plt_file.write(str(NOD[0, j]) + " ")
        plt_file.write(str(NOD[1, j]) + " ")
        plt_file.write(str(NOD[2, j]) + "\n")
