import os

def modify_file(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 删除前5行和后2行
    if len(lines) > 7:  # 确保文件有足够的行数
        new_lines = lines[5:-2]
    else:
        new_lines = []  # 如果文件行数不够，清空文件
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def process_directory(directory):
    # 遍历目录及其子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # 只处理文件，忽略其他文件类型
            if os.path.isfile(file_path):
                modify_file(file_path)

# 示例：调用函数
directory = '/home/liuzhuo/dedupfs/webhttrack/news.sjtu.edu.cn'  # 替换为你的目录路径
process_directory(directory)


#scp -r liu@10.0.25.69:~/backup .
