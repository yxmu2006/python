import os

# Set the directory path and the file size threshold (50 KB)
dir_path = 'F:\\4k桌面\\Game'
size_threshold = 50000  # 50 KB

# Get a list of files in the directory
files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

# Iterate over the files and delete the small JPEG files
print("Deleting small JPEG files...")
for file in files:
    if file.endswith('.jpg') and os.path.getsize(os.path.join(dir_path, file)) < size_threshold:
        os.remove(os.path.join(dir_path, file))
        print(f"Deleted {file}")

print("Done!")
