import linecache
import os

path = "25RyR_Random6_ISO_100%"
avg_line = 19614


def avg_ca_jsr():
    with open("../data/" + path + "/avg_fn_jsr.csv", "w") as file_object:
        for filename in os.listdir("../data/" + path + "/blink/fn"):
            data = linecache.getline("../data/" + path + "/blink/fn/" + filename, avg_line)
            file_object.write(data)


def avg_gn_jsr():
    with open("../data/" + path + "/avg_gn_jsr.csv", "w") as file_object:
        for filename in os.listdir("../data/" + path + "/blink/gn"):
            data = linecache.getline("../data/" + path + "/blink/gn/" + filename, avg_line)
            file_object.write(data)


avg_ca_jsr()
avg_gn_jsr()
