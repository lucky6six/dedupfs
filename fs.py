

import hashlib
import os
import difflib
import time
# import xxhash
import argparse
import sys

size_per_chunk = 4 * 1024  # 4KB
type_of_fs = "dedup"
head_rate = 8
# 存储文件块的原始数据
# block_storage = {}
sf_to_block = {}
hhash_to_block = {}
thash_to_block = {}
time_diff = 0
time_feature = 0
is_detect = False

def read_file_into_chunks(file_path, chunk_size):
    """
    以块大小读取文件内容，并对最后一块进行舍去（如果小于块大小）
    :param file_path: 文件路径
    :param chunk_size: 块大小，默认 4KB
    :return: 逐块返回数据
    """
    # print(chunk_size)
    with open(file_path, 'rb') as file:
        while True:
            
            chunk = file.read(chunk_size)
            if not chunk:
                break
            # print(chunk)
            yield chunk,len(chunk)

def compute_block_hash(chunk):
    """
    计算块数据的哈希值 (例如使用 SHA-256)
    :param chunk: 块数据
    :return: 块的哈希值
    """
    return hashlib.sha256(chunk).hexdigest()

def get_finesse_super_feature_from_features(chunk_features):
    # print(chunk_features)
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
        low_sp += str(sorted_values[0])   # 最小的值
        mid_sp += str(sorted_values[1])# 中间的值
        high_sp += str(sorted_values[2])  # 最大的值
    # print(low_sp, mid_sp, high_sp)
    sf1 = compute_block_hash(low_sp.encode())
    sf2 = compute_block_hash(mid_sp.encode())
    sf3 = compute_block_hash(high_sp.encode())
    # print(sf1, sf2, sf3)
    return sf1, sf2, sf3

def get_finesse_super_feature(chunk,size):
    global time_feature
    start_time = time.time()
    subchunk_num = 12
    chunk_features = []
    subchunk_size = size // subchunk_num
    prime = 2**63 - 1
    for i in range(subchunk_num):
        # 计算每个子块的起始和结束位置
        start = i * subchunk_size
        end = (i + 1) * subchunk_size if i != subchunk_num - 1 else size
        # 获取当前子块
        sub_chunk = chunk[start:end]
        # 在当前子块内应用滑动窗口来计算哈希值
        min_hash = float('inf')  # 用于记录当前子块的最小哈希值
        window_size = subchunk_size//9 # 假设滑动窗口大小为8个字节
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
            # print(min_hash)
        # 将该子块的最大哈希值作为特征
        # print(chunk_features)
        chunk_features.append(str(min_hash))
        # time.sleep(100)
        # print(chunk_features)
    
    ret = get_finesse_super_feature_from_features(chunk_features)
    end_time = time.time()
    time_feature += end_time - start_time
    # print(ret)
    return ret

