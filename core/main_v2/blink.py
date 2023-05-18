from math import sqrt
import numpy as np
from blink_coeff_matrix import LN_MATRIX, CTRL_AREA, NMAX, TRIANGLE_NUMBER, ABC_MATRIX, AREA, TOTAL_AREA
from constant import B_INNER, B_INFLOW, B_OUTFLOW, K2, K1, DCAJSR, F, BCSQ, KDCSQ, DCAFSR, CCAFSR, DCAF, \
    DT, H_JSR, UNITEC, MOLNUM
from grid_info import NOD, NPOCH, NP, PX, PY, NE


def point_type(num_of_tri):
    """
    判断三角形不同点的类型并返回数组
    :param num_of_tri: 三角形序号
    :return: inner_point, out_boundary, in_boundary, in_L, out_L
    """
    inner_point = []
    out_boundary = []
    in_boundary = []
    in_l = 0.
    out_l = 0.
    for i in range(0, 3):
        n = NOD[i, num_of_tri]
        if NPOCH[n] == B_INNER:
            inner_point.append(n)  # 存的点位置
        elif NPOCH[n] == B_INFLOW:
            in_boundary.append(n)
        elif NPOCH[n] == B_OUTFLOW:
            out_boundary.append(n)

    if len(in_boundary) == 2:
        for i in range(0, 3):
            n = NOD[i, num_of_tri]
            if (n != in_boundary[0]) and (n != in_boundary[1]):
                in_l = LN_MATRIX[num_of_tri][i][0]

    if len(out_boundary) == 2:
        for i in range(0, 3):
            n = NOD[i, num_of_tri]
            if (n != out_boundary[0]) and (n != out_boundary[1]):
                out_l = LN_MATRIX[num_of_tri][i][0]

    return inner_point, out_boundary, in_boundary, in_l, out_l


