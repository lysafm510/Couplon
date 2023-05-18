import os
import numpy as np
import pandas as pd

# GRID_PATH = "25RyR_radius_0.8_center4_0501"
GRID_PATH = "25RyR_radius_0.8_random25_0623"
DATA_PATH = "20220709_caffeine_33"
TYPE = "gn"

# ************************************************************************
grid = np.loadtxt("../parameters/grid/blink/" + GRID_PATH + "/gridt.dat", dtype=np.float64)
NP = len(grid)
PX = grid[:, 0]
PY = grid[:, 1]

nod = np.loadtxt("../parameters/grid/blink/" + GRID_PATH + "/nod.dat", dtype=np.int64)
NE = len(nod)
NOD = nod.T

os.makedirs("../tecplot_data/" + DATA_PATH + "_" + TYPE)
for filename in os.listdir("../data/" + DATA_PATH + "/blink"):
    df = pd.read_csv("../data/" + DATA_PATH + "/blink/" + filename, dtype=str,
                     index_col=0)
    # print(df.loc['0':str(NP-1),1].values)
    # print(df.loc[:, :])
    value = np.array(df.loc['1':str(NP), TYPE]).astype('float64')
    zone_name = TYPE + "_" + filename[6:14]
    with open("../tecplot_data/" + DATA_PATH + "_" + TYPE + "/" + zone_name + ".plt", "w") as plt_file:
        plt_file.write("TITLE = \"Example: 2D Finite-Element Data\"" + "\n")
        plt_file.write("VARIABLES=\"X\",\"Y\",\"VALUE\"" + "\n")
        plt_file.write(
            "ZONE T=\"" + zone_name + "\" N=" + str(NP) + ", E=" + str(NE) + ", F=FEPOINT, ET=TRIANGLE" + "\n")
        for i in range(NP):
            plt_file.write(str(PX[i]) + " ")
            plt_file.write(str(PY[i]) + " ")
            plt_file.write(str(value[i]) + "\n")
        for j in range(NE):
            plt_file.write(str(NOD[0, j]) + " ")
            plt_file.write(str(NOD[1, j]) + " ")
            plt_file.write(str(NOD[2, j]) + "\n")
    print(zone_name)
