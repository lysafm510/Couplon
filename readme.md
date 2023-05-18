### 1. core 程序核心
每模拟一次可以在core下复制不同的包  
couplon.py 为程序入口，执行此文件即可  
参数调整在 constant.py 中

### 2. parameters 
`grid` 网格文件  
`triangle_number` 计算过程中存放的中间值，一次生成，多次使用

### 3. data 
存放模拟结果  

### 4. fonts 
使用matplotlib绘图的字体放在此目录下

### 5. utils
按顺序，先通过 `average` 生成每一步平均值  
然后再进行画图，可以使用matplotlib画，但建议使用tecplot软件画图，通过python程序生成tecplot特殊格式的.plt文件  
使用 `characteristic_parameter` 生成时间特征参数

### 6. figure
使用matplotlib绘图的结果放在此处

### 7. tecplot_data
使用tecplot软件导入的plt文件放在此处

### 8. tecplot_extract
绘制x时间-y直径的时间线扫描图
* 使用`6.1_generate_mcr_file.py`,制作mcr文件
* 打开tecplot-->Scripting-->Play Macro/Script,执行刚刚的mcr文件
* 执行`6.2_generate_dat_files.py`,将刚刚生成的批量提取值dat文件集成一个总的dat文件
* 使用tecplot导入刚刚的dat文件,就是最后的时间线扫描图

