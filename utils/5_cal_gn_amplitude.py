import numpy as np
import linecache
import os
import csv

# path1 = "20220801_center4_DCAF_0.001"
# path2 = "20220801_center4_DCAF_0.01"
# path3 = "20220801_center4_DCAF_0.1"
# path4 = "20220709_DCAJSR_1"

path = "20220709_DCAJSR_1"

data = np.loadtxt("../data/" + path + "/avg_gn_jsr.csv")
# return len(data) - 3
# return len(data) - 2

a = data[0]
n = data.size
with open("../data/" + path + "/avg_gn_jsr_new.csv", "w", newline='') as file_object:
    writer = csv.writer(file_object)
    for i in range(n):
        b = data[i] / a
        writer.writerow([b])
