import os

# Set the directory path and extension to consider
dir_path = 'F:\\4k桌面\\NEW'
ext_to_remove = '.png'

# Get a list of files in the directory
files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

# Create a set to store duplicate file names with different extensions
duplicates = set()

for file in files:
    # Check if the file name has already been seen with a different extension
    if any(file.startswith(s) for s in duplicates):
        continue

    # Add the file name to the duplicates set
    duplicates.add(file)

# Print the duplicate file names with different extensions
print("Duplicate file names with different extensions:")
for dup in duplicates:
    print(dup)

# Remove the PNG files from the directory
print("\nRemoving PNG files...")
for file in files:
    if file.endswith(ext_to_remove):
        os.remove(os.path.join(dir_path, file))
        print(f"Removed {file}")

print("Done!")
