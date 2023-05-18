import csv
import os
import numpy as np
import pandas as pd
from math import fmod

from blink import average_concentration, ca_current_and_ryr_inside_store, blink_fn_equation, blink_gn_equation
from constant import SAVE_PATH, NR, CCAJSR, CCAF, START_STEP, BCAF, BCAM, BTRC, BSRM, BSLM, KDCAF, KDCAM, KDTRC, \
    KDSRM, KDSLM, RELEASE_TIME, DT, END_TIME, SAVE_INTERVAL, CCACYTREST, DCARYR, KRYR2
from smith_spark import cal_dye, cal_buffers, cytosolic_buffers_equation, cytosolic_ca_equation, \
    cytosolic_gn_equation
from grid_info import NP

'''
耦联子
'''


def do_loop_diffusion():
    # 保存路径
    data_path = "../../data/" + SAVE_PATH

    # 临时变量，0.02s后置0
    d_ca_ryr_jsr = DCARYR
    d_ca_ryr_cyto = KRYR2

    # blink赋初值
    fn = np.full(NP, CCAJSR)  # fn,肌质网每一点钙的浓度,为肌质网每一点的初始钙浓度赋值为1
    gn = np.full(NP, CCAF)  # gn,初值1/14

    # Spark赋初值
    c_ca_cyto = np.full(NR, CCACYTREST)
    c_caf = np.full(NR, CCACYTREST * BCAF / (CCACYTREST + KDCAF))
    c_cam = np.full(NR, CCACYTREST * BCAM / (CCACYTREST + KDCAM))
    c_trc = np.full(NR, CCACYTREST * BTRC / (CCACYTREST + KDTRC))
    c_srm = np.full(NR, CCACYTREST * BSRM / (CCACYTREST + KDSRM))
    c_slm = np.full(NR, CCACYTREST * BSLM / (CCACYTREST + KDSLM))
    j_dye = np.zeros(NR, float)
    j_buffers = np.zeros(NR, float)

    if START_STEP == 0:  # 开始前，先存储第0步初值
        times = 0.0  # 当前时间
        step = 0  # 当前步数

        # 写初值
        if not os.path.exists(data_path + "/blink"):
            os.makedirs(data_path + "/blink")
        with open(data_path + "/blink/blink_00000000.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['NP', 'fn', 'gn'])
            for i in range(0, NP):
                writer.writerow([i + 1, fn[i], gn[i]])
            avg_fn_jsr = average_concentration(fn)
            avg_gn_jsr = average_concentration(gn)
            writer.writerow(['average', avg_fn_jsr, avg_gn_jsr])
            c_ca_store, i_ca_ryr, i_ca_fsr = ca_current_and_ryr_inside_store(fn, d_ca_ryr_jsr)
            writer.writerow(['interface_in', c_ca_store])
            writer.writerow(['interface_out', c_ca_cyto[0]])
            writer.writerow(['i_ca_ryr', i_ca_ryr])
            writer.writerow(['i_ca_fsr', i_ca_fsr])
            writer.writerow(['step', step])
            writer.writerow(['times', times])
        file.close()
        print("数据写入【" + SAVE_PATH + "】blink_00000000.csv...")

        if not os.path.exists(data_path + "/spark"):
            os.makedirs(data_path + "/spark")
        with open(data_path + "/spark/spark_00000000.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['NP', 'c_ca_cyto', 'c_caf', 'c_cam', 'c_trc', 'c_srm', 'c_slm'])
            for i in range(0, NR):
                writer.writerow([i + 1, c_ca_cyto[i], c_caf[i], c_cam[i], c_trc[i], c_srm[i], c_slm[i]])
            writer.writerow(['step', step])
            writer.writerow(['times', times])
        file.close()
        print("数据写入【" + SAVE_PATH + "】spark_00000000.csv...")

    else:  # 不是第一步开始，先读取先前一步保存的结果
        blink_df = pd.read_csv(data_path + "/blink/blink_" + str(START_STEP - 1).zfill(8) + ".csv", dtype=str,
                               index_col=0)
        fn = np.array(blink_df.loc['1':str(NP), 'fn']).astype('float64')
        gn = np.array(blink_df.loc['1':str(NP), 'gn']).astype('float64')
        step = int(blink_df.loc['step', 'fn'])
        times = float(blink_df.loc['times', 'fn'])
        print("数据读取【" + SAVE_PATH + "】blink_" + str(step).zfill(8) + ".csv...")

        spark_df = pd.read_csv(data_path + "/spark/spark_" + str(START_STEP - 1).zfill(8) + ".csv", dtype=str,
                               index_col=0)
        c_ca_cyto = np.array(spark_df.loc['1':str(NR), 'c_ca_cyto']).astype('float64')
        c_caf = np.array(spark_df.loc['1':str(NR), 'c_caf']).astype('float64')
        c_cam = np.array(spark_df.loc['1':str(NR), 'c_cam']).astype('float64')
        c_trc = np.array(spark_df.loc['1':str(NR), 'c_trc']).astype('float64')
        c_srm = np.array(spark_df.loc['1':str(NR), 'c_srm']).astype('float64')
        c_slm = np.array(spark_df.loc['1':str(NR), 'c_slm']).astype('float64')
        print("数据读取【" + SAVE_PATH + "】Spark_" + str(step).zfill(8) + ".csv...")

    while times <= END_TIME:
        times = times + DT
        step = step + 1

        if times >= (RELEASE_TIME - DT / 2):
            d_ca_ryr_jsr = 0
            d_ca_ryr_cyto = 0

        # 计算blink
        new_fn = blink_fn_equation(fn, gn, c_ca_cyto[0], d_ca_ryr_jsr, 10)
        gn = blink_gn_equation(fn, gn, 10)
        fn = np.copy(new_fn)
        c_ca_store, i_ca_ryr, i_ca_fsr = ca_current_and_ryr_inside_store(fn, d_ca_ryr_jsr)
        # c_ca_store = 1.0

        # 计算spark
        j_dye = cal_dye(j_dye, c_ca_cyto, c_caf)
        j_buffers = cal_buffers(j_buffers, c_ca_cyto, c_cam, c_trc, c_srm, c_slm)
        # 因为上面两个函数已经计算出fn和gn方程需要的dye和buffers
        # 所以下面计算缓冲物的函数对后面两个fn和gn方程没有影响
        # 放在fn和gn前面是因为用到的浓度是n时刻旧的值
        c_cam, c_trc, c_srm, c_slm = cytosolic_buffers_equation(c_ca_cyto, c_cam, c_trc, c_srm, c_slm)
        c_ca_cyto = cytosolic_ca_equation(c_ca_cyto, j_dye, j_buffers, c_ca_store, d_ca_ryr_cyto, 10)
        c_caf = cytosolic_gn_equation(c_caf, j_dye, 10)

        if fmod(step, SAVE_INTERVAL) == 0 or times == END_TIME:
            with open(data_path + "/blink/blink_" + str(step).zfill(8) + ".csv", "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['NP', 'fn', 'gn'])
                for i in range(0, NP):
                    writer.writerow([i + 1, fn[i], gn[i]])
                avg_fn_jsr = average_concentration(fn)
                avg_gn_jsr = average_concentration(gn)
                writer.writerow(['average', avg_fn_jsr, avg_gn_jsr])
                writer.writerow(['interface_in', c_ca_store])
                writer.writerow(['interface_out', c_ca_cyto[0]])
                writer.writerow(['i_ca_ryr', i_ca_ryr])
                writer.writerow(['i_ca_fsr', i_ca_fsr])
                writer.writerow(['step', step])
                writer.writerow(['times', times])
            file.close()
            print("数据写入【" + SAVE_PATH + "】blink_" + str(step).zfill(8) + ".csv...")

            with open(data_path + "/spark/spark_" + str(step).zfill(8) + ".csv", "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['NP', 'c_ca_cyto', 'c_caf', 'c_cam', 'c_trc', 'c_srm', 'c_slm'])
                for i in range(0, NR):
                    writer.writerow([i + 1, c_ca_cyto[i], c_caf[i], c_cam[i], c_trc[i], c_srm[i], c_slm[i]])
                writer.writerow(['step', step])
                writer.writerow(['times', times])
            file.close()
            print("数据写入【" + SAVE_PATH + "】spark_" + str(step).zfill(8) + ".csv...")


do_loop_diffusion()
