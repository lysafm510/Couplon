path = "8_25通道_咖啡因_入流量0"

with open("../tecplot_extract/" + path + "/" + path + ".dat", "w") as file:
    num_y = 501
    idx = []
    with open("../tecplot_extract/" + path + "/extract_files/Gn_00000000.dat", "r") as file2:
        for i in file2.readlines()[5:]:
            idx.append(i.strip().split()[0])
    file2.close()
    num_x = len(idx)
    print(num_x)

    file.write('TITLE = "WRITE BY LYS"\n')
    file.write('VARIABLES="X","Y","Value" \n')
    file.write('DATASETAUXDATA Common.VectorVarsAreVelocity = "TRUE"\n')
    file.write('ZONE T = "Peaks"\n')
    file.write(' STRANDID = 1, SOLUTIONTIME = 0\n')
    # numx和numy分别是X，Y坐标的点数
    file.write(
        ' Nodes = {}, Elements = {}, ZONETYPE = FEQuadrilateral\n'.format(num_x * num_y, (num_x - 1) * (num_y - 1)))
    file.write(' DATAPACKING = POINT\n')
    file.write(' DT = (SINGLE SINGLE SINGLE)\n')

    for i in range(0, 501):
        a = str(i * 100).zfill(8)
        b = i * 0.2

        x = []
        y = []
        value = []
        with open("../tecplot_extract/" + path + "/extract_files/Gn_" + a + ".dat", "r") as file1:
            for i in file1.readlines()[5:]:
                y.append(i.strip().split()[0])
                x.append(str(b))
                value.append(i.strip().split()[2])
        file1.close()

        for i in range(len(x)):
            file.write(x[i] + "\t" + y[i] + "\t" + value[i] + "\n")

    for j in range(1, num_y):
        for i in range(1, num_x):
            file.write(
                '{} {} {} {}\n'.format(num_x * j + i, num_x * (j - 1) + i, num_x * (j - 1) + i + 1, num_x * j + i + 1))
