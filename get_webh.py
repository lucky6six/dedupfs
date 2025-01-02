import requests
import os
import time

# 网站 URL
url = "www.sjtu.edu.cn"

# 创建一个文件夹来保存网页历史
folder = "wayback_history"
if not os.path.exists(folder):
    os.mkdir(folder)

# 定义获取Wayback Machine页面快照的函数
def get_wayback_snapshot(url, timestamp):
    # Wayback Machine API 查询
    api_url = f"http://archive.org/wayback/available?url={url}&timestamp={timestamp}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        # 检查是否有找到快照
        if 'archived_snapshots' in data and 'closest' in data['archived_snapshots']:
            snapshot_url = data['archived_snapshots']['closest']['url']
            print(f"快照链接: {snapshot_url}")
            return snapshot_url
        else:
            print(f"未找到时间戳 {timestamp} 的快照。")
            return None
    else:
        print(f"API 请求失败，状态码：{response.status_code}")
        return None

# 下载指定 URL 的网页内容
def download_page(url, timestamp):
    snapshot_url = get_wayback_snapshot(url, timestamp)
    if snapshot_url:
        # 请求网页内容
        page_response = requests.get(snapshot_url)
        if page_response.status_code == 200:
            # 保存文件
            filename = f"{folder}/{url.replace('https://', '').replace('http://', '').replace('/', '_')}_{timestamp}.html"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(page_response.text)
            print(f"已保存快照：{filename}")
        else:
            print(f"下载快照失败，状态码：{page_response.status_code}")
    else:
        print(f"未找到快照，跳过时间戳：{timestamp}")

# 示例：抓取多个日期的快照
timestamps = ['20200101', '20210101', '20220101']  # 你想抓取的多个时间戳
#生成2024年1月1日到2024年12月31日每一天的时间戳
for year in range(2024, 2025):
    for month in range(1, 13):
        for day in range(1, 32):
            timestamps.append(f"{year}{month:02d}{day:02d}")

for timestamp in timestamps:
    download_page(url, timestamp)
    time.sleep(2)  # 给服务器一点时间，避免请求过于频繁
    
# httrack "https://www.sjtu.edu.cn/" -O "webhttrack" -r2  "-*" "+*.html" "+*.css" "+*.js"