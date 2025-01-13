import os
import re

# 用于提取从文件中获得的去重率、吞吐量和计算时长
def extract_metrics_from_file(file_path):
    """
    从给定的输出文件中提取去重率、吞吐量和计算时间
    :param file_path: 输出文件路径
    :return: 一个字典，包含去重率、吞吐量和计算时间
    """
    metrics = {
        "Deduplication Rate": None,
        "Throughput (MB/s)": None,
        "Computation Time (s)": None
    }
    
    # 定义正则表达式
    dedup_pattern = r"Delta Deduplication rate.*?:\s*(\d+\.\d+)"
    throughput_pattern = r"throughput:\s*(\d+\.\d+)\s*MB/s"
    computation_time_pattern = r"计算时间:\s*(\d+\.\d+)\s*秒"

    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # 使用正则表达式查找相关值
        dedup_match = re.search(dedup_pattern, content)
        throughput_match = re.search(throughput_pattern, content)
        computation_time_match = re.search(computation_time_pattern, content)
        
        if dedup_match:
            metrics["Deduplication Rate"] = float(dedup_match.group(1))
        if throughput_match:
            metrics["Throughput (MB/s)"] = float(throughput_match.group(1))
        if computation_time_match:
            metrics["Computation Time (s)"] = float(computation_time_match.group(1))
    
    return metrics

def collect_metrics(directory, block_sizes, file_types):
    """
    收集指定目录下不同块大小和文件类型的去重率、吞吐量和计算时间
    :param directory: 数据集目录
    :param block_sizes: 块大小列表
    :param file_types: 文件类型列表
    :return: 返回一个包含所有数据的列表
    """
    all_metrics = []

    # 遍历不同的块大小和文件类型
    for block_size in block_sizes:
        for file_type in file_types:
            # 构建文件路径
            file_name = f"{directory}_{file_type}_{block_size}KB.txt"
            if file_type == "burst":
                file_name = f"{directory}_{file_type}_{block_size}KB_8.txt"
            file_path = os.path.join(f"result_{directory}", file_name)
            
            if os.path.exists(file_path):
                metrics = extract_metrics_from_file(file_path)
                
                # 收集结果
                all_metrics.append({
                    "Directory": directory,
                    "Block Size (KB)": block_size,
                    "File Type": file_type,
                    "Deduplication Rate": metrics["Deduplication Rate"],
                    "Throughput (MB/s)": metrics["Throughput (MB/s)"],
                    "Computation Time (s)": metrics["Computation Time (s)"]
                })
            else:
                # 如果文件不存在，则记录为 None
                all_metrics.append({
                    "Directory": directory,
                    "Block Size (KB)": block_size,
                    "File Type": file_type,
                    "Deduplication Rate": None,
                    "Throughput (MB/s)": None,
                    "Computation Time (s)": None
                })

    return all_metrics

def print_metrics_summary(metrics):
    """
    打印统计结果
    :param metrics: 统计结果列表
    """
    print(f"{'Directory':<25}{'Block Size (KB)':<20}{'File Type':<10}{'Deduplication Rate':<20}{'Throughput (MB/s)':<20}{'Computation Time (s)':<20}")
    print("="*105)
    
    for metric in metrics:
        print(f"{metric['Directory']:<25}{metric['Block Size (KB)']:<20}{metric['File Type']:<10}{metric['Deduplication Rate']:<20}{metric['Throughput (MB/s)']:<20}{metric['Computation Time (s)']:<20}")

def main():
    # 定义目录、块大小和文件类型
    # directories = ["webh","sim","sim_base1","toolcode","toolcode-tar","lnxk","lnxtar","vmi"]
    directories = ["toolcode","lnxk","vmbackup"]
    block_sizes = [4, 8, 16]
    file_types = ["dedup", "burst", "fin"]
    
    # 收集所有数据
    all_metrics = []
    for directory in directories:
        metrics = collect_metrics(directory, block_sizes, file_types)
        all_metrics.extend(metrics)
    
    # 打印统计结果
    print_metrics_summary(all_metrics)

if __name__ == "__main__":
    main()
