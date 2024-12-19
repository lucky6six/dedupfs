'''
使用simhash进行特征表示,距离计算相似度，最初的最慢的增量压缩版本
'''

import hashlib
import os
import difflib

CHUNK_SIZE = 1024 * 4  # 4KB

# 存储文件块的原始数据
block_storage = {}
block_simhash_storage = {}

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
            
            # # 如果最后一块的大小小于块大小，进行填充
            # if len(chunk) < chunk_size:
            #     chunk = chunk.ljust(chunk_size, b'\0')  # 填充零
            
            yield chunk

def compute_block_hash(chunk):
    """
    计算块数据的哈希值 (例如使用 SHA-256)
    :param chunk: 块数据
    :return: 块的哈希值
    """
    return hashlib.sha256(chunk).hexdigest()


# SimHash 实现
def sim_hash(chunk, hash_bits=64):
    """
    计算给定数据块的 SimHash。
    :param chunk: 数据块
    :param hash_bits: 哈希值位数
    :return: 计算得到的 SimHash 值
    """
    # 初始化一个空的位向量
    bit_vector = [0] * hash_bits
    
    # 将数据块按每 8 字节分块，进行哈希计算
    for i in range(0, len(chunk), 8):
        part = chunk[i:i+8]
        # 使用 MD5 作为简单的哈希函数
        part_hash = int(hashlib.md5(part).hexdigest(), 16)
        
        # 更新位向量，查看每一位是 1 还是 0
        for j in range(hash_bits):
            if (part_hash >> j) & 1:
                bit_vector[j] += 1
            else:
                bit_vector[j] -= 1
    
    # 根据位向量最终生成 SimHash
    final_hash = 0
    for i in range(hash_bits):
        if bit_vector[i] > 0:
            final_hash |= (1 << i)
    return final_hash


def hamming_distance(hash1, hash2):
    """
    计算两个哈希值之间的汉明距离。
    :param hash1: 第一个哈希值
    :param hash2: 第二个哈希值
    :return: 汉明距离
    """
    return bin(hash1 ^ hash2).count('1')


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

def find_similar_block(chunk, chunk_sim_hash ,threshold=10):
    """
    查找与当前块相似的已存储块，返回相似块的哈希值和差异字节数
    :param chunk: 当前块数据
    :param threshold: 相似度阈值，0-1之间。默认为0.1，表示差异小于10%认为是相似的
    :return: 相似块的哈希值和差异字节数，如果找到相似块，则返回哈希值和差异字节数，否则返回None和0
    """
    # 遍历所有存储的块，计算与其哈希值的汉明距离
    for stored_hash, ref_chunk in block_simhash_storage.items():
        distance = hamming_distance(chunk_sim_hash, stored_hash)
        # 如果汉明距离小于或等于阈值，则认为块相似
        if distance <= threshold:
            # print(f"Distance: {distance}")
            diff_size = compute_difference(chunk, ref_chunk)
            return diff_size  # 返回相似块的哈希值和差异字节数
    
    return 0

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
                    
                    chunk_sim_hash = sim_hash(chunk)
                    # 查找相似块
                    diff_size = find_similar_block(chunk,chunk_sim_hash)
                    
                    # 如果相似块存在且差异较小，认为它是相似块，增加修改字节数
                    if diff_size:
                        # print(f"Found similar block (hash: {similar_hash}, diff size: {diff_size} bytes)")
                        modified_bytes += diff_size
                    else:
                        # 如果该块没有相似块，认为它是唯一的块，增加唯一字节数
                        seen_blocks.add(chunk_hash)
                        unique_bytes += chunk_size  # DEDUP 增加字节数
                        
                        # 存储该块数据，并标记为新块
                        block_storage[chunk_hash] = chunk
                        block_simhash_storage[chunk_sim_hash] = chunk

    # 计算 ZFS 风格的去重率：ALLOC 字节数 / DEDUP 字节数
    deduplication_rate = total_bytes / unique_bytes if unique_bytes else 0
    # 计算增量存储的去重率
    deduplication_rate_delta = total_bytes / (unique_bytes + modified_bytes) if unique_bytes else 0
    return deduplication_rate, total_bytes, unique_bytes, modified_bytes, deduplication_rate_delta

def main():
    # 假设我们有多个文件夹需要处理
    directories = ['gdb-15','gdb-15.2']
    
    # 调用去重模拟
    dedup_rate, total_bytes, unique_bytes, modified_bytes, dedup_rate_delta = simulate_deduplication_zfs(directories)

    # 输出结果
    print(f"Total bytes processed (ALLOC): {total_bytes}")
    print(f"Unique bytes after deduplication (DEDUP): {unique_bytes}")
    print(f"Deduplication rate: {dedup_rate:.2f}")
    print(f"Modified bytes (for incremental storage): {modified_bytes}")
    print(f"Delta Deduplication rate (for incremental storage): {dedup_rate_delta:.2f}")

if __name__ == "__main__":
    main()
