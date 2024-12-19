'''
以块为单位统计，仅有dedup功能的最初模拟。
'''
import hashlib
import os

def read_file_in_chunks(file_path, chunk_size=4096):
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
            yield chunk

def compute_block_hash(chunk):
    """
    计算块数据的哈希值（例如使用 SHA-256）
    :param chunk: 块数据
    :return: 块的哈希值
    """
    return hashlib.sha256(chunk).hexdigest()

def simulate_deduplication(directories, chunk_size=4096):
    """
    模拟多个文件夹的块级去重策略
    :param directories: 文件夹路径列表
    :param chunk_size: 块大小
    :return: ZFS 风格的去重率
    """
    seen_blocks = set()  # 存储已见过的块
    total_blocks = 0      # 处理的块总数 (相当于 ZFS 中的 ALLOC)
    unique_blocks = 0     # 唯一块数 (相当于 ZFS 中的 DEDUP)

    # 遍历每个文件夹
    for directory in directories:
        print(f"Processing directory: {directory}")
        
        # 使用 os.walk 遍历目录及其子目录
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                
                # 对文件进行块级读取和去重
                for chunk in read_file_in_chunks(file_path, chunk_size):
                    total_blocks += 1  # ALLOC 增加
                    chunk_hash = compute_block_hash(chunk)
                    
                    # 如果该块的哈希值未出现过，进行去重
                    if chunk_hash not in seen_blocks:
                        seen_blocks.add(chunk_hash)
                        unique_blocks += 1  # DEDUP 增加

    # 计算 ZFS 风格的去重率
    deduplication_rate = total_blocks / unique_blocks if unique_blocks else 0
    return deduplication_rate, total_blocks, unique_blocks

def main():
    # 假设我们有多个文件夹需要处理
    directories = ['gdb-15','gdb-15.2']
    
    # 调用去重模拟
    dedup_rate, total_blocks, unique_blocks = simulate_deduplication(directories)

    # 输出结果
    print(f"Total blocks processed (ALLOC): {total_blocks}")
    print(f"Unique blocks after deduplication (DEDUP): {unique_blocks}")
    print(f"ZFS-like deduplication rate (ALLOC / DEDUP): {dedup_rate:.2f}")

if __name__ == "__main__":
    main()
