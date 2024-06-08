import os
import re
import requests
import humanize
import concurrent.futures
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from humanize import naturalsize

CHROME_DRIVER_PATH = 'D:\chromedriver\chromedriver.exe'

def check_4k_resolution(url):
    response = requests.head(url)
    return 'x3840' in response.headers.get('Content-Type', '')

def adjust_image_url(url):
        url = url[:url.rindex('-')] + '-3840x2160-' + url[url.rindex('-') + 1:]
        url = url.replace('.html', '.jpg')
        url = url.replace('black-dark', 'images/wallpapers')
        return url


def download_image(download_url, file_path):
    try:
        response = requests.get(download_url, stream=True)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print(f"Error downloading {download_url}: {e}")

def get_movie_wallpapers(start_page, end_page):
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(executable_path=CHROME_DRIVER_PATH))

    try:
        for page in range(start_page, end_page + 1):
            url = f'https://4kwallpapers.com/black-dark/?page={page}'
            print(f"Processing page {page}...")
            driver.get(url)

            # Wait for the page to load
            wait = WebDriverWait(driver, 50)

            # Get the page source
            content = driver.page_source

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')

            # Find all movie wallpapers on this page
            wallpaper_links = soup.find_all('a', {'class': re.compile(r'wallpaper|hd')})
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for link in wallpaper_links:
                    download_url = adjust_image_url(link['href'])
                    if not download_url.startswith('http'):
                        download_url = 'https://4kwallpapers.com' + download_url
                    filename = os.path.join('F:\\4k桌面\\black', os.path.basename(download_url))
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
    finally:
            driver.quit()

get_movie_wallpapers(1, 74)
print('All balck wallpapers links printed!')
subprocess.run(['python', 'delete_little_error.py'])