def get_gear_super_feature(chunk,size,window_size=4, mod_value=123456789):
    """
    动态调整阈值进行 Gear Hash 分块
    :param data: 输入数据（字节流或字符串）
    :param window_size: 窗口大小
    :param initial_threshold: 初始哈希阈值
    :param mod_value: 模值，用于限制哈希值的范围
    :return: 块的边界位置列表
    """
    # print("______________________________a block")
    def simple_gear_hash(data):
        # Gear Hash 通过简单的加法和位移来计算哈希值
        hash_val = 0
        for char in data:
            hash_val = (hash_val << 4) + char  # 左移5位后加上字符的ASCII值
            # hash_val = hash_val % mod_value  # 使用模运算避免哈希值无限增长
        return hash_val
    
    global time_feature
    start_time = time.time()

    current_hash = simple_gear_hash(chunk[:window_size])
    # print(current_hash)
    # 使用初始阈值
    threshold = 2**64
    # print(f"threshold: {threshold}")
    # count = 0
    sf = [float('inf'), float('inf'), float('inf'),float('inf'),float('inf'),float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf')]
    para = [[12345000123534513540001234,123450000001234],[98765003451452300009876,567895000000678],[12345000012341235004321,12300000034567],[1111111324211111111,12121212121212],[3333333398567833333,123321],[9898904563469879878,678],[1234567845687564123456,87],[234567765234535243,4567],[666466663453666666,345678],[987654323467223456,456],[2345376548676543,34],[987456386543123450,66]]
    for i in range(window_size, size):
        current_hash = (current_hash << 4) + chunk[i]  # 移位并加上字符ASCII值
        # current_hash = current_hash % mod_value  # 使用模运算保持哈希值在合理范围内
        # print(current_hash)
        # 如果哈希值小于阈值，认为是抽样
        if current_hash > threshold:
            # print(current_hash)
            # count += 1
            for j in range(12):
                trans = (para[j][0]*current_hash + para[j][1]) %(2**32)
                if(trans < sf[j]):
                    sf[j] = trans
            current_hash = 0
            # 动态调整阈值，例如根据当前的哈希值变化调整
            # threshold = (threshold + current_hash) // 2  # 取当前哈希值与上一个哈希值的平均值
    # time.sleep(100)
    # print(sf)
    
    ret = get_finesse_super_feature_from_features(sf)
    # print(ret)
    # print(count)
    end_time = time.time()
    time_feature += end_time - start_time
    # return sf[0],sf[1],sf[2],sf[3],sf[4],sf[5],sf[6],sf[7],sf[8],sf[9],sf[10],sf[11]
    return ret

def hthash(chunk,size):
    global time_feature
    start_time = time.time()
    ht_size = size // head_rate
    hhash = hashlib.sha256(chunk[0:ht_size]).hexdigest()
    thash = hashlib.sha256(chunk[size-ht_size:size]).hexdigest()
    end_time = time.time()
    time_feature += end_time - start_time
    return hhash, thash

def compute_difference_detla(chunk1, chunk2,size):
    """
    计算两个数据块之间的差异字节数
    :param chunk1: 第一个数据块
    :param chunk2: 第二个数据块
    :return: 差异的字节数
    """
    global time_diff
    start_time = time.time()
    diff = difflib.SequenceMatcher(None, chunk1, chunk2).ratio()
    diff_size = int((1-diff) * size)
     # 获取当前时间
    end_time = time.time()
    # 计算时间差
    ctime = end_time - start_time
    time_diff += ctime
    return diff_size

def compute_difference_burst(chunk1, chunk2):
    """
    计算两个数据块之间的差异字节数
    :param chunk1: 第一个数据块
    :param chunk2: 第二个数据块
    :return: 差异的字节数
    """
    global time_diff
    start_time = time.time()
    size1 = len(chunk1)
    size2 = len(chunk2)
    # if size1 < size2:
    #     chunk_tmp = chunk1
    #     chunk1 = chunk2
    #     chunk2 = chunk_tmp
    #     size_tmp = size1
    #     size1 = size2
    #     size2 = size_tmp
    # print(size1,size2)
    # 1. 计算公共前缀长度
    common_prefix_len = 0
    min_size = min(size1, size2)
    max_size = max(size1, size2)
    while common_prefix_len < min_size and chunk1[common_prefix_len] == chunk2[common_prefix_len]:
        common_prefix_len += 1
 
    # 2. 计算公共后缀长度
    common_suffix_len = 0
    reminder = min_size - common_prefix_len
    while common_suffix_len < reminder and chunk1[size1 - common_suffix_len - 1] == chunk2[size2 - common_suffix_len - 1]:
        common_suffix_len += 1
    # 3. 计算去除公共前缀和公共后缀后的非公共部分大小,即burst大小
    diff_size = max_size - common_suffix_len - common_prefix_len
    # print(diff_size,common_prefix_len,common_suffix_len)
     # 获取当前时间
    end_time = time.time()
    # 计算时间差
    elapsed_time = end_time - start_time
    time_diff += elapsed_time
    # print(common_prefix_len, common_suffix_len, diff_size)
    return diff_size

def simulate_deduplication(directory, chunk_size, type_of_fs):
    """
    模拟多个文件夹的块级去重策略，并按字节计算去重率
    :param directories: 文件夹路径列表
    :param chunk_size: 块大小
    :return: ZFS 风格的去重率
    """
    # global block_storage
    global sf_to_block
    global hhash_to_block
    global thash_to_block
    seen_blocks = set()  # 存储已见过的块的哈希值
    total_bytes = 0      # 处理的字节总数 (相当于 ZFS 中的 ALLOC)
    unique_bytes = 0     # 唯一字节数 (相当于 ZFS 中的 DEDUP)
    modified_bytes = 0   # 修改字节数，用于模拟增量存储
    for root, dirs, files in os.walk(directory):
        files.sort()
        dirs.sort()
        for file in files:
            file_path = os.path.join(root, file)
            # print(f"Processing file: {file_path}")
            # 对文件进行块级读取
            for chunk,size in read_file_into_chunks(file_path, chunk_size):
                # 如果块太小，忽略
                if size < 108:
                    continue
                total_bytes += size  # 增加alloc字节数
                # 如果块已存在并且是相同的，则跳过
                chunk_hash = compute_block_hash(chunk)
                if chunk_hash in seen_blocks:
                    continue
                # 查找相似块
                if(type_of_fs == "odess1"):
                    flag = False
                    sf_of_chunk = set()
                    
                    for item_sf in get_gear_super_feature(chunk,size):
                        if item_sf in sf_to_block:
                            ref_chunk = sf_to_block[item_sf]
                            # print(item_sf)
                            diff_size = compute_difference_detla(chunk, ref_chunk,size)
                            # print(diff_size)
                            modified_bytes += diff_size
                            flag = True
                            break
                        sf_of_chunk.add(item_sf)
                        
                    if flag:
                        continue
                # sf全一样才行
                # if(type_of_fs == "odess"):
                #     flag = False
                #     sf_of_chunk = set()
                #     item_sfs = get_gear_super_feature(chunk,size)
                #     # for sf in sf_to_block:
                #         # if((item_sfs[0] == sf[0]) + (item_sfs[1] == sf[1]) + (item_sfs[2] == sf[2]) >1):
                #     if item_sfs in sf_to_block:
                #         ref_chunk = sf_to_block[item_sfs]
                #         # print(type(item_sfs))
                #         # print(type(sf_to_block))
                #         # print(chunk)
                #         # print(ref_chunk)
                #         # print(size)
                #         diff_size = compute_difference_detla(chunk, ref_chunk,size)
                #         # print(diff_size)
                #         modified_bytes += diff_size
                #         flag = True
                #     sf_of_chunk.add(item_sfs)
                        
                #     if flag:
                #         continue
                
                
                if(type_of_fs == "odess2"):
                    flag = False
                    sf_of_chunk = set()
                    item_sfs = get_gear_super_feature(chunk,size)
                    for sf in sf_to_block:
                        # print(sf)
                        if((item_sfs[0] == sf[0]) + (item_sfs[1] == sf[1]) + (item_sfs[2] == sf[2]) >1):
                            ref_chunk = sf_to_block[sf]
                            diff_size = compute_difference_detla(chunk, ref_chunk,size)
                            # print(diff_size)
                            modified_bytes += diff_size
                            flag = True
                            break
                    sf_of_chunk.add(item_sfs)
                        
                    if flag:
                        continue
                if(type_of_fs == "fin"):
                    flag = False
                    sf_of_chunk = set()
                    
                    for item_sf in get_finesse_super_feature(chunk,size):  
                        if item_sf in sf_to_block:
                            ref_chunk = sf_to_block[item_sf]
                            # print(item_sf)
                            diff_size = compute_difference_detla(chunk, ref_chunk,size)
                            # print(diff_size)
                            modified_bytes += diff_size
                            flag = True
                            break
                        sf_of_chunk.add(item_sf)
                    
                    if flag:
                        continue
                if(type_of_fs == "fin+"):
                    flag = False
                    sf_of_chunk = set()
                    
                    item_sfs = get_finesse_super_feature(chunk,size) 
                    if item_sfs in sf_to_block:
                        ref_chunk = sf_to_block[item_sfs]
                        # print(item_sf)
                        diff_size = compute_difference_detla(chunk, ref_chunk,size)
                        # print(diff_size)
                        modified_bytes += diff_size
                        flag = True
                    sf_of_chunk.add(item_sf)
                    
                    if flag:
                        continue
                elif(type_of_fs == "burst"):
                    flag = False
                    hhash,thash = hthash(chunk,size)
                    if hhash in hhash_to_block:
                        ref_chunk = hhash_to_block[hhash]
                        diff_size = compute_difference_burst(chunk, ref_chunk)
                        # print(diff_size)
                        if (is_detect == False) or diff_size < size // 3:             
                            modified_bytes += diff_size
                            flag = True
                    if thash in thash_to_block and not flag:
                        ref_chunk = thash_to_block[thash]
                        diff_size = compute_difference_burst(chunk, ref_chunk)
                        if (is_detect == False) or diff_size < size // 3:             
                            modified_bytes += diff_size
                            flag = True
                    
                    if flag:
                        continue
                    
                
                # 如果该块没有相似块，认为它是唯一的块，增加唯一字节数
                seen_blocks.add(chunk_hash)
                unique_bytes += size  # DEDUP 增加字节数
                # block_storage[chunk_hash] = chunk
                # 存储 Sf 值
                if(type_of_fs == "fin"):
                    for sf in sf_of_chunk:
                        sf_to_block[sf] = chunk
                        # print(sf)
                if(type_of_fs == "odess1"):
                    for sf in sf_of_chunk:
                        sf_to_block[sf] = chunk
                        # print(sf)
                    # print(sf_to_block)
                if(type_of_fs == "odess2" or type_of_fs == "fin+"):
                    for sf in sf_of_chunk:
                        # print(sf)
                        sf_to_block[sf] = chunk
                    
                if(type_of_fs == "burst"):
                    hhash_to_block[hhash] = chunk
                    thash_to_block[thash] = chunk

    # if(type_of_fs == "fin" or type_of_fs == "burst"):
    #     dedup_rate = total_bytes / (unique_bytes + modified_bytes) if unique_bytes else 0
    # else:
    #     dedup_rate = total_bytes / unique_bytes if unique_bytes else 0
    dedup_rate = total_bytes / (unique_bytes + modified_bytes) if unique_bytes else 0
    return total_bytes, unique_bytes, modified_bytes, dedup_rate


def get_parser():
    parser = argparse.ArgumentParser(description="接受一个文件目录并列出其中的文件。") 
    # 接受一个目录路径参数
    parser.add_argument('-d','--directory', type=str, required=True,help="要处理的目录路径")
    parser.add_argument('-t','--type', type=str, required=True,help="使用的文件系统类型,dedup,burst,fin,odess1(gear),odess2,fin+其他值默认为dedup")
    parser.add_argument('-b','--block_size_kb', type=int,required=True, help="以kb为单位的块大小")
    parser.add_argument('-r','--head_rate', type=int, help="块的头部大小占比,1/n")
    parser.add_argument('-i','--is_detect',action='store_true', help="burst启用detect")
    
    return parser

def print_info(elapsed_time, time_feature, time_diff, total_bytes, unique_bytes, delta_bytes, dedup_rate):
    print(f"代码执行时间: {elapsed_time:.2f} 秒")
    print(f"特征提取时间: {time_feature:.2f} 秒")
    print(f"计算时间: {time_diff:.2f} 秒")
    print(f"throughput: {total_bytes / elapsed_time / 1024 / 1024:.2f} MB/s")
    print(f"Total bytes processed (ALLOC): {total_bytes/1024/1024:.2f} MB")
    print(f"Unique bytes after deduplication (DEDUP): {unique_bytes/1024/1024:.2f} MB")
    print(f"Modified bytes (for incremental storage): {delta_bytes/1024/1024:.2f} MB")
    print(f"Delta Deduplication rate (for incremental storage): {dedup_rate:.2f}")

def main():
    global type_of_fs
    global size_per_chunk
    global head_rate
    global is_detect
    parser = get_parser()
    args = parser.parse_args()
    
    directory = args.directory
    block_size_kb = args.block_size_kb
    size_per_chunk = int(block_size_kb) * 1024
    if args.head_rate:
        head_rate = args.head_rate
    if args.is_detect:
        is_detect = True
    type_of_fs = args.type
    # print(size_per_chunk)
    start_time = time.time()
    # 调用去重模拟
    total_bytes, unique_bytes, modified_bytes, dedup_rate = simulate_deduplication(directory,size_per_chunk,type_of_fs)
    # 获取当前时间
    end_time = time.time()
    elapsed_time = end_time - start_time
  
    print_info(elapsed_time, time_feature,time_diff,total_bytes, unique_bytes, modified_bytes, dedup_rate)


if __name__ == "__main__":
    main()
