def dynamic_threshold_gear_hash(data, window_size=4, initial_threshold=1000000, mod_value=123456789):
    """
    动态调整阈值进行 Gear Hash 分块
    :param data: 输入数据（字节流或字符串）
    :param window_size: 窗口大小
    :param initial_threshold: 初始哈希阈值
    :param mod_value: 模值，用于限制哈希值的范围
    :return: 块的边界位置列表
    """
    def simple_gear_hash(data):
        # Gear Hash 通过简单的加法和位移来计算哈希值
        hash_val = 0
        for char in data:
            hash_val = (hash_val << 5) + ord(char)  # 左移5位后加上字符的ASCII值
            hash_val = hash_val % mod_value  # 使用模运算避免哈希值无限增长
        return hash_val

    chunk_boundaries = []
    current_hash = simple_gear_hash(data[:window_size])
    
    # 使用初始阈值
    threshold = initial_threshold
    
    for i in range(window_size, len(data)):
        current_hash = (current_hash << 5) + ord(data[i])  # 移位并加上字符ASCII值
        current_hash -= ord(data[i - window_size])  # 去掉最左边的字符影响
        current_hash = current_hash % mod_value  # 使用模运算保持哈希值在合理范围内

        # 如果哈希值小于阈值，认为这里是一个块的边界
        if current_hash < threshold:
            chunk_boundaries.append(i)
            # 动态调整阈值，例如根据当前的哈希值变化调整
            threshold = (threshold + current_hash) // 2  # 取当前哈希值与上一个哈希值的平均值

    return chunk_boundaries


# 测试数据
data = "This is a test string used for dynamic threshold Gear Hashing example."
boundaries = dynamic_threshold_gear_hash(data)
print(f"Block boundaries for Gear Hash (with dynamic threshold): {boundaries}")
