

import hashlib
import os
import difflib
import time
# import xxhash
import argparse

CHUNK_SIZE = 1024 * 8  # 4KB

# 存储文件块的原始数据
block_storage = {}
block_simhash_storage = {}
sf_to_block = {}
time_diff = 0

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

def super_features(chunk):
    num_chunks = 12
    chunk_features = []
    chunk_size = CHUNK_SIZE // num_chunks
    prime = 2**63 - 1
    for i in range(num_chunks):
        # 计算每个子块的起始和结束位置
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_chunks - 1 else CHUNK_SIZE
        # 获取当前子块
        sub_chunk = chunk[start:end]
        # 在当前子块内应用滑动窗口来计算哈希值
        min_hash = float('inf')  # 用于记录当前子块的最小哈希值
        window_size = 80  # 假设滑动窗口大小为8个字节
        
        # 滑动窗口的哈希值
        current_hash = 0
        for i in range(window_size):
            current_hash = (current_hash * 257 + sub_chunk[i])  % prime # 滚动更新哈希
        
        # 初始哈希值
        min_hash = min(min_hash, current_hash)
        
        # 递归滚动窗口计算哈希值，避免重复计算
        for j in range(1, len(sub_chunk) - window_size + 1):
            # 滚动窗口: 移除第一个字符，加入下一个字符
            # current_hash = (current_hash * 257 + sub_chunk[j + window_size - 1] - sub_chunk[j - 1] * 257**window_size)
            current_hash = (current_hash - sub_chunk[i - 1] * 257) * 257 + sub_chunk[i + window_size - 1] 
            current_hash = current_hash % prime
            min_hash = min(min_hash, current_hash)
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
        # print(sorted_values)
        # 将排序后的值拼接成字符串，直接加入 low_sp, mid_sp, high_sp
        low_sp += sorted_values[0]   # 最小的值
        mid_sp += sorted_values[1]   # 中间的值
        high_sp += sorted_values[2]  # 最大的值
    # print(low_sp, mid_sp, high_sp)
    sf1 = compute_block_hash(low_sp.encode())
    sf2 = compute_block_hash(mid_sp.encode())
    sf3 = compute_block_hash(high_sp.encode())
    # print(sf1, sf2, sf3)
    return sf1, sf2, sf3

def compute_difference(chunk1, chunk2):
    """
    计算两个数据块之间的差异字节数
    :param chunk1: 第一个数据块
    :param chunk2: 第二个数据块
    :return: 差异的字节数
    """
    global time_diff
    # diff_size = 0
    # # 遍历两个块的字节，找出不同的字节
    # for b1, b2 in zip(chunk1, chunk2):
    #     if b1 != b2:
    #         diff_size += 1
    
    # 如果块大小不同（即填充的零），则加上额外的差异字节数
    # diff_size += abs(len(chunk1) - len(chunk2))
    start_time = time.time()

    diff = difflib.SequenceMatcher(None, chunk1, chunk2)
    diff_size = int((1-diff.ratio()) * CHUNK_SIZE)
     # 获取当前时间
    end_time = time.time()

    # 计算时间差
    elapsed_time = end_time - start_time
    time_diff += elapsed_time
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
    global sf_to_block
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
                    total_bytes += chunk_size  # ALLOC 增加字节数
                    
                    chunk_hash = compute_block_hash(chunk)
             
                    # 如果块已存在并且是相同的，则跳过
                    if chunk_hash in seen_blocks:
                        continue
                    # 查找相似块
                    flag = False
                    block_super_features = {}
                    for item_sf in super_features(chunk):  
                        # print(sf_to_block) 
                        
                        if item_sf in sf_to_block:
                                ref_chunk = sf_to_block[item_sf]
                                # print(item_sf)
                                diff_size = compute_difference(chunk, ref_chunk)
                                print(diff_size)
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
                        # print(sf)

    # 计算 ZFS 风格的去重率：ALLOC 字节数 / DEDUP 字节数
    deduplication_rate = total_bytes / unique_bytes if unique_bytes else 0
    # 计算增量存储的去重率
    deduplication_rate_delta = total_bytes / (unique_bytes + modified_bytes) if unique_bytes else 0
    return deduplication_rate, total_bytes, unique_bytes, modified_bytes, deduplication_rate_delta

def main():
    parser = argparse.ArgumentParser(description="接受一个文件目录并列出其中的文件。") 
    # 接受一个目录路径参数
    parser.add_argument("directory", type=str, help="要处理的目录路径")
    args = parser.parse_args()
    directories = [args.directory]
    # directories = ['mini-art-version1','mini-art-based1']
    # # 假设我们有多个文件夹需要处理
    # directories = ['mini-test']
    
    start_time = time.time()
    # 调用去重模拟
    dedup_rate, total_bytes, unique_bytes, modified_bytes, dedup_rate_delta = simulate_deduplication_zfs(directories)
    # 获取当前时间
    end_time = time.time()

    # 计算时间差
    elapsed_time = end_time - start_time
    print(f"代码执行时间: {elapsed_time} 秒")
    print(f"计算时间: {time_diff} 秒")
    # 输出结果
    print(f"Total bytes processed (ALLOC): {total_bytes}")
    print(f"Unique bytes after deduplication (DEDUP): {unique_bytes}")
    # print(f"Deduplication rate: {dedup_rate:.2f}")
    print(f"Modified bytes (for incremental storage): {modified_bytes}")
    print(f"Delta Deduplication rate (for incremental storage): {dedup_rate_delta:.2f}")

if __name__ == "__main__":
    main()
