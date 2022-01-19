import numpy as np
import linecache
import os

path = "25RyR_ISO_random8"


def get_avg_line():
    data = np.loadtxt("../data/" + path + "/blink/fn/Fn_00000000.csv")
    return len(data) - 3


def average(line, file_name, pattern):
    with open("../data/" + path + "/" + file_name, "w") as file_object:
        for filename in os.listdir("../data/" + path + "/blink/" + pattern):
            data = linecache.getline("../data/" + path + "/blink/" + pattern + "/" + filename, line)
            file_object.write(data)


if __name__ == '__main__':
    avg_line = get_avg_line()
    average(avg_line, "avg_fn_jsr.csv", "fn")
    average(avg_line, "avg_gn_jsr.csv", "gn")