def blink_fn_equation(fn, gn, CCACYTO, DCARYR, iteration):
    """
    构建钙离子 n+1 步的方程
    """
    new_fn = np.zeros(NP, float)  # 存每一次迭代的结果fn
    med_fn = np.zeros(NP, float)  # 临时变量
    for k in range(0, iteration):
        for i in range(0, NP):
            cal_one = 0.0
            cal_two = (K2 * gn[i] - K1 * fn[i] * (F - gn[i])) * CTRL_AREA[i]  # 系数
            cal_three = 0.0
            cal_four = 0.0
            cal_five = 0.0  # 分子入流出流
            cal_six = 0.0  # 分母入流出流

            for j in range(0, NMAX):
                if TRIANGLE_NUMBER[i][j][0] != -1:
                    tri_id = TRIANGLE_NUMBER[i][j][0]  # 点i控制的第j个三角形的序号
                    ctrl_relative_id = TRIANGLE_NUMBER[i][j][1]  # 点i在这个三角形中相对第几个点，取值范围只有0,1,2

                    nod1_relative_id = (ctrl_relative_id + 1) % 3
                    nod2_relative_id = (ctrl_relative_id + 2) % 3
                    nod1_id = NOD[nod1_relative_id, tri_id]
                    nod2_id = NOD[nod2_relative_id, tri_id]

                    if k == 0:
                        cca1_nod1 = fn[i]
                        cca1_nod2 = fn[nod1_id]
                        cca1_nod3 = fn[nod2_id]
                    else:
                        cca1_nod1 = (fn[i] + new_fn[i]) / 2.0
                        cca1_nod2 = (fn[nod1_id] + new_fn[nod1_id]) / 2.0
                        cca1_nod3 = (fn[nod2_id] + new_fn[nod2_id]) / 2.0
                    # 求的不带边界点的
                    # ABC_MATRIX : 第tri_pos个三角形，相对第(0，1，2)个点，第3维度(1 a;2 b;3 c)
                    # LN_MATRIX : 第tri_pos个三角形，相对第(0，1，2)个点，第3维度(1 L;2 Nix;3 Niy)
                    # nod_index 中心点   column_2、column_3 另外两个点    nod_2、nod_3  另外两个点绝对位置
                    # cal_one 从0开始

                    # nod_2,nod_3只要有一个是内部结点，就计算这个三角形
                    # nod_2,nod_3都是边界点（>0），跳过这个三角形
                    if NPOCH[nod1_id] == B_INNER or NPOCH[nod2_id] == B_INNER:
                        cal_one += DCAJSR * (LN_MATRIX[tri_id][ctrl_relative_id][1] *
                                             (cca1_nod2 * ABC_MATRIX[tri_id][nod1_relative_id][1] +
                                              cca1_nod3 * ABC_MATRIX[tri_id][nod2_relative_id][1])
                                             + LN_MATRIX[tri_id][ctrl_relative_id][2] *
                                             (cca1_nod2 * ABC_MATRIX[tri_id][nod1_relative_id][2] +
                                              cca1_nod3 * ABC_MATRIX[tri_id][nod2_relative_id][2])
                                             ) * LN_MATRIX[tri_id][ctrl_relative_id][0]

                        # nod1_id,nod2_id只要有一个是内部结点，就计算这个三角形
                        # nod1_id,nod2_id都是边界点（>0），跳过这个三角形
                        cal_four += DCAJSR * 0.5 * (
                                LN_MATRIX[tri_id][ctrl_relative_id][1] * ABC_MATRIX[tri_id][ctrl_relative_id][1] +
                                LN_MATRIX[tri_id][ctrl_relative_id][2] * ABC_MATRIX[tri_id][ctrl_relative_id][2]) * \
                                    LN_MATRIX[tri_id][ctrl_relative_id][0]

                    # 计算分子分母公共项
                    avg_cca = (cca1_nod1 + cca1_nod2 + cca1_nod3) / 3.0
                    cal_three += (1 + BCSQ * KDCSQ / ((KDCSQ + avg_cca) ** 2)) * AREA[tri_id]

                    # 判断点的类型,输入第tri_id个三角形，第i个点
                    inner_point, out_boundary_point, in_boundary_point, in_l, out_l = point_type(tri_id)
                    if k == 0:
                        cca2_nod2 = fn[nod1_id]
                        cca2_nod3 = fn[nod2_id]
                    else:
                        cca2_nod2 = new_fn[nod1_id]
                        cca2_nod3 = new_fn[nod2_id]

                    if len(out_boundary_point) == 2 and DCARYR != 0:  # 为出流边界点时
                        fk = (cca2_nod2 + cca2_nod3) / 3.0
                        cal_five += DCARYR * (CCACYTO - fk) * out_l  # 分子
                        cal_six += (DCARYR * out_l) / 3.0  # 分母

                    if len(in_boundary_point) == 2:  # 为入流边界点时
                        fj = (cca2_nod2 + cca2_nod3) / 3.0
                        cal_five += DCAFSR * (CCAFSR - fj) * in_l  # 分子
                        cal_six += (DCAFSR * in_l) / 3.0  # 分母
                else:
                    break
            # 中间结果
            med_fn[i] = (DT * cal_one + DT * cal_two + fn[i] * cal_three + DT * fn[i]
                         * cal_four + DT * cal_five) / (cal_three - DT * cal_four + DT * cal_six)
        # 当每次迭代所有点都计算完后，再赋值
        new_fn = np.copy(med_fn)
    return new_fn


