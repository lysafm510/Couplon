import numpy as np
import linecache
import os

path = "test_1RyR_correct"


def get_avg_line():
    data = np.loadtxt("../data/" + path + "/blink/fn/Fn_00000000.csv")
    return (len(data) - 3)


def avg_ca_jsr(avg_line):
    with open("../data/" + path + "/avg_fn_jsr.csv", "w") as file_object:
        for filename in os.listdir("../data/" + path + "/blink/fn"):
            data = linecache.getline("../data/" + path + "/blink/fn/" + filename, avg_line)
            file_object.write(data)


def avg_gn_jsr(avg_line):
    with open("../data/" + path + "/avg_gn_jsr.csv", "w") as file_object:
        for filename in os.listdir("../data/" + path + "/blink/gn"):
            data = linecache.getline("../data/" + path + "/blink/gn/" + filename, avg_line)
            file_object.write(data)


if __name__ == '__main__':
    avg_line = get_avg_line()
    avg_ca_jsr(avg_line)
    avg_gn_jsr(avg_line)
