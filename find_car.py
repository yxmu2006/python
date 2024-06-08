import os
import shutil
from ultralytics import YOLO
from concurrent.futures import ThreadPoolExecutor

# 初始化YOLOv8模型
model = YOLO('yolov8n.pt')  # 可以根据需要选择不同的YOLOv8模型

# 定义路径
source_dir = 'F:\\4k桌面\\wallpapers'
target_dir = 'F:\\4k桌面\\wallpapers\\del'

# 确保目标目录存在
os.makedirs(target_dir, exist_ok=True)

# 定义要检测的类别ID
target_classes = [1, 2, 3]  # 自行车、汽车、摩托车的ID

# 获取所有图片文件路径
all_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'))]

# 将文件分成100组
num_groups = 100
file_groups = [all_files[i::num_groups] for i in range(num_groups)]

def process_files(file_group):
    for file_path in file_group:
        try:
            # 使用YOLOv8模型进行目标检测
            results = model(file_path)
            
            # 检查检测结果中是否包含目标类别
            for result in results:
                for obj in result.boxes:
                    if obj.cls in target_classes:
                        # 如果检测到目标类别，则将图片移动到目标目录
                        shutil.move(file_path, os.path.join(target_dir, os.path.basename(file_path)))
                        print(f"Moved {os.path.basename(file_path)} to {target_dir}")
                        break
        except FileNotFoundError:
            print(f"Image Not Found: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

# 使用ThreadPoolExecutor进行并发处理
with ThreadPoolExecutor(max_workers=num_groups) as executor:
    executor.map(process_files, file_groups)