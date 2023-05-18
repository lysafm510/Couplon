import os

tecplot_path = "8_25通道_咖啡因_入流量0"  # 读取tecplot_data位置，尽量为英文名
start_x = -300  # 起点坐标
start_y = 0
end_x = 300  # 终点坐标
end_y = 0
count = 600  # 离散点数量

os.makedirs("../tecplot_extract/" + tecplot_path + "/extract_files")

with open("../tecplot_extract/" + tecplot_path + "\\" + tecplot_path + ".mcr", "w",
          encoding='utf-8') as file:
    file.write("#!MC 1410" + "\n")
    for i in range(0, 501):
        j = i * 100
        a = str(j).zfill(8)
        file.write(
            "$!ReadDataSet  '\"E:\\Codefield\\Code_python\\Digitalcell\\Couplon_New\\tecplot_data\\" + tecplot_path +
            "\gn_" + a + ".plt\" '" + "\n")
        file.write("  ReadDataOption = New" + "\n")
        file.write("  ResetStyle = No" + "\n")
        file.write("  VarLoadMode = ByName" + "\n")
        file.write("  AssignStrandIDs = Yes" + "\n")
        file.write("  VarNameList = '\"X\" \"Y\" \"VALUE\"'" + "\n")
        file.write("$!ExtendedCommand " + "\n")
        file.write("  CommandProcessorID = 'Extract Precise Line'" + "\n")
        file.write(
            "  Command = 'XSTART = " + str(start_x) + " YSTART = " + str(start_y) +
            " ZSTART = 0 XEND = " + str(end_x) + " YEND = " + str(
                end_y) + " ZEND = 0 NUMPTS = " + str(
                count) + " EXTRACTTHROUGHVOLUME = F EXTRACTTOFILE = T EXTRACTFILENAME = "
                         "\\'E:\Codefield\Code_python\Digitalcell\Couplon_New\\tecplot_extract\\" +
            tecplot_path + "\\extract_files\\Gn_" + a + ".dat\\' '" + "\n")