def blink_gn_equation(fn, gn, iteration):
    """
    构建Gn方程
    """
    new_gn = np.zeros(NP, float)
    med_gn = np.zeros(NP, float)

    for k in range(0, iteration):
        for i in range(0, NP):  # i代表点，m代表该点三角形的个数 j第j个三角形 N1代表该三角形的其中一点
            cal_one = 0.
            cal_two = (K1 * fn[i] * (F - gn[i]) - K2 * gn[i]) * CTRL_AREA[i]
            cal_three = 0.

            for j in range(0, NMAX):
                if TRIANGLE_NUMBER[i][j][0] != -1:
                    tri_id = TRIANGLE_NUMBER[i][j][0]  # 点i控制的第j个三角形的序号
                    ctrl_relative_id = TRIANGLE_NUMBER[i][j][1]  # 点i在这个三角形中相对第几个点，取值范围只有0,1,2

                    nod1_relative_id = (ctrl_relative_id + 1) % 3
                    nod2_relative_id = (ctrl_relative_id + 2) % 3
                    nod1_id = NOD[nod1_relative_id, tri_id]
                    nod2_id = NOD[nod2_relative_id, tri_id]

                    if k == 0:
                        gn_nod2 = gn[nod1_id]
                        gn_nod3 = gn[nod2_id]
                    else:
                        gn_nod2 = (gn[nod1_id] + new_gn[nod1_id]) / 2.0
                        gn_nod3 = (gn[nod2_id] + new_gn[nod2_id]) / 2.0
                    # 求的不带边界点的
                    # abcMatrix : 第tri_pos个三角形，相对第(0，1，2)个点，第3维度(1 a;2 b;3 c)
                    # nlMatrix : 第tri_pos个三角形，相对第(0，1，2)个点，第3维度(1 L;2 Nix;3 Niy)
                    # nod_index 中心点   column_2、column_3 另外两个点    nod_2、nod_3  另外两个点绝对位置

                    # nod_2,nod_3只要有一个是内部结点，就计算这个三角形
                    # nod_2,nod_3都是边界点（>0），跳过这个三角形
                    if NPOCH[nod1_id] == B_INNER or NPOCH[nod2_id] == B_INNER:
                        cal_one += DCAF * (LN_MATRIX[tri_id][ctrl_relative_id][1] *
                                           (gn_nod2 * ABC_MATRIX[tri_id][nod1_relative_id][1] +
                                            gn_nod3 * ABC_MATRIX[tri_id][nod2_relative_id][1])
                                           + LN_MATRIX[tri_id][ctrl_relative_id][2] *
                                           (gn_nod2 * ABC_MATRIX[tri_id][nod1_relative_id][2] +
                                            gn_nod3 * ABC_MATRIX[tri_id][nod2_relative_id][2])
                                           ) * LN_MATRIX[tri_id][ctrl_relative_id][0]
                        cal_three += 0.5 * DCAF * (
                                LN_MATRIX[tri_id][ctrl_relative_id][1] * ABC_MATRIX[tri_id][ctrl_relative_id][1] +
                                LN_MATRIX[tri_id][ctrl_relative_id][2] * ABC_MATRIX[tri_id][ctrl_relative_id][2]) * \
                                     LN_MATRIX[tri_id][ctrl_relative_id][0]
                else:
                    break
            med_gn[i] = (DT * cal_one + DT * cal_two + gn[i] * CTRL_AREA[i] + gn[i] * DT * cal_three) / (
                    CTRL_AREA[i] - DT * cal_three)
        new_gn = np.copy(med_gn)
    gn = np.copy(new_gn)
    return gn


def average_concentration(conc_matrix):
    """
    求平均钙离子/荧光钙浓度
    :param conc_matrix: 钙离子/荧光钙数值
    :return: avg_conc 平均浓度
    """
    total_conc = 0.0
    avg_conc = 0.0
    for i in range(0, NP):
        total_conc = total_conc + conc_matrix[i] * CTRL_AREA[i]
    total_conc = total_conc / 3
    if TOTAL_AREA > 0.00000000000001:
        avg_conc = total_conc / TOTAL_AREA
    return avg_conc


def ca_current_and_ryr_inside_store(fn, DCARYR):
    """
    求钙离子电流
    """
    ca_in = 0.0
    ca_out = 0.0
    arc_len = 0.0
    for i in range(0, NE):
        for j in range(0, 3):
            p1 = NOD[(j + 1) % 3, i]
            p2 = NOD[(j + 2) % 3, i]
            #  out current
            if NPOCH[p1] == B_OUTFLOW and NPOCH[p2] == B_OUTFLOW:
                length = sqrt((PX[p1] - PX[p2]) ** 2 + (PY[p1] - PY[p2]) ** 2)
                ca_out = ca_out + length * (fn[p1] + fn[p2]) / 2
                #  inside store
                arc_len = arc_len + length
            #  in current
            if NPOCH[p1] == B_INFLOW and NPOCH[p2] == B_INFLOW:
                length = sqrt((PX[p1] - PX[p2]) ** 2 + (PY[p1] - PY[p2]) ** 2)
                ca_in = ca_in + length * (CCAFSR - (fn[p1] + fn[p2]) / 2)
    cca_store = ca_out / arc_len
    ca_out = ca_out * DCARYR * H_JSR
    ca_in = ca_in * DCAFSR * H_JSR
    i_ca_ryr = ca_out * UNITEC * 2 * MOLNUM * (10.0 ** -11)
    i_ca_fsr = ca_in * UNITEC * 2 * MOLNUM * (10.0 ** -11)

    return cca_store, i_ca_ryr, i_ca_fsr
