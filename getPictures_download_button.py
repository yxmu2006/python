import os
import re
import time
import requests
import humanize
import concurrent.futures
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

#下载movie PNG格式的 10个并发

def adjust_image_url(url):
    # Use regular expressions to extract the width and height from the URL
    match = re.search(r'(\d+)x(\d+)', url)
    if match:
        width, height = map(int, match.groups())
        
        # Check if the resolution is not 4K
        if (width, height) != (3840, 2160):
            # Replace the existing resolution with 4K
            new_url = f"{url[:match.start()]}{3840}x2160{url[match.end():]}"
            return new_url
    return url

def download_image(download_url, filename):
    img_response = requests.get(download_url)
    img_response.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(img_response.content)

    file_stats = os.stat(filename)
    file_size = file_stats.st_size
    print(f"Downloaded: {filename} File size: {(humanize.naturalsize(file_size))}")
# 创建保存壁纸的文件夹
os.makedirs('wallpapers', exist_ok=True)

# 设置 ChromeDriver 的路径
chrome_driver_path = r'D:\chromedriver\chromedriver.exe'  # 请替换为您的 ChromeDriver 路径

# 创建 ChromeDriver 服务对象
service = Service(executable_path=chrome_driver_path)

# 初始化 WebDriver
driver = webdriver.Chrome(service=service)
try:
    # Your code that might raise an SSL error
    driver.get('https://4kwallpapers.com/ultrawide-monitor-hd-wallpapers/')
except WebDriverException as e:
    if "ssl_client_socket_impl.cc" in str(e):
        print("SSL error detected, skipping...")
    else:
        raise

# 打开目标网页

# 等待页面加载
wait = WebDriverWait(driver, 30)

# 点击“Load More”按钮10次，每次延迟1秒
for _ in range(30):
    try:
        load_more_button = wait.until(EC.element_to_be_clickable((By.ID, 'load-more-button')))
        ActionChains(driver).move_to_element(load_more_button).click(load_more_button).perform()
        time.sleep(0.5)
    except Exception as e:
        print(f"点击“Load More”按钮时出错: {e}")
        break

# 获取页面内容
content = driver.page_source

# 使用 BeautifulSoup 解析内容
soup = BeautifulSoup(content, 'html.parser')

# 查找所有“Download”链接
download_links = soup.find_all('a', string='Download')
# 遍历所有下载链接并下载图片
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for link in download_links:
        download_url = adjust_image_url(link['href'])
        if not download_url.startswith('http'):
            download_url = 'https://4kwallpapers.com' + download_url
        filename = os.path.join('d:\\wallpapers', os.path.basename(download_url))
        if not os.path.exists(filename):
            print(f"Downloading: {filename}...")

            # Create a future for each download task
            futures.append(executor.submit(download_image, download_url, filename))

    # Wait for all downloads to complete
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Error downloading {future.result()}: {e}")
# 关闭浏览器
driver.quit()

print('所有壁纸已下载完成！')
subprocess.run(['python', 'delete_little_error.py'])
