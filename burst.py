

import hashlib
import os
import difflib
import argparse
import time
# import xxhash

CHUNK_SIZE = 1024 * 4  # 4KB
HT_SIZE = CHUNK_SIZE // 4

# 存储文件块的原始数据
block_storage = {}
# block_simhash_storage = {}
# sf_to_block = {}
hhash_to_block = {}
thash_to_block = {}
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

def hthash(chunk):
    hhash = hashlib.sha256(chunk[0:HT_SIZE]).hexdigest()
    thash = hashlib.sha256(chunk[CHUNK_SIZE-HT_SIZE:CHUNK_SIZE]).hexdigest()
    return hhash, thash

# def super_features(chunk):
#     num_chunks = 12
#     chunk_features = []
#     chunk_size = CHUNK_SIZE // num_chunks
#     for i in range(num_chunks):
#         # 计算每个子块的起始和结束位置
#         start = i * chunk_size
#         end = (i + 1) * chunk_size if i != num_chunks - 1 else CHUNK_SIZE
#         # 获取当前子块
#         sub_chunk = chunk[start:end]
#         # 在当前子块内应用滑动窗口来计算哈希值
#         min_hash = float('inf')  # 用于记录当前子块的最小哈希值
#         window_size = 8  # 假设滑动窗口大小为8个字节
        
#         # 滑动窗口的哈希值
#         current_hash = 0
#         # 使用 XXHash 计算初始窗口的哈希值
#         for i in range(window_size):
#             current_hash = (current_hash * 257 + sub_chunk[i])  # 滚动更新哈希
        
#         # 初始哈希值
#         min_hash = min(min_hash, current_hash)
        
#         # 递归滚动窗口计算哈希值，避免重复计算
#         for j in range(1, len(sub_chunk) - window_size + 1):
#             # 滚动窗口: 移除第一个字符，加入下一个字符
#             current_hash = (current_hash * 257 + sub_chunk[j + window_size - 1] - sub_chunk[j - 1] * 257**window_size)
#             min_hash = min(min_hash, current_hash)
#         # 将该子块的最大哈希值作为特征
#         chunk_features.append(str(min_hash))
        
#     high_sp = ""
#     mid_sp = ""
#     low_sp = ""
#     for i in range(0,9,3):  # 保证每次获取3个元素
#         # 取出三个连续的字符串
#         a, b, c = chunk_features[i], chunk_features[i + 1], chunk_features[i + 2]

#         # 使用 sorted() 排序三元组，返回从小到大的顺序
#         sorted_values = sorted([a, b, c])
        
#         # 将排序后的值拼接成字符串，直接加入 low_sp, mid_sp, high_sp
#         low_sp += sorted_values[0]   # 最小的值
#         mid_sp += sorted_values[1]   # 中间的值
#         high_sp += sorted_values[2]  # 最大的值
#     sf1 = compute_block_hash(low_sp.encode('utf-8'))
#     sf2 = compute_block_hash(mid_sp.encode('utf-8'))
#     sf3 = compute_block_hash(high_sp.encode('utf-8'))
#     return sf1, sf2, sf3



def compute_difference(chunk1, chunk2):
    """
    计算两个数据块之间的差异字节数
    :param chunk1: 第一个数据块
    :param chunk2: 第二个数据块
    :return: 差异的字节数
    """
    global time_diff
    start_time = time.time()
    
    # 1. 计算公共前缀长度
    common_prefix_len = 0
    while common_prefix_len < CHUNK_SIZE and chunk1[common_prefix_len] == chunk2[common_prefix_len]:
        common_prefix_len += 1
    
    # 2. 计算公共后缀长度
    common_suffix_len = 0
    while common_suffix_len < CHUNK_SIZE - common_prefix_len and chunk1[CHUNK_SIZE - common_suffix_len - 1] == chunk2[CHUNK_SIZE - common_suffix_len - 1]:
        common_suffix_len += 1
    
    # 3. 计算去除公共前缀和公共后缀后的非公共部分大小,即burst大小
    diff_size = CHUNK_SIZE - common_prefix_len - common_suffix_len
    
     # 获取当前时间
    end_time = time.time()
    # 计算时间差
    elapsed_time = end_time - start_time
    time_diff += elapsed_time
    print(common_prefix_len, common_suffix_len, diff_size)
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
                    hhash,thash = hthash(chunk)
                    if hhash in hhash_to_block:
                        ref_chunk = hhash_to_block[hhash]
                        diff_size = compute_difference(chunk, ref_chunk)
                        # print(diff_size)
                        modified_bytes += diff_size
                        flag = True
                    if thash in thash_to_block and not flag:
                        ref_chunk = thash_to_block[thash]
                        diff_size = compute_difference(chunk, ref_chunk)
                        modified_bytes += diff_size
                        flag = True
                    
                    if flag:
                        continue
                    # 如果该块没有相似块，认为它是唯一的块，增加唯一字节数
                    seen_blocks.add(chunk_hash)
                    unique_bytes += chunk_size  # DEDUP 增加字节数
                    
                    # 存储该块数据，并标记为新块
                    block_storage[chunk_hash] = chunk
                    # 存储 h / t
                    hhash_to_block[hhash] = chunk
                    thash_to_block[thash] = chunk


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
