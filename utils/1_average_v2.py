# 求fn、gn平均值
# @ version: 2.0

import os
import pandas as pd

DATA_PATH = "20220709_DCAJSR_1"


def extract(x, y, file):
    for filename in os.listdir('../data/' + DATA_PATH + '/blink'):
        df = pd.read_csv('../data/' + DATA_PATH + '/blink/' + filename, dtype=str, index_col=0)
        with open('../data/' + DATA_PATH + '/' + file + '.csv', 'a') as f:
            f.writelines(str(float(df.loc[x, y])) + '\n')
        f.close()


if __name__ == '__main__':
    extract('i_ca_ryr', 'fn', 'i_ca_ryr')
    extract('i_ca_fsr', 'fn', 'i_ca_fsr')
    # extract('average', 'gn', 'avg_gn_jsr')
