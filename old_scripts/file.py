import hashlib
import os
import difflib

CHUNK_SIZE = 1024 * 4  # 4KB

# 存储文件块的原始数据
block_storage = {}

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

def find_similar_block(chunk, threshold=0.1):
    """
    查找与当前块相似的已存储块，返回相似块的哈希值和差异字节数
    :param chunk: 当前块数据
    :param threshold: 相似度阈值，0-1之间。默认为0.1，表示差异小于10%认为是相似的
    :return: 相似块的哈希值和差异字节数，如果找到相似块，则返回哈希值和差异字节数，否则返回None和0
    """
    # return None, 0
    for stored_hash, stored_chunk in block_storage.items():
        # 计算两个块之间的差异
        diff_size = compute_difference(chunk, stored_chunk)
        
        # 如果差异字节数小于阈值，认为是相似的块
        
        if diff_size / CHUNK_SIZE < threshold:
            return stored_hash, diff_size  # 返回相似块的哈希值和差异字节数
    
    return None, 0

def simulate_deduplication_zfs(directories, chunk_size=CHUNK_SIZE):
    """
    模拟多个文件夹的块级去重策略，并按字节计算去重率
    :param directories: 文件夹路径列表
    :param chunk_size: 块大小
    :return: ZFS 风格的去重率
    """
    global block_storage
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
                    similar_hash, diff_size = find_similar_block(chunk)
                    
                    # 如果相似块存在且差异较小，认为它是相似块，增加修改字节数
                    if similar_hash:
                        # print(f"Found similar block (hash: {similar_hash}, diff size: {diff_size} bytes)")
                        modified_bytes += diff_size
                    else:
                        # 如果该块没有相似块，认为它是唯一的块，增加唯一字节数
                        seen_blocks.add(chunk_hash)
                        unique_bytes += chunk_size  # DEDUP 增加字节数
                        
                        # 存储该块数据，并标记为新块
                        block_storage[chunk_hash] = chunk

    # 计算 ZFS 风格的去重率：ALLOC 字节数 / DEDUP 字节数
    deduplication_rate = total_bytes / unique_bytes if unique_bytes else 0
    # 计算增量存储的去重率
    deduplication_rate_delta = total_bytes / (unique_bytes + modified_bytes) if unique_bytes else 0
    return deduplication_rate, total_bytes, unique_bytes, modified_bytes, deduplication_rate_delta

def main():
    # 假设我们有多个文件夹需要处理
    directories = ['gdb-15']
    
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
