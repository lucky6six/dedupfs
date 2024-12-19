import os
import random
import string
import struct
import difflib

# 配置常量
CHUNK_SIZE = 4 * 1024  # 4KB
FILE_SIZE = 1 * 1024 * 1024  # 1MB
NUM_CHUNKS = FILE_SIZE // CHUNK_SIZE # 
NUM_VERSIONS = 17  # 数据集的版本数量
SELECTED_BLOCKS = NUM_CHUNKS // 4  # 选择 1/4 的块，即 8192/128 个块
MODIFY_SIZE = 1024  # 每个选中块中修改 1KB 数据
DATASET_DIR = "mini-art-based1"  # 数据集保存路径

# 创建一个目录用于存储生成的文件
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

# 生成一个随机的ASCII字符串
def generate_random_ascii(size):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=size))

# 创建初始版本（全随机 ASCII 字符填充的文件）
def create_initial_version():
    file_data = generate_random_ascii(FILE_SIZE)
    with open(os.path.join(DATASET_DIR, "version_1.bin"), "w") as f:
        f.write(file_data)

# 拆分文件为块
def split_into_chunks(filename):
    with open(filename, "rb") as f:
        file_data = f.read()
    
    chunks = []
    for i in range(0, len(file_data), CHUNK_SIZE):
        chunks.append(file_data[i:i + CHUNK_SIZE])
    
    return chunks

# 修改某个块中的 1KB 数据为随机 ASCII 字符
def modify_chunk(chunk):
    start = random.randint(0, len(chunk) - MODIFY_SIZE)
    modified_chunk = chunk[:start] + generate_random_ascii(MODIFY_SIZE).encode() + chunk[start + MODIFY_SIZE:]
    return modified_chunk

# def compute_difference(chunk1, chunk2):
#     diff = difflib.SequenceMatcher(None, chunk1, chunk2)
#     diff_size = int((1-diff.ratio()) * CHUNK_SIZE)
#     return diff_size

def compute_difference(chunk1, chunk2):
    """
    计算两个数据块之间的差异字节数
    :param chunk1: 第一个数据块
    :param chunk2: 第二个数据块
    :return: 差异的字节数
    """

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
    print(common_prefix_len, common_suffix_len, diff_size)
    return diff_size


# 创建新版本的文件
def create_new_version(version_number, previous_version_file):
    chunks = split_into_chunks(previous_version_file)
    
    selected_chunk_indexes = random.sample(range(NUM_CHUNKS), SELECTED_BLOCKS)
    print(selected_chunk_indexes)
    for index in selected_chunk_indexes:
        a = modify_chunk(chunks[index])
        print(compute_difference(chunks[index], a))
        chunks[index] = a
    
    # 合并所有块并保存为新的版本文件
    new_version_data = b''.join(chunks)
    with open(os.path.join(DATASET_DIR, f"version_{version_number}.bin"), "wb") as f:
        f.write(new_version_data)

# 主函数
def generate_backup_artificial_dataset():
    # 生成初始版本
    create_initial_version()
    
    # 生成后续版本
    for version in range(2, NUM_VERSIONS + 1):
        previous_version_file = os.path.join(DATASET_DIR, f"version_1.bin")
        create_new_version(version, previous_version_file)
        print(f"Version {version} created.")

# 运行脚本
if __name__ == "__main__":
    generate_backup_artificial_dataset()
    print("Backup-Artificial dataset has been generated.")
