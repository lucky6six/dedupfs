

import hashlib
import os
import time

CHUNK_SIZE = 1024 * 8  # 4KB

# 存储文件块的原始数据
block_storage = {}
block_simhash_storage = {}
sf_to_block = {}

def read_file_into_chunks(file_path, chunk_size=CHUNK_SIZE):
    """
    以块大小读取文件内容，并对最后一块进行填充（如果小于块大小）
    :param file_path: 文件路径
    :param chunk_size: 块大小，默认 4KB
    :return: 逐块返回数据
    """
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            
            # 如果最后一块的大小小于块大小，进行填充
            if len(chunk) < chunk_size:
                chunk = chunk.ljust(chunk_size, b'\0')  # 填充零
            
            yield chunk

def compute_block_hash(chunk):
    """
    计算块数据的哈希值 (例如使用 SHA-256)
    :param chunk: 块数据
    :return: 块的哈希值
    """
    return hashlib.sha256(chunk).hexdigest()

def super_features(chunk):
    num_chunks = 12
    chunk_features = []
    chunk_size = CHUNK_SIZE // num_chunks
    for i in range(num_chunks):
        # 计算每个子块的起始和结束位置
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_chunks - 1 else CHUNK_SIZE
        
        # 获取当前子块
        sub_chunk = chunk[start:end]
        
        # 在当前子块内应用滑动窗口来计算哈希值
        min_hash = float('inf')  # 用于记录当前子块的最小哈希值
        
        window_size = 8  # 假设滑动窗口大小为8个字节
        for j in range(len(sub_chunk) - window_size + 1):
            window = sub_chunk[j:j + window_size]  # 当前滑动窗口的数据
            window_hash = compute_block_hash(window)# 计算当前窗口的哈希值
            window_hash = int(window_hash, 16)      # 将哈希值转换为整数
            # 更新最大哈希值
            if window_hash < min_hash:
                min_hash = window_hash
            
        # 将该子块的最大哈希值作为特征
        chunk_features.append(str(min_hash))
        
    high_sp = ""
    mid_sp = ""
    low_sp = ""
    for i in range(0,9,3):  # 保证每次获取3个元素
        # 取出三个连续的字符串
        a, b, c = chunk_features[i], chunk_features[i + 1], chunk_features[i + 2]

        # 使用 sorted() 排序三元组，返回从小到大的顺序
        sorted_values = sorted([a, b, c])
        
        # 将排序后的值拼接成字符串，直接加入 low_sp, mid_sp, high_sp
        low_sp += sorted_values[0]   # 最小的值
        mid_sp += sorted_values[1]   # 中间的值
        high_sp += sorted_values[2]  # 最大的值
    sf1 = compute_block_hash(low_sp.encode('utf-8'))
    sf2 = compute_block_hash(mid_sp.encode('utf-8'))
    sf3 = compute_block_hash(high_sp.encode('utf-8'))
    yield sf1, sf2, sf3

def compute_difference(chunk1, chunk2):
    """
    计算两个数据块之间的差异字节数
    :param chunk1: 第一个数据块
    :param chunk2: 第二个数据块
    :return: 差异的字节数
    """
    diff_size = 0
    # 遍历两个块的字节，找出不同的字节
    for b1, b2 in zip(chunk1, chunk2):
        if b1 != b2:
            diff_size += 1
    
    # 如果块大小不同（即填充的零），则加上额外的差异字节数
    # diff_size += abs(len(chunk1) - len(chunk2))
    
    return diff_size

def simulate_deduplication_zfs(directories, chunk_size=CHUNK_SIZE):
    """
    模拟多个文件夹的块级去重策略，并按字节计算去重率
    :param directories: 文件夹路径列表
    :param chunk_size: 块大小
    :return: ZFS 风格的去重率
    """
    global block_storage
    global block_simhash_storage
    seen_blocks = set()  # 存储已见过的块的哈希值
    total_bytes = 0      # 处理的字节总数 (相当于 ZFS 中的 ALLOC)
    unique_bytes = 0     # 唯一字节数 (相当于 ZFS 中的 DEDUP)
    modified_bytes = 0   # 修改字节数，用于模拟增量存储

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
                    chunk_size = CHUNK_SIZE  # 获取当前块的字节数
                    total_bytes += chunk_size  # ALLOC 增加字节数
                    
                    chunk_hash = compute_block_hash(chunk)
             
                    # 如果块已存在并且是相同的，则跳过
                    if chunk_hash in seen_blocks:
                        continue
                    # 查找相似块
                    flag = False
                    block_super_features = {}
                    for item_sf in super_features(chunk):   
                        if item_sf in sf_to_block:
                                ref_chunk = sf_to_block[item_sf]
                                diff_size = compute_difference(chunk, ref_chunk)
                                modified_bytes += diff_size
                                flag = True
                                break
                        block_super_features[item_sf] = chunk
                    
                    if flag:
                        continue
                    # 如果该块没有相似块，认为它是唯一的块，增加唯一字节数
                    seen_blocks.add(chunk_hash)
                    unique_bytes += chunk_size  # DEDUP 增加字节数
                    
                    # 存储该块数据，并标记为新块
                    block_storage[chunk_hash] = chunk
                    # 存储 Sf 值
                    for sf in block_super_features:
                        sf_to_block[sf] = block_super_features[sf]

    # 计算 ZFS 风格的去重率：ALLOC 字节数 / DEDUP 字节数
    deduplication_rate = total_bytes / unique_bytes if unique_bytes else 0
    # 计算增量存储的去重率
    deduplication_rate_delta = total_bytes / (unique_bytes + modified_bytes) if unique_bytes else 0
    return deduplication_rate, total_bytes, unique_bytes, modified_bytes, deduplication_rate_delta

def main():
    # 假设我们有多个文件夹需要处理
    directories = ['mini-test']
    
    start_time = time.time()
    # 调用去重模拟
    dedup_rate, total_bytes, unique_bytes, modified_bytes, dedup_rate_delta = simulate_deduplication_zfs(directories)
    # 获取当前时间
    end_time = time.time()

    # 计算时间差
    elapsed_time = end_time - start_time
    print(f"代码执行时间: {elapsed_time} 秒")

    # 输出结果
    print(f"Total bytes processed (ALLOC): {total_bytes}")
    print(f"Unique bytes after deduplication (DEDUP): {unique_bytes}")
    # print(f"Deduplication rate: {dedup_rate:.2f}")
    print(f"Modified bytes (for incremental storage): {modified_bytes}")
    print(f"Delta Deduplication rate (for incremental storage): {dedup_rate_delta:.2f}")

if __name__ == "__main__":
    main()
