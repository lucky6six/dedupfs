'''
以字节为单位的仅dedup系统
'''

import hashlib
import os
import argparse

CHUNK_SIZE = 1024 * 4  # 4KB

def read_file_into_chunks(file_path, chunk_size=CHUNK_SIZE):
    """
    以块大小读取文件内容
    :param file_path: 文件路径
    :param chunk_size: 块大小，默认 4KB
    :return: 逐块返回数据
    """
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            # 如果最后一块的大小小于块大小，舍去
            if len(chunk) < chunk_size:
                break
            
            yield chunk

def compute_block_hash(chunk):
    """
    计算块数据的哈希值 (例如使用 SHA-256)
    :param chunk: 块数据
    :return: 块的哈希值
    """
    return hashlib.sha256(chunk).hexdigest()

def simulate_deduplication_zfs(directories, chunk_size=CHUNK_SIZE):
    """
    模拟多个文件夹的块级去重策略，并按字节计算去重率
    :param directories: 文件夹路径列表
    :param chunk_size: 块大小
    :return: ZFS 风格的去重率
    """
    seen_blocks = set()  # 存储已见过的块
    total_bytes = 0      # 处理的字节总数 (相当于 ZFS 中的 ALLOC)
    unique_bytes = 0     # 唯一字节数 (相当于 ZFS 中的 DEDUP)

    # 遍历每个文件夹
    for directory in directories:
        print(f"Processing directory: {directory}")
        
        # 使用 os.walk 遍历目录及其子目录
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                
                # 对文件进行块级读取和去重
                for chunk in read_file_into_chunks(file_path, chunk_size):
                    # chunk_size = len(chunk)  # 获取当前块的字节数
                    chunk_size = CHUNK_SIZE
                    total_bytes += chunk_size  # ALLOC 增加字节数
                    
                    chunk_hash = compute_block_hash(chunk)
                    
                    # 如果该块的哈希值未出现过，进行去重
                    if chunk_hash not in seen_blocks:
                        seen_blocks.add(chunk_hash)
                        unique_bytes += chunk_size  # DEDUP 增加字节数

    # 计算 ZFS 风格的去重率：ALLOC 字节数 / DEDUP 字节数
    deduplication_rate = total_bytes / unique_bytes if unique_bytes else 0
    return deduplication_rate, total_bytes, unique_bytes

def main():
    # 假设我们有多个文件夹需要处理
    parser = argparse.ArgumentParser(description="接受一个文件目录并列出其中的文件。") 
    # 接受一个目录路径参数
    parser.add_argument("directory", type=str, help="要处理的目录路径")
    args = parser.parse_args()
    directories = [args.directory]
    # directories = ['mini-art-version1','mini-art-based1']
    # directories = ['gdb-code']
    
    # 调用去重模拟
    dedup_rate, total_bytes, unique_bytes = simulate_deduplication_zfs(directories)

    # 输出结果
    print(f"Total bytes processed (ALLOC): {total_bytes}")
    print(f"Unique bytes after deduplication (DEDUP): {unique_bytes}")
    print(f"ZFS-like deduplication rate (ALLOC / DEDUP): {dedup_rate:.2f}")

if __name__ == "__main__":
    main()
