import subprocess
import os
import time
import argparse

def run_fs_script(directory, file_type, block_size_kb, head_rate=None,is_detect=False):
    """
    运行 fs.py 脚本并传递命令行参数，同时捕获输出并写入文件。
    
    :param directory: 要处理的目录路径
    :param file_type: 文件系统类型，dedup, burst, fin 等
    :param block_size_kb: 以 KB 为单位的块大小
    :param head_rate: 块的头部大小占比，1/n。默认为 None，表示不传递该参数
    """
    command = ["python3", "fs.py", "-d", directory, "-t", file_type, "-b", str(block_size_kb)]

    if head_rate:
        command.extend(["-r", str(head_rate)])
    if is_detect:
        command.extend(["-i"])
    # 打印并执行命令，同时捕获输出
    print(f"Running command: {' '.join(command)}")
    
    # 捕获命令的输出
    result = subprocess.run(command, capture_output=True, text=True)

    # 捕获输出并保存到文件
    output = result.stdout
    save_output_to_file(directory, file_type, block_size_kb, head_rate, output,is_detect)

def save_output_to_file(directory, file_type, block_size_kb, head_rate, output,is_detect=False):
    """
    将输出结果保存到文件，按指定格式命名文件，并存放在 result 文件夹下。
    
    :param directory: 文件目录
    :param file_type: 文件类型
    :param block_size_kb: 块大小
    :param head_rate: 头部大小占比
    :param output: fs.py 的输出内容
    """
    # 创建 result 文件夹（如果不存在的话）
    dir =  "result_" + directory 
    if not os.path.exists(dir):
        os.makedirs(dir)

    # 设置文件保存路径
    output_file = f"{dir}/{directory}_{file_type}_{block_size_kb}KB.txt"
    
    if head_rate:
        output_file = f"{dir}/{directory}_{file_type}_{block_size_kb}KB_{head_rate}.txt"
    if is_detect:
        output_file = f"{dir}/{directory}_{file_type}_{block_size_kb}KB_{head_rate}_detect.txt"
    # 写入文件
    with open(output_file, 'w') as f:
        f.write(output)
    
    print(f"Output saved to: {output_file}")

def get_parser():
    parser = argparse.ArgumentParser(description="接受一个文件目录并列出其中的文件。") 
    # 接受一个目录路径参数
    parser.add_argument('-d','--directory', type=str, required=True,help="要处理的目录路径")
    parser.add_argument('-c','--clear',  action='store_true', help="清空目录")
    return parser

def main():
    #推荐数据集
    '''
    8KB块
    toolcode:  gdb gcc openjdk nodejs各版本
    lnxk linux kernel 各版本源码
    lnxtar linux kernel 各版本源码tar包
    vmi 虚拟机镜像
    web httrack下载的网站
    sim  synthetic backups by simulating  file create/delete/modify operations
    '''
    
    
    # 设置不同的参数组合
    directories = ["sim","sim_base1","toolcode","vmi","webh","lnxk","lnxtar"]
    blocksize = [4,8,16,128]
    # head_rate = [4,8,16]
    start_time = time.time()
    parser = get_parser()
    args = parser.parse_args()
    if args.clear:
        subprocess.run(["rm", "-rf", "result"])
        return
    directory = args.directory
    run_fs_script(directory, file_type="dedup", block_size_kb=8)
    run_fs_script(directory, file_type="burst", block_size_kb=8, head_rate=8)
    run_fs_script(directory, file_type="burst", block_size_kb=8, head_rate=8,is_detect=True)
    run_fs_script(directory, file_type="fin", block_size_kb=8)
    
    # for directory in directories:
    #     for block in blocksize:
    #         run_fs_script(directory, file_type="dedup", block_size_kb=block)
    #         run_fs_script(directory, file_type="burst", block_size_kb=block, head_rate=8)
    #         run_fs_script(directory, file_type="burst", block_size_kb=block, head_rate=8,is_detect=True)
    #         run_fs_script(directory, file_type="fin", block_size_kb=block)
    
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()