import os
import shutil



def copy_directory(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
        print(f"Created directory {dest}")

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            copy_directory(src_path, dest_path)
            print(f"Copied directory {src_path} to {dest_path}")
        else:
            shutil.copy(src_path, dest_path)
            print(f"Copied file {src_path} to {dest_path}")
