# 输入data、figure文件下的保存路径名
SAVE_PATH = "保存路径"
# 请把钙空穴网格以及网格三角形单元数据在grid、triangle_number包下，并输入路径
TRIANGLE_PATH = "三角单元路径"
GRID_PATH = "网格路径"
START_STEP = 0  # 从多少步开始，初始从第0步开始。如果有10000步数据，从10001步开始

RELEASE_TIME = 2 * 10 ** -2  # 0.02s,这个就是ryr通道开放的时间，后80毫秒是恢复的
END_TIME = 0.1  # 结束时间
SAVE_INTERVAL = 100  # 文件保存间隔
DT = 2 * 10 ** -6

# ***************************************************************************************
"""
blink constant
"""

# 初始浓度
CCAF = (1 / 14) * 1.14
# CCAMYO = 0.001
F = 0.1  # [F]T   fluo-5总浓度

# 系数
# 钙离子
DCAFSR = 0.7854 * 10 ** 6  # 入流量
DCARYR = 0.25 * 6.5 * 10 ** 7  # 出流量
DCAJSR = 3.5 * 10 ** 8  # 终池jSR自由Ca离子扩散系数
# 钙离子结合荧光染料
DCAF = 2 * 10 ** 7  # jSR扩散系数
K1 = 48800  # KF+  Ca离子和fluo-5的结合速率
K2 = 19520  # KF-  Ca离子和fluo-5的解离速率
# 钙离子结合缓冲物
BCSQ = 14.0  # 方程中的B，所有肌钙集蛋白（肌浆网SR上调控钙储存的主要结合蛋白，调节SR钙释放）的量
KDCSQ = 0.63  # 方程中的K，肌钙集蛋白的Ca离子解离常数

# 点的属性
B_INNER = 0  # 内部
B_INFLOW = 2  # 入流
B_WALL = 1  # 壁面
B_OUTFLOW = 4  # 出流
B_SYMMETRY = 8
B_SOURCE = 16

PMAX = 50000  # 点数
EMAX = 100000  # 三角形单元数
NVEX = 3  # 三角形顶点数

H_JSR = 30.0  # JSR的高度
UNITEC = 1.610217733  # 一个电荷的常数
MOLNUM = 6.0221367  # 摩尔常数，单位

CCAJSR = (K2 * CCAF) / (K1 * (F - CCAF))
CCAFSR = CCAJSR

# ***************************************************************************************
"""
smith spark constant
"""

# smith_spark 网格
NR = 1001  # 点数
R0 = 0
R1 = 10000
DR = (R1 - R0) / (NR - 1)  # dr=10   间距

# pump
MIUPUMP = 0.208
KPUMP = 0.184 * 10 ** -3
MPUMP = 3.9

# cytosolic spark
CCACYTREST = 1.0 * 10 ** -4
DCACYT = 3.5 * 10 ** 8
KRYR2 = 1.22522 * 10 ** 10  # 胞浆自由Ca离子扩散系数
# CCASTORE = 1.0

# Fluo-3 parameter
KPCAF = 80000  # K_plus_Ca_Fluo-3  结合速率
KMCAF = 90  # K_minus_Ca_Fluo-3    解离速率
BCAF = 0.05  # [F]T_Ca_Fluo-3     Total concentration for Fluo-3
KDCAF = KMCAF / KPCAF  # Kn = Kn-/Kn+
# DCAF = 2 * 10 ** 7  # 扩散系数

# Calmodulin parameter  钙调蛋白
KPCAM = 100000
KMCAM = 38
BCAM = 0.024
KDCAM = KMCAM / KPCAM

# Troponin C parameter  肌钙蛋白C
KPTRC = 39000
KMTRC = 20
BTRC = 0.07
KDTRC = KMTRC / KPTRC

# SR membrane parameter
KPSRM = 115000
KMSRM = 100
BSRM = 0.047
KDSRM = KMSRM / KPSRM

# SL membrane parameter
KPSLM = 115000
KMSLM = 1000
BSLM = 1.124
KDSLM = KMSLM / KPSLM
