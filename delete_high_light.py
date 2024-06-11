import os
from PIL import Image, ImageStat

dir_path = 'F:\\4k桌面\\New'
min_brightness_threshold = 180

del_dir = os.path.join(dir_path, 'del')
if not os.path.exists(del_dir):
    os.makedirs(del_dir)

def new_func(dir_path, min_brightness_threshold, del_dir):
    for file in os.listdir(dir_path):
        if file.endswith(".jpg"):
            img_file_path = os.path.join(dir_path, file)
            try:
                img = Image.open(img_file_path)
                stat = ImageStat.Stat(img)
                brightness = stat.mean[0]  # average pixel value in R channel (red)
                if brightness > min_brightness_threshold:
                    print(f"Found bright image: {file} ({brightness})")
                    os.rename(img_file_path, os.path.join(del_dir, file))
            except Exception as e:
                print(f"Failed to open {file}: {str(e)}")

new_func(dir_path, min_brightness_threshold, del_dir)
print("Done.1112344")